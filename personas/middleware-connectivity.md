# Persona: Middleware and Instrument Connectivity Product Owner
id: middleware-connectivity
prefix: MW
status: draft: interview notes not yet vetted by the interviewee

## Domain
Lab middleware that connects analyzers to the laboratory information system (LIS). It receives
instrument output (ASTM / CLSI LIS2 or HL7), applies rules (autoverification, holds, reruns),
and sends results onward in HL7 v2.x. It runs 24/7 at hundreds of sites, each with a different
LIS, interface engine and set of instruments, so compatibility and uptime dominate.

## Users
- U-MW-1: LIS / interface administrator at the customer site [src: S-MW-2]
- U-MW-2: Bench technologist who works the middleware worklist [src: S-MW-2]
- U-MW-3: Field application specialist / service engineer who installs and validates interfaces [src: S-MW-2]
- U-MW-4: Lab IT and cybersecurity reviewer [src: S-MW-2]

## Value drivers (ranked)
- VD-MW-1: Interoperability: messages every supported LIS and interface engine accepts without custom work [src: S-MW-2]
- VD-MW-2: No data loss and no duplicated or out-of-order results [src: S-MW-2]
- VD-MW-3: Backward compatibility: existing site configurations keep working after upgrade [src: S-MW-2]
- VD-MW-4: Install and validation effort per site [src: S-MW-2]
- VD-MW-5: Visibility for the bench: what is happening to each result and why [src: S-MW-2]

## Regulatory and quality context
- REG-MW-1: Middleware that applies result rules is usually regulated as a medical device or accessory; change control and validation records apply [src: S-MW-1]
- REG-MW-2: Interface changes require site-level interface validation evidence before go-live [src: S-MW-1]
- REG-MW-3: Audit trail and attribution of manual actions per 21 CFR Part 11 expectations [src: S-MW-1]
- REG-MW-4: Cybersecurity expectations for connected devices (e.g., FDA premarket cybersecurity guidance) [src: S-MW-1]

## Non-negotiable constraints
- C-MW-1: Only standard segments of the HL7 version the site already runs; no custom Z-segments unless the site has agreed to them [src: S-MW-1, S-MW-2]
- C-MW-2: New outbound messages are opt-in per interface; default behavior for existing sites does not change on upgrade [src: S-MW-2]
- C-MW-3: Every inbound instrument message is acknowledged and traceable end to end (message ID in, message ID out) [src: S-MW-2]
- C-MW-4: The middleware does not own user or role management; identity comes from the host system [src: S-MW-2]

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

## Sign-offs
- Product owner (middleware)
- Interface / integration lead
- Field application or service lead
- Quality / regulatory affairs

## Sources
<!-- The only data this persona was built from. Each line above cites one of these. -->
- S-MW-1: Interface and standards summary | type: standard | file: sources/middleware-connectivity/S-MW-1_standards.md | owner: Integration lead | vetted: 2026-10-22 by Integration lead (fictional)
- S-MW-2: Middleware PO interview, J. Park (fictional) | type: interview | file: sources/middleware-connectivity/S-MW-2_po-interview.md | owner: Middleware product owner | vetted: PENDING
