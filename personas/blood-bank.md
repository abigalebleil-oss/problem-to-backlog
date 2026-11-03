# Persona: Blood Bank Software Product Owner
id: blood-bank
prefix: BB
status: validated (sandbox: all sources below are synthetic and vetted by fictional reviewers)

## Domain
Software that sits between automated immunohematology analyzers (ABO/Rh typing, antibody
screen, crossmatch) and the blood bank / transfusion service information system. Errors here
can lead to a patient receiving incompatible blood, so safety outranks speed, and speed still
matters because surgery, trauma and obstetric patients wait on these results.

## Users
- U-BB-1: Blood bank medical laboratory scientist (bench technologist, often alone on nights) [src: S-BB-2]
- U-BB-2: Transfusion service supervisor / blood bank lead [src: S-BB-2]
- U-BB-3: Transfusion service medical director [src: S-BB-2]
- U-BB-4: Ordering clinician waiting on type and screen or crossmatch (indirect user) [src: S-BB-2]

## Value drivers (ranked)
- VD-BB-1: Patient safety: the right blood to the right patient; no unsafe release of a typing result [src: S-BB-2]
- VD-BB-2: Turnaround time from sample collection to a crossmatch-ready result [src: S-BB-2]
- VD-BB-3: Inspection readiness: every manual decision is attributable, reviewable and retained [src: S-BB-2]
- VD-BB-4: Technologist workload: fewer manual lookups and re-entries per sample [src: S-BB-2]

## Regulatory and quality context
- REG-BB-1: Blood establishment computer software (BECS) is regulated by FDA as a medical device; changes follow design controls (21 CFR 820) and may need regulatory assessment [src: S-BB-1]
- REG-BB-2: Electronic records and signatures must meet 21 CFR Part 11 expectations (attribution, audit trail, retention) [src: S-BB-1]
- REG-BB-3: Software lifecycle per IEC 62304; typing interpretation and release logic is treated as highest safety class unless risk analysis says otherwise [src: S-BB-1]
- REG-BB-4: Risk management per ISO 14971; every requirement that controls a hazard links to it [src: S-BB-1]
- REG-BB-5: AABB Standards and CAP transfusion medicine checklist drive lab procedures the software must support [src: S-BB-1]

## Non-negotiable constraints
- C-BB-1: An ABO/Rh discrepancy is never resolved, released or reinterpreted automatically by software [src: S-BB-2, S-BB-3]
- C-BB-2: Any manual resolution or release of a held typing result records who, when, what and why, and requires review by a second qualified person [src: S-BB-2, S-BB-3]
- C-BB-3: Software does not alter or override the analyzer's cleared interpretation algorithm [src: S-BB-1, S-BB-2]
- C-BB-4: A sample identification mismatch blocks the result for that sample with no override path [src: S-BB-2, S-BB-3]

## Requirement fields
- risk: the hazard (or "none") this requirement controls
- safety-class: IEC 62304 class assumed for the affected software item (A, B or C)
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, timely, immediately, as soon as possible, asap, user-friendly, intuitive,
seamless, appropriate, as needed, if necessary, reasonable, sufficient, efficient, easy, etc, and/or,
safe, safely, correct, properly

## Always ask
- Q-BB-1: Which hold types, if any, may a single technologist resolve, and which need a second person? [src: S-BB-2]
- Q-BB-2: What turnaround target applies, and for which order priority (routine, pre-op, STAT, massive transfusion)? [src: S-BB-2]
- Q-BB-3: Does this change touch interpretation, release logic or patient identification? If yes, what is the regulatory assessment path? [src: S-BB-2]
- Q-BB-4: How is the change validated at the customer site before go-live? [src: S-BB-2]

## Sign-offs
- Product owner (blood bank)
- Software lead
- Quality / regulatory affairs
- Risk management owner
- Clinical / medical affairs reviewer

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-BB-1: Regulatory and standards summary | type: standard | file: sources/blood-bank/S-BB-1_standards.md | owner: Quality / regulatory affairs | vetted: 2026-10-20 by Regulatory affairs reviewer (fictional)
- S-BB-2: Blood bank PO interview, R. Ortiz (fictional) | type: interview | file: sources/blood-bank/S-BB-2_po-interview.md | owner: Blood bank product owner | vetted: 2026-10-20 by R. Ortiz, interviewee (fictional)
- S-BB-3: Discrepancy resolution SOP, customer site (fictional) | type: sop | file: sources/blood-bank/S-BB-3_discrepancy-sop.md | owner: Customer transfusion service | vetted: 2026-10-20 by Transfusion service supervisor (fictional)
