---
name: problem-to-backlog
description: Turn an initiative's discovery output and technical design into milestones, customer value deliveries and requirements that are ready to implement, shaped by a domain persona and company knowledge, with human approval gates and deterministic checks. Use when a PO wants to go from a user problem to backlog-ready work.
---

# Problem → Backlog-ready work

Alignment is the slowest part of getting from a user problem to work a team can build. This
skill drafts the artifacts every group needs to agree on, already shaped by the domain's value
drivers, constraints and company standards, and puts every assumption, open question and
cross-team conflict in front of a human before anything is committed.

**The AI drafts. Code checks. People decide.** You never skip a gate, and you never mark
anything approved.

## Knowledge you may use (and nothing else)
| Layer | File | IDs you may cite |
|---|---|---|
| Company | `knowledge/company.md` | `K-n` |
| Persona | `personas/<id>.md` | `U-`, `VD-`, `REG-`, `C-`, `Q-<PREFIX>-n` |
| Initiative | `initiatives/<INIT>/discovery.md`, `design.md`, `feedback/*.md` | `F-n`, `D-n`, `DC-n`, verbatim quotes |

If a fact is not in these files, it is an **assumption** (list it) or a **question** (ask it).
Never invent an ID. Never paraphrase inside quotation marks. Do not fill gaps with general
knowledge about the domain: the persona and company files exist so that you draft from vetted,
local knowledge instead. Every company and persona line names the vetted source it came from.

Write all outputs to `initiatives/<INIT>/runs/<primary-persona>/`.

---

## Step 0 — Select your persona
1. List the personas in `personas/` (skip `_template.md`) with their title, top value driver,
   status, and how many of their sources are vetted (`python checks/checks.py persona <file>`).
2. Ask the user (use AskUserQuestion if available):
   - **Primary persona**: whose product this is. Their value drivers rank the work and their
     requirement fields are mandatory.
   - **Consulted personas** (zero or more): adjacent teams whose constraints the plan must honor.
     This is where cross-team alignment happens.
   - Or **Create your own**: run the `create-persona` skill, then return here.
3. Ask which initiative to run (folders in `initiatives/`).
4. Read every selected persona, `knowledge/company.md`, and all initiative files.
5. If a selected persona has unvetted sources, say so before continuing: the plan can be
   drafted, but citations resting on those sources will be flagged until the owner vets them.

## Step 1 — Intake → `01_intake.md` · **GATE 1**
Do not draft any plan yet. Produce only:

```
# Intake: <INIT-ID> · persona: <primary> · consulted: <ids, or none>

## Understanding
<3–5 sentences: the problem, who has it, and what "done" means, in the primary persona's terms>

## Questions
- <persona Q-ID> [blocking|non-blocking]: <question> | answer:
- Q-01 [blocking|non-blocking]: <your question> | answer:

## Assumptions
- A-01: <assumption> | basis: <IDs, or "none — inferred"> | status: UNVERIFIED
```

Rules:
- Ask **every** `Always ask` question from the primary and consulted personas, by its persona ID.
  If the inputs already answer it, fill the answer and cite the ID that answers it.
- Mark a question **blocking** if a wrong guess would change scope, safety, regulatory path or a
  non-negotiable. Everything else is non-blocking.
- Every design element left "not yet decided" becomes a question.
- Prefer one sharp question over three vague ones.

Then run `python checks/checks.py intake <file>`, fix anything it reports, and **stop**. Show the
user the blocking questions and unverified assumptions and ask them to answer in the file or in
chat. When they answer, write the answers into the file, set assumption status to CONFIRMED or
REJECTED, and re-run the check. Continue only when it passes.

## Step 2 — Milestones → `02_milestones.md` · **GATE 2**
Propose milestones (definition `K-1`, calendar `K-4`) before any detailed work:

```
### MS-1 — <user-visible outcome>
- Window: <release, sprints>
- Goal: <what a named user can do at the end>
- Value drivers: <VD-IDs from the primary persona, highest-ranked first>
- Covers: <F- and D- IDs>
- Out of scope: <what is deliberately left for later>
- Why this order: <one line tied to value driver rank, risk or dependency>
```

Order milestones by the primary persona's value driver ranking, then by risk and dependency.
Show the user and **stop** for approval or changes. Fixing scope here is cheap.

## Step 3 — Plan → `03_plan.md`
Write the full plan in exactly this structure:

```
# Delivery plan: <INIT-ID> · persona: <primary> · consulted: <ids, or none>

## Milestones
### MS-1 — <title>
- Window: ...
- Goal: ...
- Value drivers: ...
- Out of scope: ...

## Customer value deliveries
### CVD-01 · MS-1 · <title>
- User: <U-ID from a selected persona>
- User need: As a <user>, I need <capability> so that <outcome>.
- Value driver: <one VD-ID>
- Traces to: <F- and D- IDs>
- Evidence: "<verbatim quote>" [source: <feedback file>]
- Requirements: <REQ-IDs>
- Acceptance criteria:
  - AC-1: Given <context>, when <action>, then <observable, measurable result>.

## Requirements
### REQ-01 · <title>
- Text: The system shall <one behavior, with numbers not adjectives>.
- Derived from: <F-, D-, DC-, C- IDs>
- <every field listed under the primary persona's "Requirement fields">: <value>

## Cross-team alignment
- <C-ID>: addressed by <REQ-IDs> — <how>
- <C-ID>: CONFLICT — <what conflicts, the options, who decides>
- <C-ID>: not applicable — <why>

## Deferred
- <F- or D-ID>: deferred — <reason and target release>

## Assumptions
- A-01: <assumption> | basis: <IDs> | status: <UNVERIFIED|CONFIRMED>

## Open questions
- Q-01 [non-blocking]: <question>

## Decision log
- DEC-01: <decision> | why: <reason> | sources: <IDs>
```

Rules:
1. Every finding (`F-`) is covered by a CVD or explicitly deferred. Every design element (`D-`) is
   covered by a requirement or explicitly deferred.
2. Every CVD has exactly one milestone, one user, one value driver, at least one requirement and
   at least one Given / when / then acceptance criterion a QA engineer can test without asking.
3. Every requirement is one "shall" behavior (`K-8`) and carries every field the primary persona requires.
4. Every non-negotiable constraint of the primary **and** consulted personas appears in
   Cross-team alignment. Never weaken one to make the plan fit. If a design element conflicts
   with a constraint, write CONFLICT and name the decision owner. Do not resolve it yourself.
5. No banned terms (company and persona lists) in requirements or acceptance criteria. If an input
   is vague, propose a number, mark it `[PROPOSED]` (`K-9`), and add an assumption.
6. Confirmed answers from Gate 1 are inputs: cite the question ID in the Decision log.
7. When a consulted persona's view changes a CVD or requirement, say so in the Decision log.

## Step 4 — Check, then hand to humans
1. Run `python checks/checks.py plan <file>`. If it fails, fix the plan and re-run, at most twice.
   If it still fails, stop and show the user what is failing and why. Do not hide failures.
2. Run `python checks/checks.py trace <file>` to export the traceability matrix.
3. Run `python checks/checks.py provenance <file>` to show which vetted sources the plan rests on.
4. Run `python checks/review.py start <file>` to create the review log.
5. Tell the user, in this order: the review queue from the check (assumptions, conflicts,
   proposed values, deferrals, unvetted sources), how the persona shaped the plan (value drivers
   per milestone), and who must sign off (the `Sign-offs` of each selected persona).

Nothing enters the backlog until `python checks/review.py status <review.csv>` passes.
