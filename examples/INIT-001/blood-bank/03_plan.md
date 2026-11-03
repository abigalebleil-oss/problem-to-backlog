<!-- Reference output of Step 3 for the blood bank persona, consulting middleware and clinical QC.
     Drafted by Claude to illustrate the format; regenerate it live with the skill and compare.
     Passes the deterministic checks. Still needs every sign-off before it enters the backlog. -->

# Delivery plan: INIT-001 · persona: blood-bank · consulted: middleware-connectivity, clinical-qc

## Milestones

### MS-1 — Every held sample says why, and a wrong-sample result can never be released
- Window: Release 2027.1, sprints 1–2
- Goal: a technologist sees the hold category and analyzer flag for every held sample on the worklist, and a sample ID mismatch has no release path.
- Value drivers: VD-BB-1, VD-BB-2, VD-BB-4
- Out of scope: alerts, resolution workflow, anything sent to the LIS.

### MS-2 — Discrepancies are resolved by two qualified people, on the record
- Window: Release 2027.1, sprints 2–3
- Goal: an ABO/Rh discrepancy is released only after a second qualified reviewer approves, and a supervisor can show every resolution at inspection.
- Value drivers: VD-BB-1, VD-BB-3
- Out of scope: user and role management (provided by the host system).

### MS-3 — The bench hears about holds and QC lapses before the phone rings
- Window: Release 2027.1, sprints 3–4
- Goal: technologists see a hold within 60 seconds, the lab is warned before reagent QC expires, and a QC failure lists the samples to review.
- Value drivers: VD-BB-2, VD-BB-1
- Out of scope: STAT and massive transfusion handling.

### MS-4 — The LIS shows held, not missing
- Window: Release 2027.1, sprints 4–5
- Goal: sites that opt in see held type and screens as in process with the hold category in the LIS.
- Value drivers: VD-BB-2
- Out of scope: changes to the LIS itself; sites beyond the pilot.

## Customer value deliveries

### CVD-01 · MS-1 · Each hold carries a category the bench can act on
- User: U-BB-1
- User need: As a night-shift blood bank technologist, I need each held sample to show why it is held so that I can start the right workup without walking to the analyzer.
- Value driver: VD-BB-2
- Traces to: F-01, F-02, F-04, D-1, D-2
- Evidence: "the middleware worklist just says HOLD" [source: 01_night_bb_tech.md]
- Requirements: REQ-01, REQ-02
- Acceptance criteria:
  - AC-1: Given the analyzer flags a forward-reverse ABO discrepancy, when TypeBridge receives the result, then the sample is held with category "abo_rh_discrepancy" and the analyzer flag text is stored unchanged.
  - AC-2: Given a held sample, when a technologist opens the worklist, then the hold panel shows its category, analyzer flag text and minutes held without opening another screen.
  - AC-3: Given any held sample, when its category is set, then the analyzer interpretation stored for that sample is identical to the value received.

### CVD-02 · MS-1 · A sample ID mismatch has no release path
- User: U-BB-1
- User need: As a blood bank technologist, I need a result whose sample ID matches no open order to be blocked so that it can never be released to the wrong patient.
- Value driver: VD-BB-1
- Traces to: D-1
- Requirements: REQ-03
- Acceptance criteria:
  - AC-1: Given a result whose sample ID matches no open order, when TypeBridge receives it, then it is held as "sample_id_mismatch" and no release or resolution action is shown for it.
  - AC-2: Given a sample_id_mismatch hold, when any user attempts a release through the worklist or the API, then TypeBridge refuses and writes the attempt to the audit log.

