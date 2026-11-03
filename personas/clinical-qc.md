# Persona: Clinical Lab QC Software Product Owner
id: clinical-qc
prefix: QC
status: draft: interview notes not yet vetted by the interviewee

## Domain
Software that manages quality control for clinical lab testing: QC lot setup, running controls,
applying multi-rule evaluation (e.g., Westgard rules), deciding whether patient results can be
reported, documenting corrective action, and comparing performance with peer labs. Its job is
to stop bad patient results from being reported without raising so many false alarms that
staff start ignoring them.

## Users
- U-QC-1: Bench technologist who runs controls and reviews QC flags [src: S-QC-2]
- U-QC-2: QC coordinator / lab quality manager [src: S-QC-2]
- U-QC-3: Lab director who signs off on QC policy [src: S-QC-2]
- U-QC-4: Inspector or assessor reviewing QC records [src: S-QC-2]

## Value drivers (ranked)
- VD-QC-1: Error detection: QC failures stop patient reporting before results reach clinicians [src: S-QC-2]
- VD-QC-2: Low false rejection: fewer needless reruns and holds [src: S-QC-2]
- VD-QC-3: Corrective action is documented and complete for every QC failure [src: S-QC-2]
- VD-QC-4: Inspection-ready QC records and review history [src: S-QC-2]

## Regulatory and quality context
- REG-QC-1: CLIA QC requirements (42 CFR 493.1256) and CAP checklist items set minimum QC frequency and review [src: S-QC-1]
- REG-QC-2: ISO 15189 for accredited labs: QC design, review and corrective action records [src: S-QC-1]
- REG-QC-3: QC rules and limits are lab policy, set by the lab director, not by software defaults [src: S-QC-1]

## Non-negotiable constraints
- C-QC-1: Patient results run after a QC rejection are not reported until QC is acceptable and the lab documents corrective action [src: S-QC-2]
- C-QC-2: QC rule configuration changes are attributable, dated and require director-level approval [src: S-QC-2]
- C-QC-3: A QC event and its corrective action stay linked to the patient results it affected [src: S-QC-2]

## Requirement fields
- qc-impact: none, or which QC decision this changes (evaluation, hold, release, record)
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, timely, immediately, appropriate, as needed, if necessary, accurate,
reliable, user-friendly, intuitive, etc, and/or

## Always ask
- Q-QC-1: Which QC rules and frequencies does the lab policy set for this test or reagent? [src: S-QC-2]
- Q-QC-2: What corrective action must be documented before patient results can be released? [src: S-QC-2]
- Q-QC-3: How are patient results run since the last acceptable QC identified for review? [src: S-QC-2]

## Sign-offs
- Product owner (QC software)
- Lab quality subject-matter expert
- Software lead
- Quality / regulatory affairs

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-QC-1: QC regulations and standards summary | type: standard | file: sources/clinical-qc/S-QC-1_regulations.md | owner: Quality / regulatory affairs | vetted: 2026-10-22 by Regulatory affairs reviewer (fictional)
- S-QC-2: QC software PO interview, M. Chen (fictional) | type: interview | file: sources/clinical-qc/S-QC-2_po-interview.md | owner: QC software product owner | vetted: PENDING
