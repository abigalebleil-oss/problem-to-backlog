<!-- Reference output of Step 3 for the SAME initiative with the middleware persona as primary,
     consulting the clinical analyzer persona. Compare with examples/INIT-001/clinical-analyzer/03_plan.md:
     same inputs, different ranking, scope and required fields.
     Drafted by Claude to illustrate the format; regenerate it live with the skill and compare. -->

# Delivery plan: INIT-001 · persona: middleware-reporting · consulted: clinical-analyzer

## Milestones

### MS-1 — The LIS and the worklist both know a sample is held, and why
- Window: Release 2027.1, sprints 1–3
- Goal: every hold carries a machine-readable category; opted-in LIS interfaces receive a standard in-process status with the reason; nothing changes for sites that do not opt in.
- Value drivers: VD-MW-1, VD-MW-3, VD-MW-5
- Out of scope: alerts and the resolution workflow.

### MS-2 — The bench is alerted, and holds clear on the record
- Window: Release 2027.1, sprints 3–4
- Goal: technologists see a hold within 60 seconds, discrepancies need a second qualified reviewer, and wrong-sample results cannot be released.
- Value drivers: VD-MW-5
- Out of scope: user and role management (host system).

### MS-3 — Every held and final message traces to the instrument message
- Window: Release 2027.1, sprint 5
- Goal: a field engineer can follow any order from the inbound instrument message to every outbound message it produced, and validate the new message with the field kit.
- Value drivers: VD-MW-2, VD-MW-4
- Out of scope: sites beyond the pilot.

## Customer value deliveries

### CVD-01 · MS-1 · Each hold carries a machine-readable category
- User: U-MW-2
- User need: As a bench technologist working the middleware worklist, I need each held sample to show its hold category so that I know what to do without opening the analyzer software.
- Value driver: VD-MW-5
- Traces to: F-01, F-02, D-1, D-2
- Evidence: "the middleware worklist just says HOLD" [source: 01_night_typing_tech.md]
- Requirements: REQ-01, REQ-02, REQ-10
- Acceptance criteria:
  - AC-1: Given the analyzer flags a forward-reverse ABO discrepancy, when TypeBridge receives the result, then it is held with category "abo_rh_discrepancy" and the analyzer flag text is stored unchanged.
  - AC-2: Given a held sample, when the worklist is open, then the hold panel shows category, analyzer flag text and minutes held.
  - AC-3: Given a sample held as reagent_qc_not_valid, when acceptable QC is recorded but the sample is not rerun, then the sample remains held.

### CVD-02 · MS-1 · The LIS sees held, not missing
- User: U-MW-1
- User need: As an LIS administrator, I need held results to reach the LIS as in process with a reason so that nursing can see a sample is being worked.
- Value driver: VD-MW-1
- Traces to: F-07, F-04, D-6
- Evidence: "a held type and screen just sits as pending." [source: 03_lis_admin.md]
- Requirements: REQ-03
- Acceptance criteria:
  - AC-1: Given held-status messaging is enabled for an interface, when a sample is held, then TypeBridge sends an HL7 v2.5 ORU^R01 with OBX-11 = "I" and the hold category in an NTE segment.
  - AC-2: Given any held-status message, when it is validated against the HL7 v2.5 segment list, then it contains no Z-segments.

### CVD-03 · MS-1 · An upgrade changes nothing until the site turns it on
- User: U-MW-1
- User need: As an LIS administrator, I need the new message to be off until I enable it so that an upgrade never changes what my LIS receives overnight.
- Value driver: VD-MW-3
- Traces to: D-6
- Evidence: "I can't have an upgrade change what the LIS receives overnight." [source: 03_lis_admin.md]
- Requirements: REQ-04
- Acceptance criteria:
  - AC-1: Given a site upgraded to this release, when a sample is held on an interface that has not been enabled, then the outbound messages are byte-identical to the previous release.
  - AC-2: Given an administrator enables held-status messaging on one interface, when a sample is held, then only that interface receives the held-status message.

