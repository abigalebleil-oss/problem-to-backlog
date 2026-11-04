# S-CA-1 · Regulatory and standards summary for blood typing analyzer software

Type: standard summary. Written from public sources for the sandbox. In a real deployment,
regulatory affairs owns this file and links each item to the controlled copy of the standard.

- FDA regulates blood typing software used by blood establishments (blood establishment computer
  software, BECS) as a medical device. Software
  changes follow design controls under 21 CFR 820 and may need a regulatory assessment.
- 21 CFR Part 11 sets expectations for electronic records and signatures: attribution, audit trail, retention.
- IEC 62304 defines the software lifecycle and safety classes A, B and C. Software that decides
  whether a typing result can be released is treated as class C unless risk analysis shows otherwise.
- ISO 14971 governs risk management. Requirements that control a hazard trace to it.
- AABB Standards and the CAP checklist items for blood typing (immunohematology) set lab
  procedures the software must support.
- Analyzer interpretation algorithms are part of the cleared device; downstream software must not
  alter or reinterpret them.
