# problem-to-backlog

**From a user problem to implementation-ready work, with the whole organization aligned.**

An AI skill plus deterministic guardrails that turns discovery output and a technical design into
milestones, customer value deliveries and requirements, shaped by each domain's expertise and the
company's standards, with humans approving at every gate.

> Sandbox version of a skill I built and use as a Software Product Owner at my current company.
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

**How we'll know it works:** throughput first, then quality.
- Cycle time from discovery complete to backlog-ready
- Review rounds before sign-off
- Share of drafted items accepted without edit (from the review log)
- Post-start changes to story descriptions and acceptance criteria
- Story split and reopen rates
- PO time spent per milestone
- Defects traced to requirement gaps

## How it works

### Three layers of knowledge, and nothing else
| Layer | Lives in | Owned by | Example |
|---|---|---|---|
| **Company** | `knowledge/company.md` | Product ops | Definition of ready, release calendar, "shall" standard |
| **Persona** (domain) | `personas/*.md` | Each domain's POs | Clinical analyzer: safety > turnaround; never auto-resolve a discrepancy |
| **Initiative** | `initiatives/<INIT>/` | The PO running it | Whatever the PO wants requirements for: their own brief, plus discovery and design when they exist |

Every line the AI may rely on has an ID (`K-4`, `VD-CA-1`, `C-MW-2`, `F-03`, `D-5`). If something
isn't in these files, the AI must list it as an assumption or ask about it.

### Vetted, local sources: do the work once, reuse it everywhere
Every company and persona line ends with the source it came from, for example
`- C-CA-1: An ABO/Rh discrepancy is never resolved ... automatically by software [src: S-CA-2, S-CA-3]`.
Each source is a saved file (interview notes, SOP excerpt, standards summary, support data) with
an owner and a vetting record:

```
personas/clinical-analyzer.md          the persona: what the skill reads and cites
personas/sources/clinical-analyzer/
  S-CA-1_standards.md                  standard   vetted by regulatory affairs
  S-CA-2_po-interview.md               interview  vetted by the interviewee
  S-CA-3_discrepancy-sop.md            sop        vetted by the customer site supervisor
```

A business team builds this once with the `create-persona` skill. After that, every PO in the
domain drafts from the same vetted knowledge instead of the model's general knowledge, so there
is less room for hallucination and fewer assumptions to check. The checks enforce it:
- a persona line without a registered, existing source **fails**
- a persona marked `validated` with an unvetted source **fails**
- a source vetted more than 12 months ago is queued for **re-vetting**
- a plan that cites persona lines resting on unvetted sources is **flagged** for sign-off
- `checks.py provenance <plan>` shows every citation traced back to its source file and who vetted it

### Personas: domain expertise, captured once, reused by everyone
| Persona | Top value driver | A non-negotiable it brings |
|---|---|---|
| `flow-cytometry` | Reproducibility across days, operators, instruments, sites | Older experiments reopen with their original results |
| `clinical-analyzer` (blood typing analyzers) | The right blood type on the right patient's record | A typing discrepancy is never resolved by software |
| `middleware-reporting` (analyzer → LIS → clinician) | Interoperability with every supported LIS; only verified results reach clinicians | Results run after a QC failure are never reported until QC is acceptable |
| `_template.md` / `create-persona` skill | **Create your own** by being interviewed | |

Seeded status: `clinical-analyzer` is validated (all sources vetted, by fictional reviewers). The other
two are drafts with unvetted interview notes, so the review queue shows what that looks like.

A run picks a **primary persona** (ranks the work, sets mandatory requirement fields) and any
**consulted personas** (adjacent teams whose constraints the plan must honor). Consulted personas
are how cross-team alignment happens before the first meeting, not after.

