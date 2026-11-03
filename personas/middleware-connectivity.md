# Persona: Middleware and Instrument Connectivity Product Owner
id: middleware-connectivity
prefix: MW
status: seeded from public knowledge; validate with a middleware PO before production use

## Domain
Lab middleware that connects analyzers to the laboratory information system (LIS). It receives
instrument output (ASTM / CLSI LIS2 or HL7), applies rules (autoverification, holds, reruns),
and sends results onward in HL7 v2.x. It runs 24/7 at hundreds of sites, each with a different
LIS, interface engine and set of instruments, so compatibility and uptime dominate.

## Users
- U-MW-1: LIS / interface administrator at the customer site
- U-MW-2: Bench technologist who works the middleware worklist
- U-MW-3: Field application specialist / service engineer who installs and validates interfaces
- U-MW-4: Lab IT and cybersecurity reviewer

## Value drivers (ranked)
- VD-MW-1: Interoperability: messages every supported LIS and interface engine accepts without custom work
- VD-MW-2: No data loss and no duplicated or out-of-order results
- VD-MW-3: Backward compatibility: existing site configurations keep working after upgrade
- VD-MW-4: Install and validation effort per site
- VD-MW-5: Visibility for the bench: what is happening to each result and why

## Regulatory and quality context
- REG-MW-1: Middleware that applies result rules is usually regulated as a medical device or accessory; change control and validation records apply
- REG-MW-2: Interface changes require site-level interface validation evidence before go-live
- REG-MW-3: Audit trail and attribution of manual actions per 21 CFR Part 11 expectations
- REG-MW-4: Cybersecurity expectations for connected devices (e.g., FDA premarket cybersecurity guidance)

## Non-negotiable constraints
- C-MW-1: Only standard segments of the HL7 version the site already runs; no custom Z-segments unless the site has agreed to them
- C-MW-2: New outbound messages are opt-in per interface; default behavior for existing sites does not change on upgrade
- C-MW-3: Every inbound instrument message is acknowledged and traceable end to end (message ID in, message ID out)
- C-MW-4: The middleware does not own user or role management; identity comes from the host system

## Requirement fields
- interface-impact: none, inbound, outbound or both, with the message type
- backward-compatible: yes, or no with the migration path
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, fast, real-time, real time, timely, immediately, seamless, seamlessly,
appropriate, as needed, if necessary, robust, scalable, user-friendly, intuitive, etc, and/or

## Always ask
- Q-MW-1: Which LIS and interface engines must accept any new message, and which HL7 version do they run?
- Q-MW-2: Is the new behavior on by default, or configured per interface?
- Q-MW-3: What message volume and peak rate must this handle at the largest site?
- Q-MW-4: How will field teams validate this at a site without a full revalidation?

## Sign-offs
- Product owner (middleware)
- Interface / integration lead
- Field application or service lead
- Quality / regulatory affairs

## Knowledge sources
- Seeded by Claude from public standards (HL7 v2.x, CLSI LIS1/LIS2) and general domain knowledge.
  Replace with a recorded interview with a middleware PO using the create-persona skill.
