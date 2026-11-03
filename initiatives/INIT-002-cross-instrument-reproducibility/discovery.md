# Discovery output: INIT-002 — Same sample, same answer, on any instrument

Source: synthetic discovery summary for a fictional flow cytometry software product
("CytoSuite"). All people, sites and numbers are fictional. Each finding cites its feedback file.

## Problem statement
Labs with more than one cytometer get different answers for the same sample depending on the
instrument, and cannot tell before acquiring whether an instrument has drifted. Upgrades and
template edits can silently change results on old experiments. Labs prove standardization with
spreadsheets and screenshots. Reproducibility, the thing customers judge the product on most,
depends on manual work outside the software.

## Findings
- F-01: The same control sample gives CD4 percentages 3–4 points apart across instruments in one facility [source: 01_core_facility_manager.md]
- F-02: Facility staff spend about two hours a month matching voltages manually with beads and a spreadsheet [source: 01_core_facility_manager.md]
- F-03: A software upgrade shifted gates on a reopened experiment and damaged customer trust [source: 01_core_facility_manager.md]
- F-04: Longitudinal studies need to know results stay comparable across instrument service events [source: 02_research_scientist.md]
- F-05: Researchers want to apply one gating template across timepoints and see what changed [source: 02_research_scientist.md]
- F-06: Template edits must not force re-gating of existing files [source: 02_research_scientist.md]
- F-07: Settings drift after service is the most common cause of instrument disagreement visits; users want a baseline comparison before acquiring [source: 03_field_application_scientist.md]
- F-08: FCS keyword errors in exports are blamed on the product [source: 03_field_application_scientist.md]
- F-09: Multi-site trials need per-run proof that instruments were set up the same way; today it is screenshots [source: 04_translational_lab_tech.md]

## Not yet known
- How often instruments drift outside tolerance between scheduled services
- Which third-party analysis tools customers use most
