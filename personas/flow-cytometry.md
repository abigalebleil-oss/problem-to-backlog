# Persona: Flow Cytometry Software Product Owner
id: flow-cytometry
prefix: FC
status: draft: PO domain notes awaiting the PO's review

## Domain
Acquisition and analysis software for flow cytometers used in research, translational and
clinical labs. Users build multicolor panels, acquire samples, gate populations and export
results. Customers judge the product by whether the same sample gives the same answer across
days, operators, instruments and sites.

## Users
- U-FC-1: Core facility manager running shared instruments for many labs [src: S-FC-2]
- U-FC-2: Research scientist designing panels and analyzing populations [src: S-FC-2]
- U-FC-3: Clinical or translational lab technologist running standardized panels [src: S-FC-2]
- U-FC-4: Field application scientist supporting setup and troubleshooting [src: S-FC-2]

## Value drivers (ranked)
- VD-FC-1: Reproducibility: the same sample gives the same result across days, operators, instruments and sites [src: S-FC-2, S-FC-3]
- VD-FC-2: Time to market for new instrument and assay capabilities [src: S-FC-2]
- VD-FC-3: Data integrity and standard exports (FCS 3.1) that downstream tools accept [src: S-FC-2]
- VD-FC-4: Ease of panel setup and standardization for less-experienced users [src: S-FC-2]

## Regulatory and quality context
- REG-FC-1: Most customers run research-use-only (RUO) workflows; clinical customers may need IVD or CE-IVDR pathways for specific assays [src: S-FC-1]
- REG-FC-2: GxP customers expect 21 CFR Part 11 features (audit trail, e-signatures, user management) [src: S-FC-1]
- REG-FC-3: File format and metadata follow the FCS 3.1 standard [src: S-FC-1]

## Non-negotiable constraints
- C-FC-1: Changes to acquisition, compensation or gating math are versioned, and older experiments reopen with their original results [src: S-FC-2]
- C-FC-2: Exported FCS files stay valid FCS 3.1 and keep instrument settings metadata [src: S-FC-1, S-FC-2]
- C-FC-3: Instrument settings used for an acquisition are recorded with the data [src: S-FC-2]

## Requirement fields
- reproducibility-impact: none, or which result could change between runs, instruments or sites
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, timely, immediately, user-friendly, intuitive, seamless, appropriate,
as needed, if necessary, accurate, consistent, etc, and/or

## Always ask
- Q-FC-1: Could this change alter a population percentage or MFI for an existing experiment? [src: S-FC-2]
- Q-FC-2: Which instrument configurations and software versions must stay compatible? [src: S-FC-2]
- Q-FC-3: Do any GxP customers depend on this workflow? [src: S-FC-2]

## Sign-offs
- Product owner (flow cytometry)
- Software lead
- Applications / scientific lead
- QA lead

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-FC-1: Flow cytometry standards and regulatory summary | type: standard | file: sources/flow-cytometry/S-FC-1_standards.md | owner: Quality / regulatory affairs | vetted: 2026-10-22 by Regulatory affairs reviewer (fictional)
- S-FC-2: Flow cytometry PO domain notes | type: experience | file: sources/flow-cytometry/S-FC-2_po-notes.md | owner: Flow cytometry product owner | vetted: PENDING
- S-FC-3: Field support case themes, last 12 months (synthetic) | type: data | file: sources/flow-cytometry/S-FC-3_support-cases.md | owner: Support operations | vetted: 2026-10-22 by Support operations lead (fictional)