### The flow: AI drafts, code checks, people decide
| Step | AI produces | Deterministic check | Human gate |
|---|---|---|---|
| 0 Set up | Persona menu (or build your own), initiative menu (or start a new one), extra guardrails, then "What are we trying to write requirements for?" | `checks.py persona`: every line sourced, sources vetted | PO picks personas, adds guardrails, states the work in their own words |
| 1 Intake | Questions (every persona "always ask" + gaps), assumptions | `checks.py intake`: fails on any unanswered blocking question | **Gate 1:** PO answers, confirms or rejects assumptions |
| 2 Milestones | Milestones ordered by the persona's value drivers | | **Gate 2:** PO and dev lead approve scope |
| 3 Plan | CVDs, requirements, alignment, decision log | `checks.py plan`: citations, verbatim quotes, coverage, persona fields, banned terms, every constraint aligned | |
| 4 Review | Trace matrix, provenance, review log | `checks.py provenance`; `review.py status`: every item decided, every edit and reject has a reason | **Gate 3:** each persona's sign-offs |

The check never approves anything. A pass means "worth a human's time", and it always prints a
**review queue**: unverified assumptions, AI-proposed values, conflicts, deferrals.

## Quick start
```bash
python3 -m pytest -q                                                           # 22 tests
python3 checks/checks.py persona    personas/flow-cytometry.md
python3 checks/checks.py intake     examples/INIT-001/clinical-analyzer/01_intake.md
python3 checks/checks.py plan       examples/INIT-001/clinical-analyzer/03_plan.md
python3 checks/checks.py plan       examples/INIT-001/middleware-reporting/03_plan.md
python3 checks/checks.py plan       examples/INIT-002/flow-cytometry/03_plan.md
python3 checks/checks.py provenance examples/INIT-001/clinical-analyzer/03_plan.md
python3 checks/checks.py plan       examples/INIT-001/planted-failures/03_plan.md   # fails on purpose
```
In Claude Code, run the skill with `/problem-to-backlog`, or `/create-persona` to add a domain.
Python 3.9+ standard library only.

## Repo map
```
.claude/skills/problem-to-backlog/SKILL.md   the skill (steps, gates, output format)
.claude/skills/create-persona/SKILL.md     interview a domain expert into a persona pack
knowledge/company.md, knowledge/sources/  company layer and its vetted sources
personas/                                  domain layer (3 seeded + template)
personas/sources/<persona>/                the vetted sources each persona was built from
initiatives/INIT-001-typing-holds/         blood typing holds: feedback, discovery, design
initiatives/INIT-002-cross-instrument-reproducibility/   flow cytometry: feedback, discovery, design
initiatives/INIT-003-imaging-flow-cytometer/  started from one sentence: "a flow cytometer that has imaging capabilities"
checks/checks.py                           persona, intake (Gate 1), plan, trace, provenance
checks/review.py                           human review log and acceptance metrics
examples/INIT-001/                         clinical analyzer, middleware, planted failures
examples/INIT-002/                         flow cytometry
examples/INIT-003/                         new initiative from one sentence: intake stops on 5 blocking questions
examples/create-persona/                   interview notes for a live create-persona demo (clinical lab QC) and the finished backup
tests/                                     guardrail tests
docs/DEMO.md                               live demo script
```

## What code can't catch
`examples/INIT-001/planted-failures/03_plan.md` includes a requirement that auto-resolves ABO
discrepancies. It is well formed, cites real IDs and claims to satisfy the "never auto-resolve"
constraint, so it passes every check that applies to it (the file as a whole still fails, on the
other planted errors). A test documents that on purpose: deterministic checks prove
an output is **grounded and complete**; only a qualified human can judge whether it is **right**.
That is why the gates exist.

## What is real and what is synthetic
- **Real:** the approach, the gate design and the problem it solves come from my work at Waters.
- **Synthetic:** the TypeBridge and CytoSuite products, interviews, SOPs, support data, reviewers,
  numbers and example outputs. Example outputs were
  drafted to illustrate the format; in the demo the skill regenerates them live.
- **Seeded personas and their sources** were written for the sandbox from public standards and
  general domain knowledge. In a real deployment each source is a controlled document or a
  recorded interview, vetted by its owner through `create-persona`.
