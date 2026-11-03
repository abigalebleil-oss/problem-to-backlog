# problem-to-ready

**From a user problem to implementation-ready work, with the whole organization aligned.**

An AI skill plus deterministic guardrails that turns discovery output and a technical design into
milestones, customer value deliveries and requirements, shaped by each domain's expertise and the
company's standards, with humans approving at every gate.

> Sandbox version of a skill I built and use as a Software Product Owner at Waters (flow cytometry).
> Everything here is synthetic: the "TypeBridge" product, people, sites and numbers are fictional.

---

## The problem

Going from a user problem to work a team can build is slowed less by writing than by **alignment**.
Product, engineering, QA, regulatory and adjacent product teams each hold constraints and domain
knowledge the others don't. That knowledge surfaces late, as review comments, rework, re-planned
milestones and defects.

**Goal:** shorten the time from *problem understood* to *ready to implement* by generating first-draft
delivery artifacts that already reflect each domain's value drivers, constraints and company
knowledge, and by making every assumption, open question and cross-team conflict visible to the
people who must decide.

**Who it's for:** product owners, and the engineering, QA, regulatory and partner-team reviewers who
have to agree before work enters a backlog.

**How we'll know it works:**
- Cycle time from discovery complete to backlog-ready
- Review rounds before sign-off
- Share of drafted items accepted without edit (from the review log)
- Defects traced to requirement gaps

## How it works

### Three layers of knowledge, and nothing else
| Layer | Lives in | Owned by | Example |
|---|---|---|---|
| **Company** | `knowledge/company.md` | Product ops | Definition of ready, release calendar, "shall" standard |
| **Persona** (domain) | `personas/*.md` | Each domain's POs | Blood bank: safety > turnaround; never auto-resolve a discrepancy |
| **Initiative** | `initiatives/<INIT>/` | The PO running it | Discovery findings, design elements, interview quotes |

Every line the AI may rely on has an ID (`K-4`, `VD-BB-1`, `C-MW-2`, `F-03`, `D-5`). If something
isn't in these files, the AI must list it as an assumption or ask about it.

### Personas: domain expertise, captured once, reused by everyone
| Persona | Top value driver | A non-negotiable it brings |
|---|---|---|
| `flow-cytometry` | Reproducibility across days, operators, instruments, sites | Older experiments reopen with their original results |
| `clinical-qc` | QC failures stop reporting before results reach clinicians | QC rule changes need director approval |
| `middleware-connectivity` | Interoperability with every supported LIS | New outbound messages are opt-in per interface |
| `blood-bank` | Right blood to the right patient | A discrepancy is never resolved by software |
| `_template.md` / `create-persona` skill | **Create your own** by being interviewed | |

A run picks a **primary persona** (ranks the work, sets mandatory requirement fields) and any
**consulted personas** (adjacent teams whose constraints the plan must honor). Consulted personas
are how cross-team alignment happens before the first meeting, not after.

### The flow: AI drafts, code checks, people decide
| Step | AI produces | Deterministic check | Human gate |
|---|---|---|---|
| 0 Select persona | Persona menu | `checks.py persona` | PO picks primary and consulted |
| 1 Intake | Questions (every persona "always ask" + gaps), assumptions | `checks.py intake`: fails on any unanswered blocking question | **Gate 1:** PO answers, confirms or rejects assumptions |
| 2 Milestones | Milestones ordered by the persona's value drivers | | **Gate 2:** PO and dev lead approve scope |
| 3 Plan | CVDs, requirements, alignment, decision log | `checks.py plan`: citations, verbatim quotes, coverage, persona fields, banned terms, every constraint aligned | |
| 4 Review | Trace matrix, review log | `review.py status`: every item decided, every edit and reject has a reason | **Gate 3:** each persona's sign-offs |

The check never approves anything. A pass means "worth a human's time", and it always prints a
**review queue**: unverified assumptions, AI-proposed values, conflicts, deferrals.

## Quick start
```bash
python -m pytest -q                                                         # 13 tests
python checks/checks.py intake examples/INIT-001/blood-bank/01_intake.md
python checks/checks.py plan   examples/INIT-001/blood-bank/03_plan.md
python checks/checks.py plan   examples/INIT-001/middleware-connectivity/03_plan.md
python checks/checks.py plan   examples/INIT-001/planted-failures/03_plan.md   # fails on purpose
```
In Claude Code, run the skill with `/problem-to-ready`, or `/create-persona` to add a domain.
Python 3.9+ standard library only.

## Repo map
```
.claude/skills/problem-to-ready/SKILL.md   the skill (steps, gates, output format)
.claude/skills/create-persona/SKILL.md     interview a domain expert into a persona pack
knowledge/company.md                       company layer
personas/                                  domain layer (4 seeded + template)
initiatives/INIT-001-typing-holds/         initiative layer: feedback, discovery, design
checks/checks.py                           persona, intake (Gate 1), plan, trace export
checks/review.py                           human review log and acceptance metrics
examples/INIT-001/                         reference outputs: blood bank, middleware, planted failures
tests/                                     guardrail tests
docs/DEMO.md                               live demo script
```

## What code can't catch
`examples/INIT-001/planted-failures/03_plan.md` includes a requirement that auto-resolves ABO
discrepancies. It is well formed, cites real IDs and claims to satisfy the "never auto-resolve"
constraint, so every check passes it. A test documents that on purpose: deterministic checks prove
an output is **grounded and complete**; only a qualified human can judge whether it is **right**.
That is why the gates exist.

## What is real and what is synthetic
- **Real:** the approach, the gate design and the problem it solves come from my work at Waters.
- **Synthetic:** the TypeBridge product, interviews, numbers and example outputs. Example outputs were
  drafted to illustrate the format; in the demo the skill regenerates them live.
- **Seeded personas** come from public standards and general domain knowledge, and are marked for
  validation with real domain POs via `create-persona`.
