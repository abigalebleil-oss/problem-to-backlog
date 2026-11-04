# Persona: Middleware and Result Reporting Product Owner
id: middleware-reporting
prefix: MW
status: draft: interview notes not yet vetted by the interviewees

## Domain
Lab middleware that takes results from clinical analyzers and reports them to clinicians. It
receives instrument output (ASTM / CLSI LIS2 or HL7), checks QC and applies result rules
(autoverification, holds, reruns), and sends verified results in HL7 v2.x to the laboratory
information system (LIS), where they flow to the clinician's record. It runs 24/7 at hundreds
of sites, each with a different LIS, interface engine and set of instruments, so compatibility,
uptime and never reporting an unverified result dominate.

## Users
- U-MW-1: LIS / interface administrator at the customer site [src: S-MW-2]
- U-MW-2: Bench technologist who works the middleware worklist [src: S-MW-2]
- U-MW-3: Field application specialist / service engineer who installs and validates interfaces [src: S-MW-2]
- U-MW-4: Lab IT and cybersecurity reviewer [src: S-MW-2]
- U-MW-5: QC coordinator / lab quality manager who reviews QC holds and corrective action [src: S-MW-4]
- U-MW-6: Ordering clinician who reads reported results in the EHR (indirect user) [src: S-MW-2]

## Value drivers (ranked)
- VD-MW-1: Interoperability: messages every supported LIS and interface engine accepts without custom work [src: S-MW-2]
- VD-MW-2: No data loss and no duplicated or out-of-order results [src: S-MW-2]
- VD-MW-3: Backward compatibility: existing site configurations keep working after upgrade [src: S-MW-2]
- VD-MW-4: Install and validation effort per site [src: S-MW-2]
- VD-MW-5: Visibility for the bench: what is happening to each result and why [src: S-MW-2]
- VD-MW-6: Only verified results reach clinicians: QC failures stop reporting before results reach the clinician's record [src: S-MW-4]

## Regulatory and quality context
- REG-MW-1: Middleware that applies result rules is usually regulated as a medical device or accessory; change control and validation records apply [src: S-MW-1]
- REG-MW-2: Interface changes require site-level interface validation evidence before go-live [src: S-MW-1]
- REG-MW-3: Audit trail and attribution of manual actions per 21 CFR Part 11 expectations [src: S-MW-1]
- REG-MW-4: Cybersecurity expectations for connected devices (e.g., FDA premarket cybersecurity guidance) [src: S-MW-1]
- REG-MW-5: CLIA QC requirements (42 CFR 493.1256), CAP checklist items and ISO 15189 set QC review and corrective action records [src: S-MW-3]
- REG-MW-6: QC rules and limits are lab policy, set by the lab director, not by software defaults [src: S-MW-3]

## Non-negotiable constraints
- C-MW-1: Only standard segments of the HL7 version the site already runs; no custom Z-segments unless the site has agreed to them [src: S-MW-1, S-MW-2]
- C-MW-2: New outbound messages are opt-in per interface; default behavior for existing sites does not change on upgrade [src: S-MW-2]
- C-MW-3: Every inbound instrument message is acknowledged and traceable end to end (message ID in, message ID out) [src: S-MW-2]
- C-MW-4: The middleware does not own user or role management; identity comes from the host system [src: S-MW-2]
- C-MW-5: Patient results run after a QC rejection are not reported until QC is acceptable and the lab documents corrective action [src: S-MW-4]
- C-MW-6: QC rule configuration changes are attributable, dated and require director-level approval [src: S-MW-4]
- C-MW-7: A QC event and its corrective action stay linked to the patient results it affected [src: S-MW-4]

## Requirement fields
- interface-impact: none, inbound, outbound or both, with the message type
- backward-compatible: yes, or no with the migration path
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, real-time, real time, timely, immediately, seamless, seamlessly,
appropriate, as needed, if necessary, robust, scalable, user-friendly, intuitive, etc, and/or

## Always ask
- Q-MW-1: Which LIS and interface engines must accept any new message, and which HL7 version do they run? [src: S-MW-2]
- Q-MW-2: Is the new behavior on by default, or configured per interface? [src: S-MW-2]
- Q-MW-3: What message volume and peak rate must this handle at the largest site? [src: S-MW-2]
- Q-MW-4: How will field teams validate this at a site without a full revalidation? [src: S-MW-2]
- Q-MW-5: Which QC rules and frequencies does the lab policy set for this test or reagent? [src: S-MW-4]
- Q-MW-6: What corrective action must be documented before patient results can be released? [src: S-MW-4]
- Q-MW-7: How are patient results run since the last acceptable QC identified for review? [src: S-MW-4]

## Sign-offs
- Product owner (middleware and result reporting)
- Interface / integration lead
- Field application or service lead
- Lab quality subject-matter expert
- Quality / regulatory affairs

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-MW-1: Interface and standards summary | type: standard | file: sources/middleware-reporting/S-MW-1_standards.md | owner: Integration lead | vetted: 2026-10-22 by Integration lead (fictional)
- S-MW-2: Middleware PO interview, J. Park (fictional) | type: interview | file: sources/middleware-reporting/S-MW-2_po-interview.md | owner: Middleware product owner | vetted: PENDING
- S-MW-3: QC and result-release regulations summary | type: standard | file: sources/middleware-reporting/S-MW-3_qc-regulations.md | owner: Quality / regulatory affairs | vetted: 2026-10-22 by Regulatory affairs reviewer (fictional)
- S-MW-4: Result-reporting and QC PO interview, M. Chen (fictional) | type: interview | file: sources/middleware-reporting/S-MW-4_qc-po-interview.md | owner: Middleware product owner | vetted: PENDING
