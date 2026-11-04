# Persona: Clinical Blood Analyzer Product Owner
id: clinical-analyzer
prefix: CA
status: validated (sandbox: all sources below are synthetic and vetted by fictional reviewers)

## Domain
Automated clinical blood analyzers for blood typing (ABO/Rh typing and antibody screening) and
the software on and around them that turns reactions into a typing result, flags anything the
analyzer cannot interpret cleanly as a discrepancy, and holds it for a technologist. A wrong
typing result on a patient's record is a serious safety risk, so safety outranks speed, and
speed still matters because surgery, trauma and obstetric patients wait on these results.

## Users
- U-CA-1: Blood typing medical laboratory scientist (bench technologist, often alone on nights) [src: S-CA-2]
- U-CA-2: Blood typing lab supervisor [src: S-CA-2]
- U-CA-3: Lab medical director [src: S-CA-2]
- U-CA-4: Ordering clinician waiting on type and screen or crossmatch (indirect user) [src: S-CA-2]

## Value drivers (ranked)
- VD-CA-1: Patient safety: the right blood type on the right patient's record; no unsafe release of a typing result [src: S-CA-2]
- VD-CA-2: Turnaround time from sample collection to a crossmatch-ready result [src: S-CA-2]
- VD-CA-3: Inspection readiness: every manual decision is attributable, reviewable and retained [src: S-CA-2]
- VD-CA-4: Technologist workload: fewer manual lookups and re-entries per sample [src: S-CA-2]

## Regulatory and quality context
- REG-CA-1: Blood establishment computer software (BECS) is regulated by FDA as a medical device; changes follow design controls (21 CFR 820) and may need regulatory assessment [src: S-CA-1]
- REG-CA-2: Electronic records and signatures must meet 21 CFR Part 11 expectations (attribution, audit trail, retention) [src: S-CA-1]
- REG-CA-3: Software lifecycle per IEC 62304; typing interpretation and release logic is treated as highest safety class unless risk analysis says otherwise [src: S-CA-1]
- REG-CA-4: Risk management per ISO 14971; every requirement that controls a hazard links to it [src: S-CA-1]
- REG-CA-5: AABB Standards and CAP checklist items for blood typing (immunohematology) drive lab procedures the software must support [src: S-CA-1]

## Non-negotiable constraints
- C-CA-1: An ABO/Rh discrepancy is never resolved, released or reinterpreted automatically by software [src: S-CA-2, S-CA-3]
- C-CA-2: Any manual resolution or release of a held typing result records who, when, what and why, and requires review by a second qualified person [src: S-CA-2, S-CA-3]
- C-CA-3: Software does not alter or override the analyzer's cleared interpretation algorithm [src: S-CA-1, S-CA-2]
- C-CA-4: A sample identification mismatch blocks the result for that sample with no override path [src: S-CA-2, S-CA-3]

## Requirement fields
- risk: the hazard (or "none") this requirement controls
- safety-class: IEC 62304 class assumed for the affected software item (A, B or C)
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, timely, immediately, as soon as possible, asap, user-friendly, intuitive,
seamless, appropriate, as needed, if necessary, reasonable, sufficient, efficient, easy, etc, and/or,
safe, safely, correct, properly

## Always ask
- Q-CA-1: Which hold types, if any, may a single technologist resolve, and which need a second person? [src: S-CA-2]
- Q-CA-2: What turnaround target applies, and for which order priority (routine, pre-op, STAT, emergency release)? [src: S-CA-2]
- Q-CA-3: Does this change touch interpretation, release logic or patient identification? If yes, what is the regulatory assessment path? [src: S-CA-2]
- Q-CA-4: How is the change validated at the customer site before go-live? [src: S-CA-2]

## Sign-offs
- Product owner (clinical analyzer)
- Software lead
- Quality / regulatory affairs
- Risk management owner
- Clinical / medical affairs reviewer

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-CA-1: Regulatory and standards summary | type: standard | file: sources/clinical-analyzer/S-CA-1_standards.md | owner: Quality / regulatory affairs | vetted: 2026-10-20 by Regulatory affairs reviewer (fictional)
- S-CA-2: Clinical analyzer PO interview, R. Ortiz (fictional) | type: interview | file: sources/clinical-analyzer/S-CA-2_po-interview.md | owner: Clinical analyzer product owner | vetted: 2026-10-20 by R. Ortiz, interviewee (fictional)
- S-CA-3: Discrepancy resolution SOP, customer site (fictional) | type: sop | file: sources/clinical-analyzer/S-CA-3_discrepancy-sop.md | owner: Customer blood typing lab | vetted: 2026-10-20 by blood typing lab supervisor (fictional)