### CVD-03 · MS-2 · Discrepancy resolution needs a second qualified reviewer
- User: U-BB-2
- User need: As a transfusion service supervisor, I need every discrepancy resolution reviewed by a second qualified person so that the software enforces the SOP we already follow.
- Value driver: VD-BB-1
- Traces to: F-05, F-06, D-5
- Evidence: "Discrepancy resolution should always get a second set of eyes." [source: 02_tx_supervisor.md]
- Requirements: REQ-04, REQ-05
- Acceptance criteria:
  - AC-1: Given an abo_rh_discrepancy hold, when technologist A records a resolution and reason, then the result stays held with status "awaiting review".
  - AC-2: Given a resolution recorded by technologist A, when technologist A tries to approve it, then TypeBridge refuses.
  - AC-3: Given a resolution recorded by technologist A, when a different user whose host-system role includes blood bank qualification approves it, then the result is released and both steps appear in the audit log with user ID, timestamp and reason.
  - AC-4: Given a resolution with an empty reason, when technologist A submits it, then TypeBridge rejects it.
  - AC-5: Given an abo_rh_discrepancy hold, when no user acts on it for 24 hours, then its hold status is unchanged.

### CVD-04 · MS-2 · A supervisor can show any resolution at inspection
- User: U-BB-2
- User need: As a transfusion service supervisor, I need a report of every resolution and review so that I can show an inspector who released each held result and why.
- Value driver: VD-BB-3
- Traces to: F-05, D-5
- Evidence: "At inspection I can't always show who reviewed it or why it was released." [source: 02_tx_supervisor.md]
- Requirements: REQ-06
- Acceptance criteria:
  - AC-1: Given a date range, when a supervisor runs the resolution report, then every released held result lists sample ID, hold category, resolver, reviewer, timestamps and reasons.
  - AC-2: Given an audit entry, when its content is changed outside TypeBridge, then the integrity check reports that entry as altered.

### CVD-05 · MS-3 · The bench learns about a hold within a minute
- User: U-BB-1
- User need: As a night-shift blood bank technologist, I need to be told when a sample is held so that I hear about it before the clinical unit calls.
- Value driver: VD-BB-2
- Traces to: F-03, F-04, D-3
- Evidence: "I don't even know the sample is held yet." [source: 01_night_bb_tech.md]
- Requirements: REQ-07
- Acceptance criteria:
  - AC-1: Given a technologist logged into the blood bank worklist, when a sample is held, then a banner shows the sample ID and hold category within 60 seconds.
  - AC-2: Given a hold banner, when the technologist acknowledges it, then the acknowledgement time and user ID are recorded.

### CVD-06 · MS-3 · A warning comes before reagent QC expires
- User: U-QC-2
- User need: As a lab QC coordinator, I need a warning before typing reagent QC expires so that day shift runs QC before results start holding.
- Value driver: VD-BB-2
- Traces to: F-08, D-4
- Evidence: "I need a warning before QC expires, not a pile of holds after." [source: 04_qc_coordinator.md]
- Requirements: REQ-08, REQ-12
- Acceptance criteria:
  - AC-1: Given reagent QC for a typing reagent expires at 07:00 and no new acceptable QC is recorded, when the time reaches 06:00, then the worklist shows a warning naming the reagent and its expiry time.
  - AC-2: Given the same reagent, when the time reaches 06:45, then a second warning is shown.
  - AC-3: Given acceptable QC was recorded at 05:50, when the time reaches 06:00, then no warning is shown.
  - AC-4: Given a sample held as reagent_qc_not_valid, when acceptable QC is recorded but the sample is not rerun, then the sample remains held.

### CVD-07 · MS-3 · A QC failure lists the samples to review
- User: U-QC-2
- User need: As a lab QC coordinator, I need the list of patient samples tested since the last acceptable QC so that the lab can review every result the failure may have affected.
- Value driver: VD-BB-1
- Traces to: F-09, D-7
- Evidence: "which patient samples were run since the last good QC" [source: 04_qc_coordinator.md]
- Requirements: REQ-09
- Acceptance criteria:
  - AC-1: Given a QC failure recorded for a typing reagent, when the QC coordinator opens the lookback list, then it shows every patient sample tested with that reagent since its last acceptable QC, with sample ID, test time and result status.
  - AC-2: Given a lookback list, when it is exported, then the CSV file contains the same rows as the screen.

