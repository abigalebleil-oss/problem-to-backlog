# S-BB-2 · Interview with a blood bank software product owner (fictional)

Type: interview. Synthetic interview notes for the sandbox, captured with the create-persona
skill. Interviewee: "R. Ortiz", Senior PO, blood bank middleware, 9 years (fictional).

## Who uses it
- "The bench tech is the main user, and on nights they're usually alone."
- "The transfusion service supervisor owns the SOPs and answers to inspectors."
- "The medical director signs off on anything that changes how discrepancies are handled."
- "Clinicians never see our screens, but they're the ones waiting. Surgery, trauma, L&D."

## What customers judge us on (ranked)
1. "Patient safety, full stop. The right blood to the right patient. No release we can't defend."
2. "Turnaround time from collection to crossmatch-ready. That's the number labs report up."
3. "Inspection readiness. Every manual decision has a name, a time and a reason."
4. "Workload. Fewer lookups and re-keying per sample."

## Never, in any design review
- "Software never resolves an ABO/Rh discrepancy on its own."
- "Any manual resolution needs who, when, what and why, and a second qualified person."
- "We don't touch the analyzer's interpretation. That's a cleared algorithm."
- "A sample ID mismatch is a hard stop. No override, new sample."

## Every requirement must say
- "What hazard it controls, or 'none'."
- "The 62304 class we're assuming for that piece of software."
- "How it will be verified."

## Words QA pushes back on
- "Promptly, quickly, timely, appropriate, as needed, user-friendly, intuitive. Also 'safe' and
  'correct' — those aren't requirements, they're hopes."

## What I ask first
- "Who's allowed to resolve which hold type alone, and which need a second person?"
- "What turnaround target, for which priority — routine, pre-op, STAT, massive transfusion?"
- "Does this touch interpretation, release logic or patient ID? Then what's the regulatory path?"
- "How does the site validate it before go-live?"

## Who signs off
- "Me, the software lead, QA/RA, the risk management owner, and a clinical or medical affairs reviewer."
