# Discovery output: INIT-001 — Held blood typing results stop delaying crossmatch-ready blood

Source: synthetic discovery summary for a fictional blood typing middleware product (analyzer to LIS). All people,
sites and numbers are fictional. Each finding cites the feedback file it comes from.

## Problem statement
When the typing analyzer holds a type and screen, the middleware does not say why, the LIS shows
the order as pending, and manual resolutions are documented on paper. Technologists lose time
diagnosing holds, clinicians cannot tell whether blood will be ready, and the lab cannot prove
who reviewed each resolution. Holds are the main reason the lab misses its pre-op turnaround target.

## Findings
- F-01: The middleware worklist shows HOLD with no reason; technologists walk to the analyzer to find out whether it is a discrepancy, weak reaction or QC problem [source: 01_night_typing_tech.md]
- F-02: Each hold costs about 5–10 minutes of lookup, with 6–8 holds on a busy night [source: 01_night_typing_tech.md]
- F-03: Technologists learn about holds late, sometimes only when a clinical unit calls [source: 01_night_typing_tech.md]
- F-04: Holds are the main reason the lab misses its 60-minute pre-op crossmatch-ready target [source: 02_lab_supervisor.md]
- F-05: Discrepancy resolutions are documented on paper and cannot always be attributed at inspection [source: 02_lab_supervisor.md]
- F-06: The lab's SOP already requires a second person to review discrepancy resolution [source: 02_lab_supervisor.md]
- F-07: The LIS shows held orders as pending with no reason, so nursing cannot tell if a sample is being worked [source: 03_lis_admin.md]
- F-08: Reagent QC lapses at shift change hold all subsequent typing results about twice a month [source: 04_qc_coordinator.md]
- F-09: After a QC failure, the lab needs the list of patient samples run since the last acceptable QC [source: 04_qc_coordinator.md]

## Constraints stated by users
- Software must never resolve a discrepancy on its own [source: 01_night_typing_tech.md]
- Standard HL7 v2.5 only, no Z-segments [source: 03_lis_admin.md]
- New LIS messages must be enabled per interface [source: 03_lis_admin.md]

## Not yet known
- How many holds per week across all shifts and sites
- What share of missed pre-op targets each hold type causes
- Whether STAT and emergency release orders need different handling
