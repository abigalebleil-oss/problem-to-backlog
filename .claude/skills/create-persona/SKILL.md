---
name: create-persona
description: Interview a domain product owner or subject-matter expert and turn their expertise into a reusable persona pack in personas/ that the problem-to-ready skill can use. Use when a team wants to "create your own" persona or refresh an existing one.
---

# Create a persona pack

A persona pack captures how an experienced PO in a domain thinks: who the users are, what
customers value most, which rules are never broken, and what they always ask first. Once
written, every PO in that domain gets that judgment in their first draft.

## How to run it
1. Ask who you are interviewing (role, domain, years of experience) and whether this is a new
   persona or a refresh of one in `personas/`.
2. Interview **one section at a time**, in this order. Ask, listen, then play back what you
   heard in the persona's format and ask "what's wrong or missing?" before moving on.
   - **Domain**: "What does your software do, where does it sit, and what happens when it fails?"
   - **Users**: "Who touches it directly? Who depends on its output?"
   - **Value drivers**: "What do your customers judge you on? Rank them. If you could only protect one, which?"
   - **Regulatory and quality context**: "Which regulations, standards or SOPs shape your requirements?"
   - **Non-negotiables**: "What would you reject in a design review no matter how good the rest is?"
   - **Requirement fields**: "What must every requirement in your area state for your reviewers to accept it?"
   - **Banned terms**: "Which words in a requirement make your QA or regulatory team push back?"
   - **Always ask**: "What do you ask first when someone brings you a new feature?"
   - **Sign-offs**: "Who must approve before work enters your backlog?"
3. Use only what the interviewee says. If you suggest something from general knowledge, label it
   "suggested" and keep it only if they confirm it.
4. Write `personas/<id>.md` from `personas/_template.md`. Pick a unique 2–3 letter prefix.
   Set `status: draft — interviewed <name/role>, <date>`.
5. Run `python checks/checks.py persona personas/<id>.md` and fix anything it reports.
6. Show the finished file and ask the interviewee to approve it. Only then change status to
   `validated`. Record who contributed under Knowledge sources.

## Rules
- Value drivers are outcomes ("turnaround time from collection to result"), not features.
- Non-negotiables are testable rules, not values ("never auto-resolve a discrepancy", not "safety first").
- Keep each line to one idea; the checks and the skill cite lines by ID.
- Never put customer names, patient data or confidential product details in a persona.
