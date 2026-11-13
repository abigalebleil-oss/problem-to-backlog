---
name: create-persona
description: Interview a domain product owner or subject-matter expert, save the vetted sources, and turn them into a reusable persona pack in personas/ that the problem-to-backlog skill can use. Use when a team wants to "create your own" persona or refresh an existing one.
---

# Create a persona pack

A persona pack captures how an experienced PO in a domain thinks: who the users are, what
customers value most, which rules are never broken, and what they always ask first. A business
team does this **once**. After that, every PO in the domain drafts from the same vetted, local
knowledge instead of from the model's general knowledge, so there is less to hallucinate and
fewer assumptions to check.

**Every persona line must come from a saved source.** The persona is a summary; the sources are
the evidence.

## How to run it
1. Ask who you are interviewing (role, domain, years of experience), and whether this is a new
   persona or a refresh of one in `personas/`. Pick a unique 2–3 letter prefix.
2. **Collect sources first.** Ask what written material the team already trusts and save each
   one under `personas/sources/<id>/S-<PREFIX>-<n>_<short-name>.md`:
   - `standard`: summary of the regulations and standards that shape requirements
   - `sop`: excerpts of SOPs or work instructions (company or, with permission, customer)
   - `data`: exports such as support case themes, complaint trends, usage data
   - `document`: product docs, design guidelines, prior decisions
   - `experience`: a PO's own written notes
   Never save patient data, customer-identifying details or anything confidential that should
   not be shared with the AI tool in use.
3. **Interview one section at a time**, in this order, and save the notes as an `interview`
   source as you go. Ask, listen, then play back what you heard and ask "what's wrong or missing?"
   - **Domain**: "What does your software do, where does it sit, and what happens when it fails?"
   - **Users**: "Who touches it directly? Who depends on its output?"
   - **Value drivers**: "What do your customers judge you on? Rank them."
   - **Regulatory and quality context**: "Which regulations, standards or SOPs shape your requirements?"
   - **Non-negotiables**: "What would you reject in a design review no matter how good the rest is?"
   - **Requirement fields**: "What must every requirement in your area state for reviewers to accept it?"
   - **Banned terms**: "Which words in a requirement make QA or regulatory push back?"
   - **Always ask**: "What do you ask first when someone brings you a new feature?"
   - **Sign-offs**: "Who must approve before work enters your backlog?"

   If the user gives you all the answers at once (pasted notes), don't re-ask each section: save
   them as the interview source, play back a one-screen summary by section, and ask once
   "what's wrong or missing?"
4. Write `personas/<id>.md` from `personas/_template.md`. End every ID line with
   `[src: S-<PREFIX>-n]` naming the source(s) it came from. If a line comes from your general
   knowledge and no source supports it, do not write it; ask the interviewee instead.
5. Register every source under `## Sources` with its type, file, owner, and `vetted: PENDING`.
6. Run `python checks/checks.py persona personas/<id>.md` and fix anything it reports.
7. **Vetting is a human step.** Ask each source's owner to review the source file and the
   persona lines that cite it. Only after they confirm, change that source to
   `vetted: <YYYY-MM-DD> by <name/role>`. When every source is vetted, set
   `status: validated`. The check fails a persona marked validated with unvetted sources.
8. Show the final persona and the check output. Remind the team that vetted sources go stale
   after 12 months and the check will ask for a re-vet.

## Rules
- Value drivers are outcomes ("turnaround time from collection to result"), not features.
- Non-negotiables are testable rules, not values ("never auto-resolve a discrepancy", not "safety first").
- One idea per line; the skill and the checks cite lines by ID.
- Never mark a source vetted yourself.
