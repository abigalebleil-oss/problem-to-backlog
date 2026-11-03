<!-- Reference output of Step 3 for the flow cytometry persona on a flow cytometry initiative.
     Drafted by Claude to illustrate the format; regenerate it live with the skill and compare.
     Passes the deterministic checks. Still needs every sign-off before it enters the backlog. -->

# Delivery plan: INIT-002 · persona: flow-cytometry · consulted: none

## Milestones

### MS-1 — A drifted instrument is caught before the sample is acquired
- Window: Release 2027.1, sprints 1–2
- Goal: each instrument has a baseline, and the daily bead run flags any detector more than 10% off target before a user acquires.
- Value drivers: VD-FC-1
- Out of scope: automatic setting transfer between instruments (deferred to 2027.2).

### MS-2 — Old experiments never change, and runs can be compared over time
- Window: Release 2027.1, sprints 2–4
- Goal: template edits create versions, every saved experiment reopens with its saved results, and a researcher can compare runs that share a template version.
- Value drivers: VD-FC-1
- Out of scope: comparing runs analyzed with different template versions.

### MS-3 — Standardization is provable for every run
- Window: Release 2027.1, sprints 4–5
- Goal: every acquisition exports a standardization record, and exported FCS files carry the baseline and check result while staying valid FCS 3.1.
- Value drivers: VD-FC-3, VD-FC-1
- Out of scope: sponsor-specific report formats.

## Customer value deliveries

### CVD-01 · MS-1 · Each instrument has a baseline to compare against
- User: U-FC-1
- User need: As a core facility manager, I need each instrument to store a baseline from a bead run so that I can tell when it drifts instead of discovering it from users' data.
- Value driver: VD-FC-1
- Traces to: F-01, D-1
- Evidence: "The CD4 percentage on the same control sample can differ by three or four points depending on which instrument they used." [source: 01_core_facility_manager.md]
- Requirements: REQ-01
- Acceptance criteria:
  - AC-1: Given a setup bead run with lot ID L-123, when the facility manager saves it as a baseline, then the instrument stores the median MFI per detector, the bead lot ID and the vendor target values.
  - AC-2: Given an instrument with a saved baseline, when a new baseline is saved, then the previous baseline is retained with its date and remains viewable.

### CVD-02 · MS-1 · Users see drift before they acquire
- User: U-FC-2
- User need: As a research scientist, I need to see whether the instrument has drifted from its baseline before I acquire so that I don't collect data I can't compare.
- Value driver: VD-FC-1
- Traces to: F-07, F-04, D-2
- Evidence: "If the software compared the daily bead run to a baseline and told the user before they acquired, I'd lose most of those visits." [source: 03_field_application_scientist.md]
- Requirements: REQ-02, REQ-03
- Acceptance criteria:
  - AC-1: Given a daily bead run where detector FL3 median MFI is 12% below its baseline target, when the user opens acquisition, then FL3 is flagged with the measured difference before the first sample is acquired.
  - AC-2: Given all detectors within 10% of target, when the user opens acquisition, then no detector is flagged.
  - AC-3: Given a flagged detector, when the user starts acquisition anyway, then the run is saved with the check result, the flagged detectors and the user ID.

### CVD-03 · MS-2 · Saved experiments reopen exactly as saved
- User: U-FC-1
- User need: As a core facility manager, I need every saved experiment to reopen with its saved results after an upgrade or template edit so that labs can trust the numbers they already reported.
- Value driver: VD-FC-1
- Traces to: F-03, F-06, D-4
- Evidence: "Don't make me re-gate 400 files because someone edited a template." [source: 02_research_scientist.md]
- Requirements: REQ-04, REQ-05
- Acceptance criteria:
  - AC-1: Given an experiment analyzed with template version 3, when the template is edited and saved as version 4, then the experiment still opens with version 3 and identical population counts.
  - AC-2: Given experiments saved in each of the two previous major versions, when they are opened in this release, then population counts and percentages are identical to the saved values.
  - AC-3: Given the GxP edition, when AC-1 and AC-2 are run, then the results are identical and template version changes appear in the audit trail.

### CVD-04 · MS-2 · Compare runs that share a template
- User: U-FC-2
- User need: As a research scientist running a longitudinal study, I need to compare population results across runs that use the same template version so that I can see whether anything moved after an instrument service.
- Value driver: VD-FC-1
- Traces to: F-04, F-05, D-5
- Evidence: "I want to apply the same gating template to every timepoint and see if anything moved." [source: 02_research_scientist.md]
- Requirements: REQ-06
- Acceptance criteria:
  - AC-1: Given five experiments analyzed with template version 4, when the scientist opens the comparison report, then it lists population percentage and median MFI per population per run in run date order.
  - AC-2: Given a population whose percentage differs from the first run by more than 2 percentage points, when the report is generated, then that population and run are flagged.

### CVD-05 · MS-3 · A standardization record for every run
- User: U-FC-3
- User need: As a translational lab technologist on a multi-site trial, I need a standardization record exported for every run so that I can show the sponsor both sites were set up the same way without screenshots.
- Value driver: VD-FC-1
- Traces to: F-09, D-6
- Evidence: "Right now that proof is screenshots in a binder." [source: 04_translational_lab_tech.md]
- Requirements: REQ-07
- Acceptance criteria:
  - AC-1: Given a completed acquisition, when the technologist exports its standardization record, then PDF and CSV files list instrument ID, baseline ID, bead lot, check result, flagged detectors and detector voltages.
  - AC-2: Given the same run, when the CSV and PDF are compared, then every value matches.

