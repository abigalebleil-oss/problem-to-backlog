"""Human review log for a plan. No AI involved.

  python checks/review.py start  <03_plan.md>      create review.csv next to the plan, one row per item
  python checks/review.py status <review.csv>      is review complete? acceptance metrics and reasons

Every milestone, CVD, requirement, unverified assumption and alignment conflict gets a row.
Reviewers fill in: disposition (accept | edit | reject), reason (required for edit and reject),
reviewer and date. The completed file is the review record for the plan, and its numbers show
where the skill or a persona needs improving.
"""

import csv
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks  # noqa: E402

FIELDS = ["id", "type", "title", "disposition", "reason", "reviewer", "date"]
DISPOSITIONS = {"accept", "edit", "reject"}


def start(plan_path):
    text = Path(plan_path).read_text()
    milestones, cvds, reqs = checks.parse_plan(text)
    rows = [{"id": k, "type": "milestone", "title": v["title"]} for k, v in milestones.items()]
    rows += [{"id": k, "type": "cvd", "title": v["title"]} for k, v in cvds.items()]
    rows += [{"id": k, "type": "requirement", "title": checks.field(v["lines"], "Text")} for k, v in reqs.items()]
    for line in checks.section_lines(text, "Assumptions"):
        a = checks.ASSUMPTION.match(line)
        if a and a.group(4).upper() == "UNVERIFIED":
            rows.append({"id": a.group(1), "type": "assumption", "title": a.group(2)})
    for line in checks.section_lines(text, "Cross-team alignment"):
        m = checks.ALIGN.match(line)
        if m and m.group(2).lower() in {"conflict", "not applicable"}:
            rows.append({"id": m.group(1), "type": "alignment", "title": f"{m.group(2)} {m.group(3)}"})
    out = Path(plan_path).with_name("review.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({**{k: "" for k in FIELDS}, **r})
    print(f"Wrote {len(rows)} review rows to {out}")
    return 0


def status(review_path):
    with open(review_path, newline="") as f:
        rows = list(csv.DictReader(f))
    problems, counts, reasons = [], Counter(), Counter()
    for r in rows:
        d = (r["disposition"] or "").strip().lower()
        if not d:
            problems.append(f"{r['id']}: no disposition yet")
            continue
        if d not in DISPOSITIONS:
            problems.append(f"{r['id']}: disposition '{d}' must be accept, edit or reject")
            continue
        counts[d] += 1
        if d in {"edit", "reject"}:
            if not r["reason"].strip():
                problems.append(f"{r['id']}: {d} needs a reason")
            else:
                reasons[r["reason"].strip().lower()] += 1
        if not r["reviewer"].strip():
            problems.append(f"{r['id']}: no reviewer named")
    total = sum(counts.values())
    print(f"Review of {review_path}: {total}/{len(rows)} items decided")
    if total:
        for d in ("accept", "edit", "reject"):
            print(f"  {d:<7} {counts[d]:>3}  ({counts[d] / total:.0%})")
    if reasons:
        print("  Top reasons (feed these back into the skill or persona):")
        for reason, n in reasons.most_common(5):
            print(f"    {n} × {reason}")
    if problems:
        print(f"\nREVIEW INCOMPLETE: {len(problems)} item(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"\nReview complete on {date.today().isoformat()}. Plan may enter the backlog.")
    return 0


def main(argv):
    if len(argv) != 3 or argv[1] not in {"start", "status"}:
        print(__doc__)
        return 2
    return start(argv[2]) if argv[1] == "start" else status(argv[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
