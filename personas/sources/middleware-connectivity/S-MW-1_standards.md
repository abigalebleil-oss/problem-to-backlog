# S-MW-1 · Interface and standards summary for lab middleware

Type: standard summary. Written from public sources for the sandbox.

- HL7 v2.x (v2.5 common in labs): ORU^R01 for results; OBX-11 carries result status; NTE carries notes.
  Z-segments are site-specific extensions and require agreement with each site.
- CLSI LIS1 / LIS2 (formerly ASTM E1381 / E1394) define instrument-to-host messaging.
- Middleware that applies result rules is usually regulated as a medical device or accessory; change
  control and site interface validation records apply.
- FDA premarket cybersecurity guidance sets expectations for connected devices.
- 21 CFR Part 11 expectations apply to the audit trail and attribution of manual actions.
