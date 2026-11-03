# Technical software design: INIT-002 — Cross-instrument reproducibility

Source: synthetic design notes for a fictional flow cytometry product ("CytoSuite").

## Current behavior
1. Daily QC runs a bead lot and reports pass or fail per detector against the bead vendor's range.
   Results are not compared with any instrument-specific baseline.
2. Gating templates are saved in place. Editing a template changes every experiment that uses it
   the next time the experiment is opened.
3. FCS 3.1 export writes standard keywords and detector voltages.

## Proposed design elements
- D-1: Instrument baseline. At setup, capture target median MFI per detector from a bead lot run and store it as the instrument's baseline.
- D-2: Pre-acquisition baseline check. Compare the daily bead run to the baseline and flag detectors outside tolerance before acquisition. Tolerance and whether to block are not yet decided by product.
- D-3: Target-value setting transfer. Compute detector voltages on instrument B that reproduce instrument A's baseline targets; the user reviews and applies them.
- D-4: Versioned gating templates. Each save creates a version; experiments pin the version they were analyzed with.
- D-5: Cross-run comparison report. For experiments sharing a template version, report population percentage and median MFI per run and flag changes above a threshold. Threshold not yet decided.
- D-6: Standardization record. Per acquisition, export instrument ID, baseline ID, bead lot, check result and detector voltages, and write baseline ID and check result into the FCS file.

## Design constraints
- DC-1: Bead lot target values are vendor-provided per lot.
- DC-2: FCS 3.1 reserves keywords that start with "$"; product keywords must not use that prefix.
- DC-3: The gating and compensation engine is shared with the GxP edition of the product.
