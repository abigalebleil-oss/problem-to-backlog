# Persona: <Role title, e.g. "Hematology Analyzer Software Product Owner">
id: <kebab-case-id>
prefix: <2–3 capital letters, unique across personas>
status: draft

<!-- Create your own persona by copying this file, or run the create-persona skill to be
     interviewed. Every line that starts with "- <TYPE>-<PREFIX>-<n>:" is an ID the skill can
     cite and the checks can verify. Every such line ends with [src: S-...] naming the source it
     came from. Save each source (interview notes, SOP excerpt, standards summary, data export)
     under personas/sources/<id>/ and register it under ## Sources. Mark a source vetted only
     after its owner has reviewed it; set status to "validated" only when all sources are vetted.
     Run `python checks/checks.py persona personas/<file>.md` when done. -->

## Domain
<Two to four sentences: what the software does, where it sits, what goes wrong when it fails.>

## Users
- U-XX-1: <user role> [src: S-XX-1]

## Value drivers (ranked)
- VD-XX-1: <what this domain's customers care about most, stated as an outcome> [src: S-XX-1]
- VD-XX-2: <second> [src: S-XX-1]

## Regulatory and quality context
- REG-XX-1: <regulation, standard or internal SOP that shapes requirements> [src: S-XX-1]

## Non-negotiable constraints
- C-XX-1: <a rule the plan may never weaken> [src: S-XX-1]

## Requirement fields
- verification: test, inspection, analysis or demonstration

## Banned terms
promptly, quickly, user-friendly, appropriate, as needed, etc

## Always ask
- Q-XX-1: <question an experienced PO in this domain always asks first> [src: S-XX-1]

## Sign-offs
- <role that must approve before work enters the backlog>

## Sources
- S-XX-1: <title> | type: <interview|standard|sop|data|experience|document> | file: sources/<id>/<file>.md | owner: <role> | vetted: <YYYY-MM-DD by name/role, or PENDING>
