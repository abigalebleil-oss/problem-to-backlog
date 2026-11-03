# Technical software design: INIT-001 — Held typing results

Source: synthetic design notes for a fictional blood bank middleware product ("TypeBridge").

## Current behavior
1. The typing analyzer sends results over ASTM (CLSI LIS2). Its interpretation is final and cleared;
   TypeBridge stores it and never recomputes it.
2. TypeBridge holds a result when the analyzer flags it, when reagent QC is not valid, or when
   the sample ID does not match an open order. The hold reason is stored as free text only.
3. Released results go to the LIS as HL7 v2.5 ORU^R01. Held results send nothing.
4. TypeBridge has an append-only audit log. Nothing writes to it for holds or releases today.

## Proposed design elements
- D-1: Hold category. Each hold carries a machine-readable category: `abo_rh_discrepancy`, `weak_or_mixed_field`, `reagent_qc_not_valid`, `sample_id_mismatch`, plus the analyzer flag text.
- D-2: Worklist hold panel. New panel showing category, analyzer flag and time held for every held sample.
- D-3: Hold alert. Event raised when a sample is held, shown on the worklist banner of the logged-in technologist. Delivery target and timing not yet decided by product.
- D-4: Reagent QC expiry warning. Warning shown before reagent QC for a typing reagent expires. Lead time not yet decided by product.
- D-5: Two-person resolution. A held discrepancy is resolved only after one technologist records the resolution and reason and a second qualified user reviews it. Both steps are written to the audit log.
- D-6: Held status to LIS. New HL7 v2.5 ORU^R01 with OBX-11 result status `I` (in process) and the hold category in an NTE segment, enabled per interface.
- D-7: QC lookback list. After a reagent QC failure, list patient samples run since the last acceptable QC for that reagent.

## Design constraints
- DC-1: TypeBridge has no user or role management. Identity and qualifications come from the host system.
- DC-2: The analyzer's interpretation algorithm is part of a cleared device and cannot be changed by TypeBridge.
- DC-3: The LIS interface engine at pilot sites accepts standard HL7 v2.5 segments only.
