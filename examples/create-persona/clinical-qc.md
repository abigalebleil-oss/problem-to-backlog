# Persona: Clinical Lab QC Software Product Owner
id: clinical-qc
prefix: QC
status: draft: built live with create-persona; sources awaiting their owners' review

<!-- Backup of the persona the create-persona skill builds in the live demo from
     examples/create-persona/interview-notes.md. Drafted by Claude to illustrate the output.
     To use it for real, move it and its sources/ folder into personas/. -->

## Domain
Software that collects QC results from analyzers across the lab, evaluates each QC run against the
lab's statistical rules, and tells technologists whether patient testing can continue. It also
sends QC data for interlaboratory peer comparison. When it fails, a lab can release patient
results on an out-of-control analyzer, or stop testing for no reason.

## Users
- U-QC-1: Bench technologist who reviews QC and accepts or rejects runs [src: S-QC-2]
- U-QC-2: Lab QC coordinator who configures rules, targets and limits per analyte [src: S-QC-2]
- U-QC-3: Lab supervisor or director who reviews QC trends and signs off corrective actions [src: S-QC-2]
- U-QC-4: LIS and middleware administrator who connects analyzers and the LIS to the QC software [src: S-QC-2]

## Value drivers (ranked)
- VD-QC-1: No patient results reported from a run after a QC failure until QC is acceptable again [src: S-QC-2, S-QC-1]
- VD-QC-2: Time from a QC failure to the technologist knowing about it [src: S-QC-2]
- VD-QC-3: Inspection readiness: every QC decision and corrective action is documented and retrievable [src: S-QC-2, S-QC-1]
- VD-QC-4: Fewer false rejections, so labs don't rerun QC that was actually fine [src: S-QC-2]

## Regulatory and quality context
- REG-QC-1: Under CLIA (42 CFR 493.1256), US labs run and evaluate QC before reporting patient results and keep QC records for inspection [src: S-QC-1]
- REG-QC-2: CAP and ISO 15189 labs document QC rules, review QC regularly and record corrective action for every QC failure [src: S-QC-1]
- REG-QC-3: Westgard multirules are configured per analyte and Levey-Jennings charts are the common QC review [src: S-QC-1]
- REG-QC-4: Regulated QC records need audit trails, user attribution and record retention [src: S-QC-1]

## Non-negotiable constraints
- C-QC-1: A rule or target change never changes the accept or reject status of historical QC runs; changes are versioned with an effective date [src: S-QC-2]
- C-QC-2: A rejected QC run is never cleared without a documented corrective action and a named user [src: S-QC-2, S-QC-1]
- C-QC-3: QC data is never deleted or edited in place; corrections are annotations with an audit trail [src: S-QC-2, S-QC-1]

## Requirement fields
- risk: the risk this requirement controls
- regulatory-reference: the regulation or standard it supports, or none
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, timely, real-time, appropriate, sufficient, user-friendly, intuitive, as needed, etc

## Always ask
- Q-QC-1: Does this change how a QC run is accepted or rejected? [src: S-QC-2]
- Q-QC-2: Which rules, targets and limits are configured per analyte, and who can change them? [src: S-QC-2]
- Q-QC-3: Does this change what we send for peer comparison? [src: S-QC-2]
- Q-QC-4: How will labs verify the change before go-live? [src: S-QC-2]

## Sign-offs
- QC software product owner
- Software lead
- QA lead
- Regulatory affairs

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-QC-1: Clinical QC standards and regulatory summary | type: standard | file: sources/clinical-qc/S-QC-1_standards.md | owner: Quality / regulatory affairs | vetted: PENDING
- S-QC-2: Interview with a clinical QC software product owner (fictional) | type: interview | file: sources/clinical-qc/S-QC-2_po-interview.md | owner: Clinical QC software product owner | vetted: PENDING