### CVD-08 · MS-4 · The LIS shows held and why
- User: U-MW-1
- User need: As an LIS administrator, I need held type and screens to reach the LIS as in process with a reason so that nursing can tell a sample is being worked.
- Value driver: VD-BB-2
- Traces to: F-07, D-6
- Evidence: "a held type and screen just sits as pending." [source: 03_lis_admin.md]
- Requirements: REQ-10, REQ-11
- Acceptance criteria:
  - AC-1: Given held-status messaging is enabled for an interface, when a sample is held, then TypeBridge sends an HL7 v2.5 ORU^R01 with OBX-11 = "I" and the hold category in an NTE segment.
  - AC-2: Given held-status messaging is not enabled for an interface, when a sample is held, then the outbound messages on that interface are identical to the current release.
  - AC-3: Given any held-status message, when it is validated against the HL7 v2.5 segment list, then it contains no Z-segments.

## Requirements

### REQ-01 · Hold category
- Text: The system shall assign each held result exactly one hold category from abo_rh_discrepancy, weak_or_mixed_field, reagent_qc_not_valid or sample_id_mismatch, and shall store the analyzer flag text unchanged.
- Derived from: D-1, F-01, DC-2
- risk: Wrong or missing category sends the technologist down the wrong resolution path
- safety-class: C
- verification: test

### REQ-02 · Worklist hold panel
- Text: The worklist shall display the hold category, analyzer flag text and minutes since the hold for every held result, refreshed at least every [PROPOSED] 60 seconds.
- Derived from: D-2, F-01, F-02
- risk: none
- safety-class: B
- verification: test

### REQ-03 · Sample ID mismatch block
- Text: The system shall offer no release or resolution action for a result held as sample_id_mismatch and shall record every attempted release in the audit log.
- Derived from: D-1, C-BB-4
- risk: A result is released against the wrong patient record
- safety-class: C
- verification: test

### REQ-04 · Two-person discrepancy resolution
- Text: The system shall release a result held as abo_rh_discrepancy only after one user records a resolution with a non-empty reason and a different user whose host-system role includes blood bank qualification approves it.
- Derived from: D-5, F-06, C-BB-2, DC-1
- risk: An incorrectly resolved discrepancy is released for transfusion
- safety-class: C
- verification: test

### REQ-05 · No automatic discrepancy resolution
- Text: The system shall not change the hold status of an abo_rh_discrepancy result without a recorded user action.
- Derived from: C-BB-1, DC-2
- risk: A discrepancy is cleared by software without human review
- safety-class: C
- verification: test

### REQ-06 · Resolution audit record and report
- Text: The system shall write each resolution and review to the append-only audit log with user ID, timestamp, hold category and reason, and shall report these entries for a selected date range.
- Derived from: D-5, F-05, REG-BB-2
- risk: A manual release cannot be attributed during inspection
- safety-class: B
- verification: test

### REQ-07 · Hold alert
- Text: The worklist shall display a banner with the sample ID and hold category to every user logged into the blood bank worklist within 60 seconds of a hold.
- Derived from: D-3, F-03
- risk: A hold goes unnoticed and delays blood for a waiting patient
- safety-class: B
- verification: test

### REQ-08 · Reagent QC expiry warning
- Text: The worklist shall display a warning naming the reagent and expiry time 60 minutes and again 15 minutes before typing reagent QC expires, unless acceptable QC has been recorded since.
- Derived from: D-4, F-08
- risk: An unnoticed QC lapse holds every typing result at shift change
- safety-class: B
- verification: test

### REQ-09 · QC lookback list
- Text: When a QC failure is recorded for a typing reagent, the system shall list every patient result tested with that reagent since its last acceptable QC.
- Derived from: D-7, F-09, C-QC-3
- risk: Patient results affected by failed QC are not reviewed
- safety-class: B
- verification: test

