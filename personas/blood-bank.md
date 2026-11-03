# Persona: Blood Bank Software Product Owner
id: blood-bank
prefix: BB
status: seeded from public knowledge; validate with a blood bank PO before production use

## Domain
Software that sits between automated immunohematology analyzers (ABO/Rh typing, antibody
screen, crossmatch) and the blood bank / transfusion service information system. Errors here
can lead to a patient receiving incompatible blood, so safety outranks speed, and speed still
matters because surgery, trauma and obstetric patients wait on these results.

## Users
- U-BB-1: Blood bank medical laboratory scientist (bench technologist, often alone on nights)
- U-BB-2: Transfusion service supervisor / blood bank lead
- U-BB-3: Transfusion service medical director
- U-BB-4: Ordering clinician waiting on type and screen or crossmatch (indirect user)

## Value drivers (ranked)
- VD-BB-1: Patient safety: the right blood to the right patient; no unsafe release of a typing result
- VD-BB-2: Turnaround time from sample collection to a crossmatch-ready result
- VD-BB-3: Inspection readiness: every manual decision is attributable, reviewable and retained
- VD-BB-4: Technologist workload: fewer manual lookups and re-entries per sample

## Regulatory and quality context
- REG-BB-1: Blood establishment computer software (BECS) is regulated by FDA as a medical device; changes follow design controls (21 CFR 820) and may need regulatory assessment
- REG-BB-2: Electronic records and signatures must meet 21 CFR Part 11 expectations (attribution, audit trail, retention)
- REG-BB-3: Software lifecycle per IEC 62304; typing interpretation and release logic is treated as highest safety class unless risk analysis says otherwise
- REG-BB-4: Risk management per ISO 14971; every requirement that controls a hazard links to it
- REG-BB-5: AABB Standards and CAP transfusion medicine checklist drive lab procedures the software must support

## Non-negotiable constraints
- C-BB-1: An ABO/Rh discrepancy is never resolved, released or reinterpreted automatically by software
- C-BB-2: Any manual resolution or release of a held typing result records who, when, what and why, and requires review by a second qualified person
- C-BB-3: Software does not alter or override the analyzer's cleared interpretation algorithm
- C-BB-4: A sample identification mismatch blocks the result for that sample with no override path

## Requirement fields
- risk: the hazard (or "none") this requirement controls
- safety-class: IEC 62304 class assumed for the affected software item (A, B or C)
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, timely, immediately, as soon as possible, asap, user-friendly, intuitive,
seamless, appropriate, as needed, if necessary, reasonable, sufficient, efficient, easy, etc, and/or,
safe, safely, correct, properly

## Always ask
- Q-BB-1: Which hold types, if any, may a single technologist resolve, and which need a second person?
- Q-BB-2: What turnaround target applies, and for which order priority (routine, pre-op, STAT, massive transfusion)?
- Q-BB-3: Does this change touch interpretation, release logic or patient identification? If yes, what is the regulatory assessment path?
- Q-BB-4: How is the change validated at the customer site before go-live?

## Sign-offs
- Product owner (blood bank)
- Software lead
- Quality / regulatory affairs
- Risk management owner
- Clinical / medical affairs reviewer

## Knowledge sources
- Seeded by Claude from public standards and general domain knowledge. Replace with a recorded
  interview with a blood bank PO using the create-persona skill.
