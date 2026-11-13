<!-- Reference output of Step 1 (intake) for a NEW initiative started from one sentence.
     Drafted by Claude to illustrate the format; regenerate it live with the skill and compare.
     It fails Gate 1 on purpose: with no discovery or design, the blocking questions are open. -->

# Intake: INIT-003 · persona: flow-cytometry · consulted: none

## Understanding
The PO wants requirements for a flow cytometer workflow that captures images (F-01), with the
first release limited to research use (DC-1). For a flow cytometry product, success means imaging
adds information without changing any existing result: the same sample still gives the same
answer across runs, instruments and sites (VD-FC-1), and older experiments reopen unchanged
(C-FC-1). Nothing yet says who needs images or for which decision, so that comes first.

## Questions
- Q-FC-1 [blocking]: Could this change alter a population percentage or MFI for an existing experiment? | answer:
- Q-FC-2 [blocking]: Which instrument configurations and software versions must stay compatible? | answer:
- Q-FC-3 [non-blocking]: Do any GxP customers depend on this workflow? | answer: Not for the first release, which is research use only (DC-1).
- Q-01 [blocking]: Which users need images, and what decision does an image help them make (for example doublet exclusion, morphology or localization)? | answer:
- Q-02 [blocking]: Is this a new instrument or an imaging module for an existing one? | answer:
- Q-03 [blocking]: How are images stored and linked to events, given exported FCS files must stay valid FCS 3.1 (C-FC-2)? | answer:
- Q-04 [non-blocking]: What acquisition rate do users expect with imaging on? | answer:
- Q-05 [non-blocking]: Which release is this targeted for? | answer:

## Assumptions
- A-01: Research scientists (U-FC-2) are the first users of imaging | basis: none — inferred | status: UNVERIFIED
- A-02: Experiments acquired without imaging must open and analyze exactly as they do today | basis: C-FC-1 | status: UNVERIFIED
- A-03: Each image is captured per event, alongside the standard scatter and fluorescence parameters | basis: none — inferred | status: UNVERIFIED