### REQ-10 · Held status to LIS
- Text: When held-status messaging is enabled for an interface, the system shall send an HL7 v2.5 ORU^R01 with OBX-11 set to "I" and the hold category in an NTE segment for each held result.
- Derived from: D-6, F-07, C-MW-1, DC-3
- risk: The LIS shows a held result as final
- safety-class: B
- verification: test

### REQ-11 · Held-status messaging is opt-in
- Text: The system shall send no held-status message on an interface until an administrator enables held-status messaging for that interface.
- Derived from: D-6, C-MW-2
- risk: An upgrade changes what the LIS receives without the site agreeing
- safety-class: B
- verification: test

### REQ-12 · QC hold clears only after QC and rerun
- Text: The system shall keep a result held as reagent_qc_not_valid until acceptable reagent QC is recorded and the sample is rerun.
- Derived from: D-1, C-QC-1
- risk: A result tested with invalid reagent QC is released
- safety-class: C
- verification: test

## Cross-team alignment
- C-BB-1: addressed by REQ-05 — no status change without a recorded user action
- C-BB-2: addressed by REQ-04, REQ-06 — second qualified reviewer and full audit record
- C-BB-3: addressed by REQ-01 — analyzer flag stored unchanged; TypeBridge never reinterprets
- C-BB-4: addressed by REQ-03 — no release path for sample ID mismatch
- C-MW-1: addressed by REQ-10 — standard v2.5 OBX and NTE only
- C-MW-2: addressed by REQ-11 — off by default, enabled per interface
- C-MW-3: CONFLICT — D-6 sends a held-status message and later a final result for the same order; the design does not say how both trace back to the inbound instrument message. Options: reuse the inbound message control ID, or a new ID with a reference to it. Decision owner: integration lead.
- C-MW-4: addressed by REQ-04 — qualification comes from the host system role (DC-1)
- C-QC-1: addressed by REQ-12 — QC holds clear only after acceptable QC and rerun
- C-QC-2: not applicable — TypeBridge does not configure QC rules; they live in the lab's QC system (Q-QC-1)
- C-QC-3: addressed by REQ-09 — lookback list links the QC failure to affected samples

## Deferred
- None.

## Assumptions
- A-01: The four interviews represent the other pilot sites | basis: none — inferred | status: UNVERIFIED
- A-02: The host system can supply each user's role and blood bank qualification to TypeBridge | basis: DC-1 | status: UNVERIFIED
- A-03: Pilot-site LIS systems display OBX-11 status "I" as in process | basis: D-6, DC-3 | status: UNVERIFIED
- A-04: Hold lookup time is a large enough share of turnaround that removing it moves the pre-op target | basis: F-02, F-04 | status: UNVERIFIED
- A-05: A 60-second panel refresh is acceptable to technologists | basis: none — proposed to make D-2 testable | status: UNVERIFIED
- A-06: Four milestones fit in sprints 1–5 with one team | basis: K-4, K-5 | status: UNVERIFIED

## Open questions
- Q-BB-4 [non-blocking]: How is the change validated at the customer site before go-live?
- Q-MW-3 [non-blocking]: What message volume and peak rate must this handle at the largest site?

## Decision log
- DEC-01: Hold categories and the sample ID mismatch block ship first (MS-1) | why: the persona ranks patient safety first and every later milestone depends on categories | sources: VD-BB-1, C-BB-4, D-1
- DEC-02: Only abo_rh_discrepancy needs a second reviewer; other holds clear by one qualified technologist after rerun | why: PO answer at Gate 1 | sources: Q-BB-1, F-06
- DEC-03: QC expiry warning and lookback list stay in 2027.1 | why: both protect patients and turnaround, the two top-ranked drivers | sources: VD-BB-1, VD-BB-2, F-08, F-09
- DEC-04: LIS held-status messaging is opt-in and ships last (MS-4) | why: consulted middleware constraint and the lowest safety impact of the four milestones | sources: C-MW-2, Q-MW-2
- DEC-05: STAT and massive transfusion are out of scope | why: PO answer at Gate 1 | sources: Q-BB-2
