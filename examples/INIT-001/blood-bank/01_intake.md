<!-- Reference output of Step 1 (intake) after the PO answered the blocking questions.
     Drafted by Claude to illustrate the format; regenerate it live with the skill and compare.
     All answers are fictional. -->

# Intake: INIT-001 · persona: blood-bank · consulted: middleware-connectivity, clinical-qc

## Understanding
When the typing analyzer holds a type and screen, nobody at the bench, in the LIS or at
inspection can see why or who resolved it. For a blood bank, success means every hold is
visible with its reason within a minute, discrepancies are never released without a second
qualified reviewer, and the lab moves closer to its 60-minute pre-op crossmatch-ready target
without weakening any safety rule.

## Questions
- Q-BB-1 [blocking]: Which hold types may a single technologist resolve, and which need a second person? | answer: Only abo_rh_discrepancy needs a second qualified reviewer. weak_or_mixed_field and reagent_qc_not_valid clear by one qualified technologist after rerun. sample_id_mismatch is never released; a new sample is required (C-BB-4).
- Q-BB-2 [blocking]: What turnaround target applies, and for which order priority? | answer: 60 minutes from receipt to crossmatch-ready for pre-op (F-04). STAT and massive transfusion are out of scope for this initiative.
- Q-BB-3 [blocking]: Does this change touch interpretation, release logic or patient identification? | answer: Release logic yes (D-5) and identification yes (sample_id_mismatch). Interpretation no (DC-2). Regulatory affairs to assess as a design change.
- Q-BB-4 [non-blocking]: How is the change validated at the customer site before go-live? | answer:
- Q-MW-1 [blocking]: Which LIS and interface engines must accept the new message, and which HL7 version? | answer: Pilot sites only for 2027.1, HL7 v2.5 standard segments (DC-3).
- Q-MW-2 [blocking]: Is the new behavior on by default, or configured per interface? | answer: Off by default, enabled per interface, as the LIS admin asked.
- Q-MW-3 [non-blocking]: What message volume and peak rate must this handle at the largest site? | answer:
- Q-MW-4 [non-blocking]: How will field teams validate this without a full revalidation? | answer: Add a held-status message script to the field interface validation kit.
- Q-QC-1 [non-blocking]: Which QC rules and frequencies apply? | answer: Reagent QC each day of use per lab policy. TypeBridge reads QC validity from the analyzer and does not evaluate QC rules.
- Q-QC-2 [blocking]: What corrective action must be documented before patient results can be released? | answer: Results held as reagent_qc_not_valid clear only after acceptable reagent QC is recorded and the sample is rerun. Corrective action is documented in the lab's QC system.
- Q-QC-3 [non-blocking]: How are patient results run since the last acceptable QC identified for review? | answer: By the lookback list in D-7; the review itself stays with the lab.
- Q-01 [blocking]: D-3 leaves the alert target and timing undecided. Who sees the alert, and how soon? | answer: Everyone logged into the blood bank worklist, within 60 seconds of the hold.
- Q-02 [blocking]: D-4 leaves the QC expiry lead time undecided. How early should the warning appear? | answer: 60 minutes before expiry, and again at 15 minutes.

## Assumptions
- A-01: The four interviews represent the other pilot sites | basis: none — inferred | status: UNVERIFIED
- A-02: The host system can supply each user's role and blood bank qualification to TypeBridge | basis: DC-1 | status: UNVERIFIED
- A-03: Pilot-site LIS systems display OBX-11 status "I" as in process | basis: D-6, DC-3 | status: UNVERIFIED
- A-04: Hold lookup time is a large enough share of turnaround that removing it moves the pre-op target | basis: F-02, F-04 | status: UNVERIFIED