### CVD-04 · MS-2 · The bench learns about a hold within a minute
- User: U-MW-2
- User need: As a bench technologist, I need to be told when a sample is held so that I hear about it before a clinical unit calls.
- Value driver: VD-MW-5
- Traces to: F-03, D-3
- Evidence: "I don't even know the sample is held yet." [source: 01_night_typing_tech.md]
- Requirements: REQ-05
- Acceptance criteria:
  - AC-1: Given a technologist logged into the worklist, when a sample is held, then a banner shows the sample ID and hold category within 60 seconds.

### CVD-05 · MS-2 · Discrepancies are resolved by two qualified people, on the record
- User: U-CA-2
- User need: As a blood typing lab supervisor, I need every discrepancy resolution reviewed by a second qualified person and recorded so that I can show an inspector who released it and why.
- Value driver: VD-CA-1
- Traces to: F-05, F-06, D-5
- Evidence: "Discrepancy resolution should always get a second set of eyes." [source: 02_lab_supervisor.md]
- Requirements: REQ-06, REQ-07, REQ-08
- Acceptance criteria:
  - AC-1: Given a resolution recorded by technologist A, when technologist A tries to approve it, then TypeBridge refuses.
  - AC-2: Given a resolution recorded by technologist A, when a different user whose host-system role includes blood typing qualification approves it, then the result is released and both steps appear in the audit log with user ID, timestamp and reason.
  - AC-3: Given an abo_rh_discrepancy hold, when no user acts on it for 24 hours, then its hold status is unchanged.
  - AC-4: Given a sample_id_mismatch hold, when any user attempts a release, then TypeBridge refuses and writes the attempt to the audit log.

### CVD-06 · MS-3 · Every message traces to the instrument message that caused it
- User: U-MW-3
- User need: As a field service engineer, I need every held-status and final message to carry a reference to the inbound instrument message so that I can trace any order end to end during interface validation.
- Value driver: VD-MW-2
- Traces to: D-6
- Requirements: REQ-09
- Acceptance criteria:
  - AC-1: Given an inbound ASTM message that produces a held-status message and later a final result, when both are sent, then both carry the inbound message control ID and the message log links all three.
  - AC-2: Given the field validation kit, when the held-status script runs against a pilot interface, then it reports pass or fail for each expected segment.

## Requirements

### REQ-01 · Hold category
- Text: The system shall assign each held result exactly one hold category from abo_rh_discrepancy, weak_or_mixed_field, reagent_qc_not_valid or sample_id_mismatch, and shall store the analyzer flag text unchanged.
- Derived from: D-1, F-01, DC-2
- interface-impact: none
- backward-compatible: yes
- verification: test

### REQ-02 · Worklist hold panel
- Text: The worklist shall display the hold category, analyzer flag text and minutes since the hold for every held result.
- Derived from: D-2, F-01, F-02
- interface-impact: none
- backward-compatible: yes
- verification: test

### REQ-03 · Held status to LIS
- Text: When held-status messaging is enabled for an interface, the system shall send an HL7 v2.5 ORU^R01 with OBX-11 set to "I" and the hold category in an NTE segment for each held result.
- Derived from: D-6, F-07, C-MW-1, DC-3
- interface-impact: outbound, ORU^R01
- backward-compatible: yes, only when enabled
- verification: test

### REQ-04 · Opt-in per interface
- Text: The system shall send no held-status message on an interface until an administrator enables held-status messaging for that interface.
- Derived from: D-6, C-MW-2
- interface-impact: outbound, ORU^R01
- backward-compatible: yes
- verification: test

### REQ-05 · Hold alert
- Text: The worklist shall display a banner with the sample ID and hold category to every user logged into the worklist within 60 seconds of a hold.
- Derived from: D-3, F-03
- interface-impact: none
- backward-compatible: yes
- verification: test

### REQ-06 · Two-person discrepancy resolution
- Text: The system shall release a result held as abo_rh_discrepancy only after one user records a resolution with a non-empty reason and a different user whose host-system role includes blood typing qualification approves it.
- Derived from: D-5, F-06, C-CA-2, DC-1
- interface-impact: none
- backward-compatible: yes
- verification: test