### CVD-06 · MS-3 · Exported FCS files carry the standardization data and open elsewhere
- User: U-FC-4
- User need: As a field application scientist, I need exported FCS files to include the baseline and check result and stay valid FCS 3.1 so that customers' third-party tools read them without errors.
- Value driver: VD-FC-3
- Traces to: F-08, D-6
- Evidence: "If a keyword is wrong, they blame us." [source: 03_field_application_scientist.md]
- Requirements: REQ-08, REQ-09
- Acceptance criteria:
  - AC-1: Given an exported FCS file, when its keywords are read, then baseline ID and check result appear as keywords that do not start with "$".
  - AC-2: Given an exported FCS file, when it is run through an FCS 3.1 validator, then it reports no errors.
  - AC-3: Given an exported FCS file, when it is opened in each of the two most-used third-party analysis tools, then events and detector names load without errors.

## Requirements

### REQ-01 · Instrument baseline
- Text: The system shall store, for each instrument, a baseline containing the median MFI per detector from a setup bead run, the bead lot ID and the vendor target values, and shall retain earlier baselines with their dates.
- Derived from: D-1, DC-1, F-01
- reproducibility-impact: none; new data only
- verification: test

### REQ-02 · Pre-acquisition baseline check
- Text: Before acquisition, the system shall compare the daily bead run with the instrument baseline and flag each detector whose median MFI differs from its baseline target by more than 10%.
- Derived from: D-2, F-07
- reproducibility-impact: none; does not change acquired data
- verification: test

### REQ-03 · Check result saved with the run
- Text: The system shall save the baseline check result, flagged detectors and user ID with every acquisition run, including runs started while a detector is flagged.
- Derived from: D-2, C-FC-3
- reproducibility-impact: none
- verification: test

### REQ-04 · Versioned gating templates
- Text: The system shall create a new template version each time a gating template is saved and shall pin each experiment to the template version it was analyzed with.
- Derived from: D-4, F-06
- reproducibility-impact: changes template storage; existing experiments migrate pinned to their last-used version
- verification: test

### REQ-05 · Reopen with saved results
- Text: When an experiment saved in this or either of the two previous major versions is opened, the system shall display population counts and percentages identical to the values saved with the experiment.
- Derived from: D-4, F-03, C-FC-1, DC-3
- reproducibility-impact: protects all existing experiments in RUO and GxP editions
- verification: test

### REQ-06 · Cross-run comparison report
- Text: For experiments that share a template version, the system shall report population percentage and median MFI per run and shall flag any population whose percentage differs from the first run by more than [PROPOSED] 2 percentage points.
- Derived from: D-5, F-05
- reproducibility-impact: none; read-only report
- verification: test

### REQ-07 · Standardization record export
- Text: The system shall export, for each acquisition, a PDF and a CSV record listing instrument ID, baseline ID, bead lot, check result, flagged detectors and detector voltages.
- Derived from: D-6, F-09, C-FC-3
- reproducibility-impact: none
- verification: test

### REQ-08 · Standardization keywords in FCS
- Text: The system shall write the baseline ID and check result to each exported FCS file as keywords that do not start with "$".
- Derived from: D-6, DC-2, C-FC-2
- reproducibility-impact: none; adds metadata only
- verification: test

### REQ-09 · FCS 3.1 validity
- Text: Exported FCS files shall pass FCS 3.1 validation and open without errors in the [PROPOSED] two third-party analysis tools most used by customers.
- Derived from: D-6, F-08, C-FC-2
- reproducibility-impact: none
- verification: demonstration

## Cross-team alignment
- C-FC-1: addressed by REQ-04, REQ-05 — experiments pin template versions and reopen with saved values
- C-FC-2: addressed by REQ-08, REQ-09 — non-reserved keywords and FCS 3.1 validation
- C-FC-3: addressed by REQ-03, REQ-07 — check result, voltages and settings saved and exported with each run

## Deferred
- D-3: deferred — setting transfer between instruments moves to 2027.2 (PO decision at Gate 1, Q-03)
- F-02: deferred — manual voltage matching is addressed by D-3 in 2027.2; MS-1 makes the drift visible in the meantime

## Assumptions
- A-01: The four interviews represent core facilities and multi-site trial labs generally | basis: none — inferred | status: UNVERIFIED
- A-02: One bead lot can serve as a baseline for the life of that lot on an instrument | basis: DC-1 | status: UNVERIFIED
- A-03: Customers' third-party analysis tools ignore FCS keywords they do not recognize | basis: DC-2 | status: UNVERIFIED
- A-04: A 2-percentage-point change is the right flag threshold for the comparison report | basis: none — proposed to make D-5 testable | status: UNVERIFIED
- A-05: Support case data shows the two most-used third-party tools | basis: none — inferred | status: UNVERIFIED

## Open questions
- Q-02 [non-blocking]: When should the comparison report flag a population change?

## Decision log
- DEC-01: Baseline check ships first (MS-1) | why: reproducibility is the top value driver and drift after service is the most common cause of disagreement | sources: VD-FC-1, F-07
- DEC-02: Warn, do not block, when a detector is flagged | why: PO answer at Gate 1; research users decide, and the flag is recorded with the run | sources: Q-01, C-FC-3
- DEC-03: Template versioning is verified in the GxP edition too | why: shared engine | sources: Q-FC-3, DC-3
- DEC-04: Setting transfer deferred to 2027.2 | why: largest engineering item; trades some facility time for time to market | sources: Q-03, VD-FC-2, F-02
