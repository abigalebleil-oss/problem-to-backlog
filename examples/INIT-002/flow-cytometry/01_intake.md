<!-- Reference output of Step 1 (intake) after the PO answered the blocking questions.
     Drafted by Claude to illustrate the format; regenerate it live with the skill and compare.
     All answers are fictional. -->

# Intake: INIT-002 · persona: flow-cytometry · consulted: none

## Understanding
Labs running more than one cytometer get different answers for the same sample, find out about
drift only after acquiring, and can lose trust when an upgrade or template edit changes old
results. For a flow cytometry customer, done means an instrument that has drifted is flagged
before acquisition, old experiments always reopen with their saved results, runs can be compared
across time, and standardization is provable per run without screenshots.

## Questions
- Q-FC-1 [blocking]: Could this change alter a population percentage or MFI for an existing experiment? | answer: Yes, D-4 changes how templates are stored. Existing experiments must migrate pinned to the template version they were last analyzed with, so nothing changes on reopen.
- Q-FC-2 [blocking]: Which instrument configurations and software versions must stay compatible? | answer: All configurations supported in the current release; experiments saved in the two previous major versions must reopen.
- Q-FC-3 [blocking]: Do any GxP customers depend on this workflow? | answer: Yes. DC-3 says the gating engine is shared with the GxP edition, so template versioning must be verified there too.
- Q-01 [blocking]: D-2 leaves tolerance and blocking undecided. What tolerance, and does a flag block acquisition? | answer: Flag any detector whose daily bead median MFI differs from its baseline target by more than 10%. Warn, do not block; record the flag with the run.
- Q-02 [non-blocking]: D-5 leaves the comparison threshold undecided. When should a population change be flagged? | answer:
- Q-03 [blocking]: D-3 setting transfer is the largest engineering item. Is it required in 2027.1? | answer: No. Defer to 2027.2; the baseline check finds the drift, and field scientists can transfer settings manually until then.

## Assumptions
- A-01: The four interviews represent core facilities and multi-site trial labs generally | basis: none — inferred | status: UNVERIFIED
- A-02: One bead lot can serve as a baseline for the life of that lot on an instrument | basis: DC-1 | status: UNVERIFIED
- A-03: Customers' third-party analysis tools ignore FCS keywords they do not recognize | basis: DC-2 | status: UNVERIFIED
