# Live demo script (~12 minutes inside the 25-minute slot)

Keep the saved examples open in a second tab as backup if a live run is slow.

| Min | Show | Say |
|---|---|---|
| 0–1 | README problem section | Alignment, not writing, is the slow part. This drafts what every group must agree on, already shaped by their domain. |
| 1–3 | `personas/clinical-analyzer.md` next to `personas/middleware-reporting.md`, then `personas/sources/clinical-analyzer/` | Same template, different judgment. Value drivers rank the work; non-negotiables can't be weakened; required fields differ. Every line cites a vetted source: built once by the business team, reused by every PO. |
| 3 | `checks.py persona personas/flow-cytometry.md`; vet S-FC-2 live (set the date and your name), re-run | My own domain notes aren't vetted yet, so the check says so. I vet them, and the persona is backed by vetted sources. |
| 3–5 | Run `/problem-to-backlog`, pick clinical analyzer + consult middleware | Persona selection. Consulted teams' constraints come along automatically. |
| 5–7 | Intake output, then `checks.py intake` | It stops. Every persona question is asked; undecided design items become questions. The gate fails until blocking questions are answered. |
| 7–9 | `checks.py plan` on the clinical analyzer plan, then the middleware plan; `checks.py provenance` on one | Same inputs, different plans: safety-first ordering and lookback kept vs. interop-first and QC items deferred with a raised conflict. Provenance shows every rule traced to a vetted file. |
| (backup) | `examples/INIT-002/flow-cytometry/03_plan.md` | Different domain, same machinery: reproducibility drives the order; setting transfer deferred for time to market. |
| 9–11 | `checks.py plan` on planted failures | Paraphrased quote, invented finding, "promptly", missing field, orphaned finding, a consulted team's constraint dropped: all caught. Then REQ-05: it passes, and it would auto-resolve discrepancies. That's why humans sign off. |
| 11–12 | `review.py start` / `status`, trace matrix | Review log is the record and the feedback loop: rejection reasons show which persona or rule to fix. |

## Likely questions to be ready for
- Why markdown personas, not a database? Any PO can write and review one; diffs show what changed; checks parse it.
- How do you stop personas going stale? Every source has an owner and a vetting date; the check queues re-vetting after 12 months; review-log rejection reasons point to gaps.
- How does this reduce hallucination? The model may cite only IDs from vetted local files; code fails anything it can't trace; anything else must be listed as an assumption or a question.
- What if two personas conflict? The skill must write CONFLICT and name an owner; it never resolves it.
- Where would this break? Bad inputs in, plausible output out. The checks catch ungrounded output, not wrong inputs or wrong judgment.
- Data sensitivity? Synthetic here. In practice: only approved tools, no patient data, personas contain no customer-identifying details.
