# Create-persona demo input: clinical lab QC software PO

Synthetic interview for the live demo. Paste everything below the line into Claude Code after
running `/create-persona`. The finished result is saved beside this file as a backup:
`examples/create-persona/clinical-qc.md` and its `sources/` folder.

---

New persona, please. Use id `clinical-qc` and prefix `QC`. I'm giving you all my answers at once
to save time, plus a standards summary my regulatory team already trusts. Save the standards
summary as source S-QC-1 (type: standard, owner: Quality / regulatory affairs) and my answers as
S-QC-2 (type: interview, owner: Clinical QC software product owner). Leave both PENDING.

Who I am: product owner for clinical laboratory quality control (QC) data management software,
8 years in the domain.

Domain: Our software collects QC results from analyzers across the lab, evaluates each QC run
against the lab's statistical rules, and tells technologists whether patient testing can continue.
It also sends QC data for interlaboratory peer comparison. When it fails, a lab can release patient
results on an analyzer that is out of control, or stop testing for no reason.

Users: The bench technologist reviews QC and accepts or rejects runs. The lab QC coordinator
configures rules, targets and limits per analyte. The lab supervisor or director reviews QC
trends and signs off corrective actions. LIS and middleware administrators connect analyzers and
the LIS to the QC software.

What customers judge us on, ranked: 1. No patient results reported from a run after a QC failure
until QC is acceptable again. 2. Time from a QC failure to the technologist knowing about it.
3. Inspection readiness: every QC decision and corrective action is documented and retrievable.
4. Fewer false rejections, so labs don't rerun QC that was actually fine.

Regulations and standards: see the standards summary.

What I'd reject in any design review: 1. A rule or target change that silently changes the
accept or reject status of historical QC runs. Changes are versioned with an effective date.
2. A rejected QC run cleared without a documented corrective action and a named user.
3. QC data deleted or edited in place. Corrections are annotations with an audit trail.

Every requirement must state: the risk it controls, the regulatory reference if one applies, and
how it is verified.

Words that make QA push back: promptly, timely, real-time without a number, appropriate,
sufficient, user-friendly, intuitive, as needed, etc.

What I ask first: Does this change how a QC run is accepted or rejected? Which rules, targets and
limits are configured per analyte, and who can change them? Does this change what we send for
peer comparison? How will labs verify the change before go-live?

Sign-offs: QC software product owner, software lead, QA lead, regulatory affairs.

STANDARDS SUMMARY (save as S-QC-1):
- US labs must run QC and evaluate it before reporting patient results, under CLIA (42 CFR
  493.1256), and keep QC records for inspection.
- CAP and ISO 15189 accredited labs must document QC rules, review QC regularly, and record
  corrective action for every QC failure.
- Westgard multirules (for example 1-3s, 2-2s, R-4s) are the common statistical rules labs
  configure per analyte; Levey-Jennings charts are the common way to review QC over time.
- Software that keeps regulated QC records is expected to provide audit trails, user
  attribution and record retention.
