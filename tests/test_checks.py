"""Tests for the deterministic guardrails. Run: python -m pytest -q"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "checks"))

import checks  # noqa: E402
import knowledge as kb  # noqa: E402
import review  # noqa: E402

EX = ROOT / "examples" / "INIT-001"


def plan_problems(path_or_text):
    text = path_or_text.read_text() if isinstance(path_or_text, Path) else path_or_text
    _, problems, queue, stats = checks.analyze_plan(text)
    return problems, queue, stats


# ---------- personas ----------

def test_all_seeded_personas_pass():
    for p in kb.list_personas():
        assert checks.check_persona(p.path) == 0, p.path


def test_template_fails_until_filled_in():
    assert checks.check_persona(ROOT / "personas" / "_template.md") == 1


def test_seeded_personas_present_with_unique_prefixes():
    # Teams add their own personas with create-persona, so check the seeded three are
    # present and that every persona's prefix is unique, not an exact list.
    personas = kb.list_personas()
    assert {"clinical-analyzer", "flow-cytometry", "middleware-reporting"} <= {p.id for p in personas}
    assert len({p.prefix for p in personas}) == len(personas)


def test_create_persona_backup_passes():
    assert checks.check_persona(ROOT / "examples" / "create-persona" / "clinical-qc.md") == 0


# ---------- Gate 1 ----------

def test_answered_intake_passes_gate():
    assert checks.check_intake(EX / "clinical-analyzer" / "01_intake.md") == 0


def test_unanswered_blocking_question_fails_gate(tmp_path):
    text = (EX / "clinical-analyzer" / "01_intake.md").read_text()
    lines = [l.split("| answer:")[0] + "| answer:" if l.startswith("- Q-CA-1 ") else l
             for l in text.splitlines()]
    f = tmp_path / "01_intake.md"
    f.write_text("\n".join(lines))
    assert checks.check_intake(f) == 1


def test_skipped_persona_question_fails_gate(tmp_path):
    text = (EX / "clinical-analyzer" / "01_intake.md").read_text()
    lines = [l for l in text.splitlines() if not l.startswith("- Q-MW-2 ")]
    f = tmp_path / "01_intake.md"
    f.write_text("\n".join(lines))
    assert checks.check_intake(f) == 1


# ---------- plans ----------

def test_clinical_analyzer_plan_passes():
    problems, queue, stats = plan_problems(EX / "clinical-analyzer" / "03_plan.md")
    assert problems == []
    assert len(stats["milestones"]) == 4 and len(stats["cvds"]) == 8 and len(stats["reqs"]) == 12
    assert any("C-MW-3 CONFLICT" in q for q in queue)
    assert any("[PROPOSED]" in q for q in queue)


def test_middleware_plan_passes_and_differs():
    problems, queue, stats = plan_problems(EX / "middleware-reporting" / "03_plan.md")
    assert problems == []
    bb = plan_problems(EX / "clinical-analyzer" / "03_plan.md")[2]
    assert stats["primary"].required_fields != bb["primary"].required_fields
    assert any("D-7 deferred" in q for q in queue)
    assert any("C-MW-7 CONFLICT" in q for q in queue)


def test_planted_failures_are_all_caught():
    problems, _, _ = plan_problems(EX / "planted-failures" / "03_plan.md")
    text = "\n".join(problems)
    assert "not verbatim in 01_night_typing_tech.md" in text
    assert "F-12 is not in the company, persona or initiative knowledge" in text
    assert "CVD-05 AC-1: banned vague term 'promptly'" in text
    assert "REQ-07: banned vague term 'promptly'" in text
    assert "REQ-04: missing field 'safety-class'" in text
    assert "F-09: finding not addressed" in text
    assert "REQ-09: not delivered by any customer value delivery" in text
    assert "C-MW-5: constraint from 'middleware-reporting' is missing" in text


def test_well_formed_but_unsafe_requirement_is_not_caught_by_code():
    """REQ-05 now auto-resolves discrepancies, violating C-CA-1, yet is well formed.
    The checks cannot judge meaning. This is why the human review gate exists."""
    problems, _, _ = plan_problems(EX / "planted-failures" / "03_plan.md")
    assert not any(p.startswith("REQ-05") for p in problems)
    assert "automatically resolve" in (EX / "planted-failures" / "03_plan.md").read_text()


def test_wrong_persona_in_header_is_rejected():
    text = (EX / "clinical-analyzer" / "03_plan.md").read_text().replace(
        "persona: clinical-analyzer", "persona: hematology", 1)
    problems, _, _ = plan_problems(text)
    assert any("persona 'hematology' not found" in p for p in problems)


# ---------- trace and review ----------

def test_trace_export(tmp_path):
    out = tmp_path / "trace.csv"
    assert checks.export_trace(EX / "clinical-analyzer" / "03_plan.md", out) == 0
    rows = list(csv.DictReader(out.open()))
    assert {"F-09", "D-7"} <= {r["source"] for r in rows}
    assert all(r["verification"] for r in rows)


def test_review_log_blocks_until_every_item_decided(tmp_path):
    plan = tmp_path / "03_plan.md"
    plan.write_text((EX / "clinical-analyzer" / "03_plan.md").read_text())
    assert review.start(plan) == 0
    log = tmp_path / "review.csv"
    assert review.status(log) == 1
    rows = list(csv.DictReader(log.open()))
    for r in rows:
        r.update(disposition="accept", reviewer="PO", date="2026-11-03")
    rows[0].update(disposition="edit", reason="")
    with log.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=review.FIELDS)
        w.writeheader()
        w.writerows(rows)
    assert review.status(log) == 1
    rows[0]["reason"] = "window too optimistic"
    with log.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=review.FIELDS)
        w.writeheader()
        w.writerows(rows)
    assert review.status(log) == 0


# ---------- provenance ----------

def _persona_copy(tmp_path, pid, edit):
    """Copy a persona and its sources into a temp personas/ folder, apply edit, return the path."""
    import shutil
    d = tmp_path / "personas"
    shutil.copytree(ROOT / "personas" / "sources", d / "sources")
    f = d / f"{pid}.md"
    f.write_text(edit((ROOT / "personas" / f"{pid}.md").read_text()))
    return f


def test_every_persona_line_cites_a_registered_source():
    for p in kb.list_personas():
        for lid, srcs in p.line_sources.items():
            assert srcs and all(s in p.sources for s in srcs), (p.id, lid)
        for s in p.sources.values():
            assert s.path.exists(), s.file


def test_line_without_source_fails(tmp_path):
    f = _persona_copy(tmp_path, "clinical-analyzer",
                      lambda t: t.replace("(bench technologist, often alone on nights) [src: S-CA-2]",
                                          "(bench technologist, often alone on nights)"))
    assert checks.check_persona(f) == 1


def test_unregistered_or_missing_source_fails(tmp_path):
    f = _persona_copy(tmp_path, "clinical-analyzer", lambda t: t.replace("[src: S-CA-1]", "[src: S-CA-9]", 1))
    assert checks.check_persona(f) == 1
    f = _persona_copy(tmp_path / "b", "clinical-analyzer",
                      lambda t: t.replace("S-CA-3_discrepancy-sop.md", "S-CA-3_missing.md"))
    assert checks.check_persona(f) == 1


def test_validated_persona_with_unvetted_source_fails(tmp_path):
    f = _persona_copy(tmp_path, "clinical-analyzer",
                      lambda t: t.replace("vetted: 2026-10-20 by R. Ortiz, interviewee (fictional)", "vetted: PENDING"))
    assert checks.check_persona(f) == 1


def test_plan_flags_reliance_on_unvetted_sources():
    _, queue, _ = plan_problems(EX.parent / "INIT-002" / "flow-cytometry" / "03_plan.md")
    assert any("persona flow-cytometry" in q and "S-FC-2" in q for q in queue)
    _, queue, _ = plan_problems(EX / "clinical-analyzer" / "03_plan.md")
    assert not any(q.startswith("persona clinical-analyzer") for q in queue)


def test_company_knowledge_lines_have_vetted_sources():
    lines, sources = kb.company_provenance()
    assert lines and all(srcs and all(sources[s].vetted for s in srcs) for _, srcs in lines.values())


def test_provenance_command_runs(capsys):
    assert checks.provenance(EX / "clinical-analyzer" / "03_plan.md") == 0
    out = capsys.readouterr().out
    assert "S-CA-3" in out and "rest only on vetted sources" in out


# ---------- flow cytometry initiative ----------

def test_flow_cytometry_intake_and_plan_pass():
    flow = EX.parent / "INIT-002" / "flow-cytometry"
    assert checks.check_intake(flow / "01_intake.md") == 0
    problems, queue, stats = plan_problems(flow / "03_plan.md")
    assert problems == []
    assert "reproducibility-impact" in stats["primary"].required_fields
    assert any("D-3 deferred" in q for q in queue)
