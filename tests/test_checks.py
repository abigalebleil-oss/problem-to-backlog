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


def test_four_personas_with_unique_prefixes():
    personas = kb.list_personas()
    assert {p.id for p in personas} == {"blood-bank", "clinical-qc", "flow-cytometry", "middleware-connectivity"}
    assert len({p.prefix for p in personas}) == 4


# ---------- Gate 1 ----------

def test_answered_intake_passes_gate():
    assert checks.check_intake(EX / "blood-bank" / "01_intake.md") == 0


def test_unanswered_blocking_question_fails_gate(tmp_path):
    text = (EX / "blood-bank" / "01_intake.md").read_text()
    lines = [l.split("| answer:")[0] + "| answer:" if l.startswith("- Q-BB-1 ") else l
             for l in text.splitlines()]
    f = tmp_path / "01_intake.md"
    f.write_text("\n".join(lines))
    assert checks.check_intake(f) == 1


def test_skipped_persona_question_fails_gate(tmp_path):
    text = (EX / "blood-bank" / "01_intake.md").read_text()
    lines = [l for l in text.splitlines() if not l.startswith("- Q-MW-2 ")]
    f = tmp_path / "01_intake.md"
    f.write_text("\n".join(lines))
    assert checks.check_intake(f) == 1


# ---------- plans ----------

def test_blood_bank_plan_passes():
    problems, queue, stats = plan_problems(EX / "blood-bank" / "03_plan.md")
    assert problems == []
    assert len(stats["milestones"]) == 4 and len(stats["cvds"]) == 8 and len(stats["reqs"]) == 12
    assert any("C-MW-3 CONFLICT" in q for q in queue)
    assert any("[PROPOSED]" in q for q in queue)


def test_middleware_plan_passes_and_differs():
    problems, queue, stats = plan_problems(EX / "middleware-connectivity" / "03_plan.md")
    assert problems == []
    bb = plan_problems(EX / "blood-bank" / "03_plan.md")[2]
    assert stats["primary"].required_fields != bb["primary"].required_fields
    assert any("D-7 deferred" in q for q in queue)
    assert any("C-QC-3 CONFLICT" in q for q in queue)


def test_planted_failures_are_all_caught():
    problems, _, _ = plan_problems(EX / "planted-failures" / "03_plan.md")
    text = "\n".join(problems)
    assert "not verbatim in 01_night_bb_tech.md" in text
    assert "F-12 is not in the company, persona or initiative knowledge" in text
    assert "CVD-05 AC-1: banned vague term 'promptly'" in text
    assert "REQ-07: banned vague term 'promptly'" in text
    assert "REQ-04: missing field 'safety-class'" in text
    assert "F-09: finding not addressed" in text
    assert "REQ-09: not delivered by any customer value delivery" in text
    assert "C-QC-1: constraint from 'clinical-qc' is missing" in text


def test_well_formed_but_unsafe_requirement_is_not_caught_by_code():
    """REQ-05 now auto-resolves discrepancies, violating C-BB-1, yet is well formed.
    The checks cannot judge meaning. This is why the human review gate exists."""
    problems, _, _ = plan_problems(EX / "planted-failures" / "03_plan.md")
    assert not any(p.startswith("REQ-05") for p in problems)
    assert "automatically resolve" in (EX / "planted-failures" / "03_plan.md").read_text()


def test_wrong_persona_in_header_is_rejected():
    text = (EX / "blood-bank" / "03_plan.md").read_text().replace(
        "persona: blood-bank", "persona: hematology", 1)
    problems, _, _ = plan_problems(text)
    assert any("persona 'hematology' not found" in p for p in problems)


# ---------- trace and review ----------

def test_trace_export(tmp_path):
    out = tmp_path / "trace.csv"
    assert checks.export_trace(EX / "blood-bank" / "03_plan.md", out) == 0
    rows = list(csv.DictReader(out.open()))
    assert {"F-09", "D-7"} <= {r["source"] for r in rows}
    assert all(r["verification"] for r in rows)


def test_review_log_blocks_until_every_item_decided(tmp_path):
    plan = tmp_path / "03_plan.md"
    plan.write_text((EX / "blood-bank" / "03_plan.md").read_text())
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
