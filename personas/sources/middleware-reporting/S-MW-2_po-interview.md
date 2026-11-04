# S-MW-2 · Interview with a middleware and connectivity product owner (fictional)

Type: interview. Synthetic notes for the sandbox. Interviewee: "J. Park", PO, lab middleware, 7 years (fictional).

## Who uses it
- "The LIS or interface admin at the site is my real customer."
- "Bench techs work the worklist all shift."
- "Field application specialists install and validate every interface."
- "Lab IT and security review us before anything connects."
- "Clinicians never log in to us, but every result they read in the EHR came through us."

## What customers judge us on (ranked)
1. "Interoperability. Every supported LIS and engine accepts our messages without custom work."
2. "No lost, duplicated or out-of-order results. Ever."
3. "Upgrades don't break existing site configs."
4. "Install and validation effort per site."
5. "The bench can see what happened to each result and why."

## Never
- "Only standard segments of the HL7 version the site runs. No Z-segments unless they agreed."
- "New outbound messages are off by default and turned on per interface."
- "Every inbound message is acknowledged and traceable to every message we send because of it."
- "We don't do user management. Identity comes from the host."

## Every requirement must say
- "Interface impact: none, inbound, outbound or both, and which message."
- "Backward compatible, or the migration path."
- "How it's verified."

## Words that cause trouble
- "Real-time, seamless, robust, scalable — and all the usual ones like promptly and as needed."

## What I ask first
- "Which LIS and engines must accept this, on which HL7 version?"
- "On by default, or per interface?"
- "Volume and peak rate at the biggest site?"
- "How will field validate it without a full revalidation?"

## Who signs off
- "Me, the integration lead, field applications or service, and QA/RA."
