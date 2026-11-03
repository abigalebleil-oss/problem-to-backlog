"""Deterministic guardrails for the problem-to-ready skill. No AI involved.

  python checks/checks.py persona <persona.md>    is a persona pack complete and well formed?
  python checks/checks.py intake  <01_intake.md>  Gate 1: may the skill move past intake?
  python checks/checks.py plan    <03_plan.md>    is the plan grounded, complete and ready for human review?
  python checks/checks.py trace   <03_plan.md> [out.csv]   export the traceability matrix
  python checks/checks.py provenance <01_intake.md|03_plan.md>  which vetted sources each citation rests on

Exit code 0 = pass. Exit code 1 = problems found (the AI regenerates or a human decides).
A pass never means "approved". It means "worth a human's time to review".
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge as kb  # noqa: E402

HEADER = re.compile(
    r"^# (Intake|Delivery plan):\s*(INIT-\d{3})\s*·\s*persona:\s*([\w-]+)"
    r"(?:\s*·\s*consulted:\s*(.+?))?\s*$", re.M)
EXTERNAL_ID = re.compile(r"(?<![\w-])(F-\d+|D-\d+|DC-\d+|K-\d+|(?:U|VD|REG|C|Q)-[A-Z]{2,3}-\d+)(?![\w-])")
QUOTE_WITH_SOURCE = re.compile(r'"([^"]+)"\s*\[source:\s*([\w.-]+)\]')
SOURCE_REF = re.compile(r"\[source:\s*([\w.-]+)\]")
MILESTONE = re.compile(r"^### (MS-\d+)\s+—\s+(.+)$")
CVD = re.compile(r"^### (CVD-\d+)\s+·\s+(MS-\d+)?\s*·?\s*(.*)$")
REQ = re.compile(r"^### (REQ-\d+)\s+·\s+(.+)$")
REQ_REF = re.compile(r"\bREQ-\d+\b")
CVD_REF = re.compile(r"\bCVD-\d+\b")
USER_NEED = re.compile(r"^As an? .+?, I need .+? so that .+", re.I)
AC_LINE = re.compile(r"^\s*-\s*AC-\d+:\s*(.*)$")
GWT = re.compile(r"\bGiven\b.+\bwhen\b.+\bthen\b", re.I)
ASSUMPTION = re.compile(r"^-\s+(A-\d+):\s*(.+?)\s*\|\s*basis:\s*(.*?)\s*\|\s*status:\s*(\w+)\s*$")
QUESTION = re.compile(r"^-\s+(Q-(?:[A-Z]{2,3}-)?\d+)\s*\[(blocking|non-blocking)\]:\s*(.+?)(?:\s*\|\s*answer:\s*(.*))?$")
ALIGN = re.compile(r"^-\s+(C-[A-Z]{2,3}-\d+):\s*(addressed by|CONFLICT|not applicable)\b\s*(.*)$", re.I)
DEFERRED = re.compile(r"^-\s+((?:F|D)-\d+):\s*deferred\b(.*)$", re.I)
VERIFICATION_METHODS = {"test", "inspection", "analysis", "demonstration"}


# ---------- shared helpers ----------

def parse_header(text):
    m = HEADER.search(text)
    if not m:
        return None
    consulted = []
    if m.group(4) and m.group(4).strip().lower() != "none":
        consulted = [c.strip() for c in m.group(4).split(",") if c.strip()]
    return {"kind": m.group(1), "init": m.group(2), "persona": m.group(3), "consulted": consulted}


def load_context(header, problems):
    """Load the initiative, the primary persona and consulted personas named in the header."""
    initiative = kb.Initiative(header["init"])
    if not initiative.found:
        problems.append(f"{header['init']}: no matching folder in initiatives/")
    personas = []
    for pid in [header["persona"]] + header["consulted"]:
        p = kb.load_persona(pid)
        if p is None:
            problems.append(f"persona '{pid}' not found in personas/")
        else:
            personas.append(p)
    return initiative, personas


def known_external_ids(initiative, personas):
    ids = set(kb.company_ids()) | set(initiative.ids)
    for p in personas:
        ids |= set(p.ids)
    return ids


def banned_regex(personas):
    terms = set(kb.COMPANY_BANNED)
    for p in personas:
        terms |= set(p.banned_terms)
    pattern = "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True))
    return re.compile(rf"(?<![\w-])({pattern})(?![\w-])", re.I)


def check_citations(text, initiative, personas, problems):
    """Every external ID exists; every source file exists; every quote is verbatim."""
    known = known_external_ids(initiative, personas)
    def norm(s):
        return " ".join(s.split())
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("#"):
            continue
        for ref in sorted(set(EXTERNAL_ID.findall(line))):
            if ref not in known:
                problems.append(f"line {lineno}: {ref} is not in the company, persona or initiative knowledge")
        for src in SOURCE_REF.findall(line):
            if src not in initiative.feedback:
                problems.append(f"line {lineno}: [source: {src}] does not exist in the initiative's feedback")
        for quote, src in QUOTE_WITH_SOURCE.findall(line):
            if src in initiative.feedback and norm(quote) not in norm(initiative.feedback[src]):
                problems.append(f'line {lineno}: quote "{quote[:45]}..." is not verbatim in {src}')


def field(lines, name):
    for line in lines:
        m = re.match(rf"^\s*-\s+{re.escape(name)}:\s*(.*)$", line, re.I)
        if m:
            return m.group(1).strip()
    return ""


def section_lines(text, title):
    return kb.sections(text).get(title, [])


def report(title, problems, queue=None, extra=None):
    print(title)
    if extra:
        print(extra)
    if queue:
        print(f"\nREVIEW QUEUE — needs a human decision ({len(queue)}):")
        for q in queue:
            print(f"  • {q}")
    if problems:
        print(f"\nFAILED: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        print("Result: NOT READY. Regenerate, or fix the input it depends on.")
        return 1
    print("\nResult: PASS. Ready for human review (this is not an approval).")
    return 0


# ---------- persona ----------

def check_persona(path):
    problems = []
    p = kb.Persona(path)
    if not p.title:
        problems.append("missing '# Persona: <title>' line")
    if not p.id or "<" in (p.id or ""):
        problems.append("missing 'id:'")
    elif Path(path).stem != p.id:
        problems.append(f"id '{p.id}' does not match file name '{Path(path).stem}'")
    if not p.prefix or not re.fullmatch(r"[A-Z]{2,3}", p.prefix):
        problems.append("prefix must be 2–3 capital letters")
    for s in kb.PERSONA_SECTIONS:
        if s not in p.sections:
            problems.append(f"missing section '## {s}'")
    if "<" in p.text.split("-->")[-1]:
        problems.append("still contains <placeholders>")
    for kind, label in (("U", "user"), ("VD", "value driver"), ("C", "non-negotiable constraint"),
                        ("Q", "always-ask question")):
        if not p.of_type(kind):
            problems.append(f"needs at least one {label} ({kind}-{p.prefix}-n)")
    for pid in p.ids:
        m = kb.PERSONA_ID.match(pid)
        if m and m.group(2) != p.prefix:
            problems.append(f"{pid}: prefix does not match persona prefix {p.prefix}")
    if "verification" not in p.required_fields:
        problems.append("Requirement fields must include 'verification'")
    if not p.banned_terms:
        problems.append("Banned terms is empty")
    prefixes = Counter(x.prefix for x in kb.list_personas())
    if p.prefix and prefixes[p.prefix] > 1 and not Path(path).name.startswith("_"):
        problems.append(f"prefix {p.prefix} is used by more than one persona")

    # provenance: every line cites a registered, existing, owned source
    queue = []
    if not p.sources:
        problems.append("no sources registered under '## Sources'")
    for line in p.source_lines:
        if not kb.SOURCE_LINE.match(line):
            problems.append(f"source line not in the required format: {line[:70]}")
    for sid, s in p.sources.items():
        if p.prefix and not sid.startswith(f"S-{p.prefix}-"):
            problems.append(f"{sid}: prefix does not match persona prefix {p.prefix}")
        if s.type not in kb.SOURCE_TYPES:
            problems.append(f"{sid}: type '{s.type}' must be one of {', '.join(sorted(kb.SOURCE_TYPES))}")
        if not s.path.exists():
            problems.append(f"{sid}: file {s.file} does not exist")
        if not s.vetted and s.vetted_raw.upper() != "PENDING":
            problems.append(f"{sid}: vetted must be 'YYYY-MM-DD by <name/role>' or PENDING")
        elif not s.vetted:
            queue.append(f"{sid} not vetted yet ({s.title}); owner: {s.owner}")
        elif s.stale:
            queue.append(f"{sid} last vetted {s.vetted_on}, over {kb.STALE_AFTER_DAYS} days ago; re-vet with {s.owner}")
    cited = set()
    for lid, srcs in p.line_sources.items():
        if not srcs:
            problems.append(f"{lid}: no [src: ...] tag; every persona line must name its source")
        for sid in srcs:
            cited.add(sid)
            if sid not in p.sources:
                problems.append(f"{lid}: cites {sid}, which is not registered under Sources")
    for sid in p.sources:
        if sid not in cited:
            queue.append(f"{sid} is registered but no persona line cites it")
    unvetted = [sid for sid, s in p.sources.items() if not s.vetted]
    if (p.status or "").lower().startswith("validated") and unvetted:
        problems.append(f"status is validated but {', '.join(unvetted)} not vetted")

    vetted_lines = sum(1 for srcs in p.line_sources.values()
                       if srcs and all(p.sources.get(s) and p.sources[s].vetted for s in srcs))
    summary = (f"  {p.title or '?'} · {len(p.users)} users · {len(p.value_drivers)} value drivers · "
               f"{len(p.constraints)} constraints · {len(p.questions)} questions · "
               f"fields: {', '.join(p.required_fields) or '-'}\n"
               f"  Status: {p.status} · {len(p.sources)} sources · "
               f"{vetted_lines}/{len(p.line_sources)} lines rest only on vetted sources")
    return report(f"Checking persona {path}", problems, queue, summary)


# ---------- intake (Gate 1) ----------

def check_intake(path):
    text = Path(path).read_text()
    problems, queue = [], []
    header = parse_header(text)
    if not header or header["kind"] != "Intake":
        return report(f"Checking intake {path}",
                      ["missing '# Intake: INIT-xxx · persona: <id> · consulted: <ids|none>' header"])
    initiative, personas = load_context(header, problems)
    check_citations(text, initiative, personas, problems)

    questions = {}
    for line in section_lines(text, "Questions"):
        m = QUESTION.match(line)
        if m:
            questions[m.group(1)] = (m.group(2), m.group(3), (m.group(4) or "").strip())
    for p in personas:
        for qid in p.questions:
            if qid not in questions:
                problems.append(f"{qid}: persona question from '{p.id}' was not asked")
    for qid, (kind, q, answer) in questions.items():
        if kind == "blocking" and not answer:
            problems.append(f"{qid} [blocking] has no answer: {q}")
        elif not answer:
            queue.append(f"{qid} unanswered (non-blocking): {q}")

    assumptions = [ASSUMPTION.match(l) for l in section_lines(text, "Assumptions")]
    assumptions = [a for a in assumptions if a]
    if not assumptions:
        problems.append("no assumptions listed. Every intake states what it is assuming")
    for a in assumptions:
        if a.group(4).upper() not in {"UNVERIFIED", "CONFIRMED", "REJECTED"}:
            problems.append(f"{a.group(1)}: status must be UNVERIFIED, CONFIRMED or REJECTED")
        elif a.group(4).upper() == "UNVERIFIED":
            queue.append(f"{a.group(1)} unverified: {a.group(2)}")

    extra = (f"  {header['init']} · persona {header['persona']} · consulted "
             f"{', '.join(header['consulted']) or 'none'} · {len(questions)} questions · "
             f"{len(assumptions)} assumptions")
    return report(f"Gate 1 — checking intake {path}", problems, queue, extra)


# ---------- plan ----------

def parse_plan(text):
    milestones, cvds, reqs = {}, {}, {}
    current = None
    for line in text.splitlines():
        m, c, r = MILESTONE.match(line), CVD.match(line), REQ.match(line)
        if m:
            current = milestones.setdefault(m.group(1), {"title": m.group(2), "lines": []})
        elif c:
            current = cvds.setdefault(c.group(1), {"milestone": c.group(2), "title": c.group(3), "lines": []})
        elif r:
            current = reqs.setdefault(r.group(1), {"title": r.group(2), "lines": []})
        elif line.startswith("## "):
            current = None
        elif current is not None:
            current["lines"].append(line)
    return milestones, cvds, reqs


def analyze_plan(text):
    problems, queue = [], []
    header = parse_header(text)
    if not header or header["kind"] != "Delivery plan":
        return None, ["missing '# Delivery plan: INIT-xxx · persona: <id> · consulted: <ids|none>' header"], [], {}
    initiative, personas = load_context(header, problems)
    if not personas:
        return header, problems, queue, {}
    primary = personas[0]
    check_citations(text, initiative, personas, problems)
    banned = banned_regex(personas)
    all_users = {u for p in personas for u in p.users}
    all_drivers = {v for p in personas for v in p.value_drivers}

    milestones, cvds, reqs = parse_plan(text)
    for label, items in (("milestones", milestones), ("customer value deliveries", cvds), ("requirements", reqs)):
        if not items:
            problems.append(f"no {label} found")

    traced, req_used = set(), set()
    for cid, c in cvds.items():
        L = c["lines"]
        if not c["milestone"]:
            problems.append(f"{cid}: no milestone")
        elif c["milestone"] not in milestones:
            problems.append(f"{cid}: milestone {c['milestone']} is not defined")
        user = field(L, "User")
        if user not in all_users:
            problems.append(f"{cid}: User '{user}' is not a user in the selected personas")
        if not USER_NEED.match(field(L, "User need")):
            problems.append(f"{cid}: user need is not 'As a ..., I need ... so that ...'")
        vd = field(L, "Value driver")
        if vd not in all_drivers:
            problems.append(f"{cid}: value driver '{vd}' is not a value driver in the selected personas")
        c["driver"] = vd
        trace = EXTERNAL_ID.findall(field(L, "Traces to"))
        if not trace:
            problems.append(f"{cid}: does not trace to any finding or design element")
        traced |= set(trace)
        rlist = REQ_REF.findall(field(L, "Requirements"))
        if not rlist:
            problems.append(f"{cid}: lists no requirements")
        for r in rlist:
            if r not in reqs:
                problems.append(f"{cid}: {r} is not defined in Requirements")
        req_used |= set(rlist)
        acs = [AC_LINE.match(l).group(1) for l in L if AC_LINE.match(l)]
        c["acs"] = len(acs)
        if not acs:
            problems.append(f"{cid}: no acceptance criteria")
        for i, ac in enumerate(acs, start=1):
            if not GWT.search(ac):
                problems.append(f"{cid} AC-{i}: not written as Given / when / then")
            for w in sorted({w.lower() for w in banned.findall(ac)}):
                problems.append(f"{cid} AC-{i}: banned vague term '{w}'")
            if "[PROPOSED]" in ac:
                queue.append(f"{cid} AC-{i} contains an AI-proposed value: {ac}")

    for rid, r in reqs.items():
        L = r["lines"]
        txt = field(L, "Text")
        if " shall " not in f" {txt} ":
            problems.append(f"{rid}: requirement text does not use 'shall'")
        for w in sorted({w.lower() for w in banned.findall(txt)}):
            problems.append(f"{rid}: banned vague term '{w}'")
        if "[PROPOSED]" in txt:
            queue.append(f"{rid} contains an AI-proposed value: {txt}")
        derived = EXTERNAL_ID.findall(field(L, "Derived from"))
        if not derived:
            problems.append(f"{rid}: not derived from any finding, design element or constraint")
        r["derived"] = derived
        for f in primary.required_fields:
            if not field(L, f):
                problems.append(f"{rid}: missing field '{f}' required by persona {primary.id}")
        v = field(L, "verification").lower()
        r["verification"] = v
        if v and v not in VERIFICATION_METHODS:
            problems.append(f"{rid}: verification '{v}' is not test, inspection, analysis or demonstration")
        if rid not in req_used:
            problems.append(f"{rid}: not delivered by any customer value delivery")

    for mid in milestones:
        if not any(c["milestone"] == mid for c in cvds.values()):
            problems.append(f"{mid}: milestone has no customer value deliveries")

    deferred = {}
    for line in section_lines(text, "Deferred"):
        m = DEFERRED.match(line)
        if m:
            deferred[m.group(1)] = m.group(2).strip(" —-:")
            queue.append(f"{m.group(1)} deferred{(': ' + deferred[m.group(1)]) if deferred[m.group(1)] else ''}")
    derived_all = {d for r in reqs.values() for d in r.get("derived", [])}
    for fid in initiative.findings:
        if fid.startswith("F-") and fid not in traced and fid not in deferred:
            problems.append(f"{fid}: finding not addressed by any CVD and not deferred")
    for did in initiative.design_elements:
        if did not in derived_all and did not in deferred:
            problems.append(f"{did}: design element not covered by any requirement and not deferred")

    aligned = {}
    for line in section_lines(text, "Cross-team alignment"):
        m = ALIGN.match(line)
        if m:
            aligned[m.group(1)] = (m.group(2).lower(), m.group(3))
    for p in personas:
        for cid in p.constraints:
            if cid not in aligned:
                problems.append(f"{cid}: constraint from '{p.id}' is missing from Cross-team alignment")
                continue
            kind, rest = aligned[cid]
            if kind == "addressed by":
                refs = REQ_REF.findall(rest)
                if not refs:
                    problems.append(f"{cid}: 'addressed by' names no requirement")
                for ref in refs:
                    if ref not in reqs:
                        problems.append(f"{cid}: addressed by {ref}, which is not defined")
            elif kind == "conflict":
                queue.append(f"{cid} CONFLICT {rest}")
            else:
                queue.append(f"{cid} marked not applicable {rest}")

    for line in section_lines(text, "Assumptions"):
        a = ASSUMPTION.match(line)
        if a and a.group(4).upper() == "UNVERIFIED":
            queue.append(f"{a.group(1)} unverified: {a.group(2)}")
    for line in section_lines(text, "Open questions"):
        q = QUESTION.match(line)
        if q and q.group(2) == "blocking":
            problems.append(f"{q.group(1)} is a blocking question still open. Resolve it at Gate 1 first")
        elif q:
            queue.append(f"{q.group(1)} open: {q.group(3)}")
    if not any(ASSUMPTION.match(l) for l in section_lines(text, "Assumptions")):
        problems.append("no Assumptions section entries. Every plan states what it assumed")
    if not [l for l in section_lines(text, "Decision log") if l.strip().startswith("- DEC-")]:
        problems.append("no Decision log entries. Every plan explains its main choices")

    for p in personas:
        cited = {i for i in set(EXTERNAL_ID.findall(text)) if i in p.ids}
        weak = sorted(i for i in cited
                      if not all(p.sources.get(s) and p.sources[s].vetted for s in p.line_sources.get(i, [])))
        if weak:
            pending = sorted({s for i in weak for s in p.line_sources[i]
                              if not (p.sources.get(s) and p.sources[s].vetted)})
            queue.append(f"persona {p.id}: {len(weak)} cited line(s) rest on unvetted source(s) "
                         f"{', '.join(pending)}. Vet before sign-off")

    stats = {"header": header, "primary": primary, "milestones": milestones, "cvds": cvds,
             "reqs": reqs, "initiative": initiative}
    return header, problems, queue, stats


def plan_summary(stats):
    if not stats:
        return ""
    primary, ms, cvds, reqs = stats["primary"], stats["milestones"], stats["cvds"], stats["reqs"]
    lines = [f"  {stats['header']['init']} · persona {primary.id} · consulted "
             f"{', '.join(stats['header']['consulted']) or 'none'}",
             f"  {len(ms)} milestones · {len(cvds)} customer value deliveries · {len(reqs)} requirements",
             "", "  How the persona shaped the plan (value driver per CVD, by milestone):"]
    for mid, m in ms.items():
        drivers = Counter(c["driver"] for c in cvds.values() if c["milestone"] == mid)
        acs = sum(c.get("acs", 0) for c in cvds.values() if c["milestone"] == mid)
        lines.append(f"    {mid} {m['title'][:46]:<46} {acs:>2} ACs  "
                     + ", ".join(f"{d}×{n}" for d, n in drivers.items()))
    methods = Counter(r.get("verification") or "?" for r in reqs.values())
    lines.append("  Verification methods: " + ", ".join(f"{k} {v}" for k, v in methods.items()))
    if "safety-class" in primary.required_fields:
        classes = Counter(field(r["lines"], "safety-class") or "?" for r in reqs.values())
        lines.append("  Safety class: " + ", ".join(f"{k} {v}" for k, v in sorted(classes.items())))
    return "\n".join(lines)


def check_plan(path):
    text = Path(path).read_text()
    _, problems, queue, stats = analyze_plan(text)
    return report(f"Checking plan {path}", problems, queue, plan_summary(stats))


# ---------- traceability export ----------

def export_trace(path, out=None):
    text = Path(path).read_text()
    header, problems, _, stats = analyze_plan(text)
    if not stats:
        print("Cannot export: plan header or personas are invalid")
        return 1
    initiative = stats["initiative"]
    rows = []
    for cid, c in stats["cvds"].items():
        sources = EXTERNAL_ID.findall(field(c["lines"], "Traces to"))
        for rid in REQ_REF.findall(field(c["lines"], "Requirements")):
            r = stats["reqs"].get(rid, {"lines": [], "title": "?"})
            for src in sources or ["-"]:
                rows.append({"source": src, "source_text": initiative.ids.get(src, ""),
                             "milestone": c["milestone"], "cvd": cid, "cvd_title": c["title"],
                             "requirement": rid, "requirement_text": field(r["lines"], "Text"),
                             "verification": field(r["lines"], "verification")})
    out = Path(out) if out else Path(path).with_name("trace_matrix.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["source"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} trace rows to {out}")
    if problems:
        print(f"Warning: the plan has {len(problems)} open problem(s); run 'plan' first.")
    return 0


# ---------- provenance ----------

def provenance(path):
    """Show, for every company or persona ID an output cites, the source it came from."""
    text = Path(path).read_text()
    header = parse_header(text)
    if not header:
        print("missing '# Intake:' or '# Delivery plan:' header")
        return 1
    problems = []
    initiative, personas = load_context(header, problems)
    company_lines, company_sources = kb.company_provenance()
    owners = [("company", company_lines, company_sources)]
    for p in personas:
        owners.append((p.id, {k: (p.ids[k], p.line_sources[k]) for k in p.ids}, p.sources))

    cited = []
    for i in dict.fromkeys(EXTERNAL_ID.findall(text)):
        for owner, lines, sources in owners:
            if i in lines:
                cited.append((i, owner, lines[i][1], sources))
                break

    by_source, unvetted_ids = {}, []
    for i, owner, srcs, sources in cited:
        for s in srcs or ["(none)"]:
            by_source.setdefault((owner, s), []).append(i)
        if not srcs or not all(sources.get(s) and sources[s].vetted for s in srcs):
            unvetted_ids.append(i)

    init_ids = [i for i in dict.fromkeys(EXTERNAL_ID.findall(text)) if i in initiative.ids]
    print(f"Provenance for {path}")
    print(f"  {len(cited)} company/persona citations · {len(init_ids)} initiative citations "
          f"(discovery and design for {header['init']})\n")
    all_sources = {(o, sid): s for o, _, srcs in owners for sid, s in srcs.items()}
    for (owner, sid), ids in sorted(by_source.items()):
        s = all_sources.get((owner, sid))
        if s is None:
            print(f"  {sid:<8} UNREGISTERED SOURCE                              ← {', '.join(ids)}")
            continue
        print(f"  {sid:<8} {s.type:<10} {s.title[:44]:<44} {s.label}")
        print(f"  {'':<8} {'':<10} file: {(s.path.relative_to(kb.ROOT))}")
        print(f"  {'':<8} {'':<10} cited via: {', '.join(ids)}")
    vetted = len(cited) - len(unvetted_ids)
    print(f"\n  {vetted}/{len(cited)} company/persona citations rest only on vetted sources.")
    if unvetted_ids:
        print(f"  Not yet vetted: {', '.join(unvetted_ids)}. Vet these sources before sign-off.")
    for p in problems:
        print(f"  - {p}")
    return 1 if problems else 0


def main(argv):
    if len(argv) < 3 or argv[1] not in {"persona", "intake", "plan", "trace", "provenance"}:
        print(__doc__)
        return 2
    cmd, path = argv[1], argv[2]
    if cmd == "persona":
        return check_persona(path)
    if cmd == "intake":
        return check_intake(path)
    if cmd == "plan":
        return check_plan(path)
    if cmd == "provenance":
        return provenance(path)
    return export_trace(path, argv[3] if len(argv) > 3 else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
