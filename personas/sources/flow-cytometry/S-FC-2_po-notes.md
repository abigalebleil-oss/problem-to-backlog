# S-FC-2 · Domain notes from a flow cytometry software product owner

Type: experience. Written for the sandbox to illustrate a PO's own domain notes. Must be
reviewed and vetted by the flow cytometry PO before this persona is marked validated.

## Who uses it
- Core facility managers run shared instruments for many labs.
- Research scientists design panels and analyze populations.
- Clinical and translational technologists run standardized panels.
- Field application scientists support setup and troubleshooting.

## What customers judge us on (ranked)
1. Reproducibility: the same sample gives the same result across days, operators, instruments and sites.
2. Time to market for new instrument and assay capabilities.
3. Data integrity and standard exports that downstream tools accept.
4. Ease of panel setup and standardization for less-experienced users.

## Never
- Changes to acquisition, compensation or gating math are versioned, and older experiments reopen with their original results.
- Exported FCS files stay valid FCS 3.1 and keep instrument settings metadata.
- The instrument settings used for an acquisition are recorded with the data.

## Every requirement must say
- Reproducibility impact: which result could change between runs, instruments or sites.
- How it is verified.

## Words that cause trouble
- Accurate and consistent without a metric; fast; intuitive; plus the usual vague terms.

## What I ask first
- Could this change a population percentage or MFI for an existing experiment?
- Which instrument configurations and software versions must stay compatible?
- Do any GxP customers depend on this workflow?

## Who signs off
- PO, software lead, applications or scientific lead, QA lead.
