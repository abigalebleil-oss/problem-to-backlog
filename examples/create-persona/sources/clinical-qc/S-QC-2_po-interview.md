# S-QC-2 · Interview with a clinical QC software product owner (fictional)

Type: interview. Synthetic interview for the sandbox. Must be reviewed by the interviewee before
it is marked vetted.

## Domain
Collects QC results from analyzers across the lab, evaluates each QC run against the lab's
statistical rules, and tells technologists whether patient testing can continue. Sends QC data for
interlaboratory peer comparison. When it fails, a lab can release patient results on an analyzer
that is out of control, or stop testing for no reason.

## Users
- Bench technologist: reviews QC and accepts or rejects runs.
- Lab QC coordinator: configures rules, targets and limits per analyte.
- Lab supervisor or director: reviews QC trends and signs off corrective actions.
- LIS and middleware administrators: connect analyzers and the LIS to the QC software.

## What customers judge us on (ranked)
1. No patient results reported from a run after a QC failure until QC is acceptable again.
2. Time from a QC failure to the technologist knowing about it.
3. Inspection readiness: every QC decision and corrective action is documented and retrievable.
4. Fewer false rejections, so labs don't rerun QC that was actually fine.

## What I'd reject in any design review
1. A rule or target change that silently changes the accept or reject status of historical QC
   runs. Changes are versioned with an effective date.
2. A rejected QC run cleared without a documented corrective action and a named user.
3. QC data deleted or edited in place. Corrections are annotations with an audit trail.

## Every requirement must state
The risk it controls, the regulatory reference if one applies, and how it is verified.

## Words that make QA push back
Promptly, timely, real-time without a number, appropriate, sufficient, user-friendly, intuitive,
as needed, etc.

## What I ask first
- Does this change how a QC run is accepted or rejected?
- Which rules, targets and limits are configured per analyte, and who can change them?
- Does this change what we send for peer comparison?
- How will labs verify the change before go-live?

## Sign-offs
QC software product owner, software lead, QA lead, regulatory affairs.