### REQ-07 · No automatic discrepancy resolution and audit record
- Text: The system shall not change the hold status of an abo_rh_discrepancy result without a recorded user action, and shall write each resolution and review to the audit log with user ID, timestamp and reason.
- Derived from: C-CA-1, D-5, F-05
- interface-impact: none
- backward-compatible: yes
- verification: test

### REQ-08 · Sample ID mismatch block
- Text: The system shall offer no release action for a result held as sample_id_mismatch and shall record every attempted release in the audit log.
- Derived from: D-1, C-CA-4
- interface-impact: none
- backward-compatible: yes
- verification: test

### REQ-09 · End-to-end message traceability
- Text: The system shall include the inbound instrument message control ID in every held-status and final result message produced from that inbound message.
- Derived from: D-6, C-MW-3
- interface-impact: outbound, ORU^R01
- backward-compatible: yes, existing fields only
- verification: test

### REQ-10 · QC hold clears only after QC and rerun
- Text: The system shall keep a result held as reagent_qc_not_valid until acceptable reagent QC is recorded and the sample is rerun.
- Derived from: D-1, C-MW-5
- interface-impact: none
- backward-compatible: yes
- verification: test

## Cross-team alignment
- C-MW-1: addressed by REQ-03 — standard v2.5 OBX and NTE only
- C-MW-2: addressed by REQ-04 — off by default, enabled per interface
- C-MW-3: addressed by REQ-09 — inbound message control ID carried on every outbound message
- C-MW-4: addressed by REQ-06 — qualification comes from the host system role (DC-1)
- C-CA-1: addressed by REQ-07 — no status change without a recorded user action
- C-CA-2: addressed by REQ-06, REQ-07 — second qualified reviewer and audit record
- C-CA-3: addressed by REQ-01 — analyzer flag stored unchanged
- C-CA-4: addressed by REQ-08 — no release path for sample ID mismatch
- C-MW-5: addressed by REQ-10 — QC holds clear only after acceptable QC and rerun
- C-MW-6: not applicable — TypeBridge does not configure QC rules
- C-MW-7: CONFLICT — deferring D-7 to 2027.2 means a QC failure is not linked to affected samples in TypeBridge this release. Options: keep D-7 in 2027.1 and drop MS-3, or rely on the lab's QC system for lookback. Decision owners: clinical analyzer PO and middleware PO.

## Deferred
- D-4: deferred — reagent QC expiry warning overlaps the QC software product; propose it lands there in 2027.2
- D-7: deferred — QC lookback list, same reason; see the C-MW-7 conflict
- F-08: deferred — addressed by D-4 in 2027.2
- F-09: deferred — addressed by D-7 in 2027.2

## Assumptions
- A-01: The four interviews represent the other pilot sites | basis: none — inferred | status: UNVERIFIED
- A-02: The host system can supply each user's role and blood typing qualification | basis: DC-1 | status: UNVERIFIED
- A-03: Pilot-site LIS systems display OBX-11 status "I" as in process | basis: D-6, DC-3 | status: UNVERIFIED
- A-04: The QC software team can take the expiry warning and lookback list in 2027.2 | basis: none — inferred | status: UNVERIFIED

## Open questions
- Q-MW-3 [non-blocking]: What message volume and peak rate must this handle at the largest site?

## Decision log
- DEC-01: LIS visibility ships in MS-1 | why: the persona ranks interoperability first and the LIS admin named it | sources: VD-MW-1, F-07
- DEC-02: QC expiry warning and lookback list deferred to 2027.2 | why: they belong closer to the QC product, and deferring keeps 2027.1 focused on interface behavior; raised as a conflict for the owners to decide | sources: VD-MW-1, C-MW-7, F-08, F-09
- DEC-03: Added end-to-end message traceability (REQ-09) | why: the middleware persona requires it; the design did not cover it | sources: C-MW-3, D-6
- DEC-04: Only abo_rh_discrepancy needs a second reviewer | why: PO answer at Gate 1 | sources: Q-CA-1, F-06
