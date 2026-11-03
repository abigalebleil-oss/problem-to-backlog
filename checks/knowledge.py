"""Load the three knowledge layers the skill is allowed to cite. No AI involved.

  company     knowledge/company.md                       K-n
  persona     personas/<id>.md                           U-, VD-, REG-, C-, Q-<PREFIX>-n
  initiative  initiatives/<INIT-ID>*/discovery.md         F-n
              initiatives/<INIT-ID>*/design.md            D-n, DC-n
              initiatives/<INIT-ID>*/feedback/*.md        verbatim quotes

Anything an output cites must exist in one of these, or be an ID the output itself defines.

Provenance: every ID line in a persona or in company knowledge ends with [src: S-...], and every
source is registered in that file's "## Sources" section with a file, an owner and a vetting
record. That is what lets the plan trace each citation back to vetted, local data.
"""

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSONA_DIR = ROOT / "personas"
COMPANY_FILE = ROOT / "knowledge" / "company.md"
INITIATIVE_DIR = ROOT / "initiatives"

ID_LINE = re.compile(r"^-\s+([A-Z]+(?:-[A-Z]+)?-\d+):\s*(.+?)\s*$")
PERSONA_ID = re.compile(r"^(U|VD|REG|C|Q)-([A-Z]{2,3})-(\d+)$")
SECTION = re.compile(r"^##\s+(.+?)\s*$")

SRC_TAG = re.compile(r"\s*\[src:\s*([^\]]+)\]\s*$")
SOURCE_LINE = re.compile(
    r"^-\s+(S-[A-Z]{2,3}-\d+):\s*(.+?)\s*\|\s*type:\s*(\w+)\s*\|\s*file:\s*(\S+)\s*"
    r"\|\s*owner:\s*(.+?)\s*\|\s*vetted:\s*(.+?)\s*$")
VETTED = re.compile(r"^(\d{4}-\d{2}-\d{2}) by (.+)$")
SOURCE_TYPES = {"interview", "standard", "sop", "data", "experience", "document"}
STALE_AFTER_DAYS = 365

PERSONA_SECTIONS = [
    "Domain", "Users", "Value drivers (ranked)", "Regulatory and quality context",
    "Non-negotiable constraints", "Requirement fields", "Banned terms", "Always ask",
    "Sign-offs", "Sources",
]
COMPANY_BANNED = ["promptly", "quickly", "user-friendly", "appropriate", "as needed", "etc", "and/or"]


def sections(text):
    """Return {section title: [lines]} for '## ' sections."""
    out, current = {}, None
    for line in text.splitlines():
        m = SECTION.match(line)
        if m:
            current = m.group(1)
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return out


def id_lines(lines):
    """Return {ID: text} for '- ID: text' lines, in order. Any [src: ...] tag is stripped."""
    return {k: v[0] for k, v in id_lines_with_sources(lines).items()}


def id_lines_with_sources(lines):
    """Return {ID: (text, [source IDs])} for '- ID: text [src: S-..]' lines."""
    found = {}
    for line in lines:
        m = ID_LINE.match(line)
        if m and not m.group(1).startswith("S-"):
            text, srcs = m.group(2), []
            tag = SRC_TAG.search(text)
            if tag:
                srcs = [s.strip() for s in tag.group(1).split(",") if s.strip()]
                text = text[:tag.start()].rstrip()
            found[m.group(1)] = (text, srcs)
    return found


class Source:
    def __init__(self, m, base_dir):
        self.id, self.title, self.type, self.file, self.owner, self.vetted_raw = m.groups()
        self.path = base_dir / self.file
        v = VETTED.match(self.vetted_raw)
        self.vetted_on = date.fromisoformat(v.group(1)) if v else None
        self.vetted_by = v.group(2) if v else None

    @property
    def vetted(self):
        return self.vetted_on is not None

    @property
    def stale(self):
        return self.vetted and (date.today() - self.vetted_on).days > STALE_AFTER_DAYS

    @property
    def label(self):
        return f"vetted {self.vetted_on} by {self.vetted_by}" if self.vetted else "NOT VETTED"


def parse_sources(lines, base_dir):
    out = {}
    for line in lines:
        m = SOURCE_LINE.match(line)
        if m:
            out[m.group(1)] = Source(m, base_dir)
    return out


def header_value(text, key):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", text, re.M)
    return m.group(1) if m else None


class Persona:
    def __init__(self, path):
        self.path = Path(path)
        self.text = self.path.read_text()
        m = re.search(r"^# Persona:\s*(.+)$", self.text, re.M)
        self.title = m.group(1).strip() if m else None
        self.id = header_value(self.text, "id")
        self.prefix = header_value(self.text, "prefix")
        self.status = header_value(self.text, "status")
        self.sections = sections(self.text)
        self.ids, self.line_sources = {}, {}
        for name in ("Users", "Value drivers (ranked)", "Regulatory and quality context",
                     "Non-negotiable constraints", "Always ask"):
            for k, (text, srcs) in id_lines_with_sources(self.sections.get(name, [])).items():
                self.ids[k] = text
                self.line_sources[k] = srcs
        self.sources = parse_sources(self.sections.get("Sources", []), self.path.parent)
        self.source_lines = [l for l in self.sections.get("Sources", []) if l.startswith("- ")]

    def of_type(self, kind):
        return {k: v for k, v in self.ids.items() if k.startswith(kind + "-")}

    @property
    def users(self):
        return self.of_type("U")

    @property
    def value_drivers(self):
        return self.of_type("VD")

    @property
    def constraints(self):
        return self.of_type("C")

    @property
    def questions(self):
        return self.of_type("Q")

    @property
    def required_fields(self):
        fields = []
        for line in self.sections.get("Requirement fields", []):
            m = re.match(r"^-\s+([a-z][a-z-]*):", line)
            if m:
                fields.append(m.group(1))
        return fields

    @property
    def banned_terms(self):
        raw = " ".join(self.sections.get("Banned terms", []))
        return [t.strip().lower() for t in raw.split(",") if t.strip()]


def load_persona(persona_id):
    path = PERSONA_DIR / f"{persona_id}.md"
    return Persona(path) if path.exists() else None


def list_personas():
    return [Persona(p) for p in sorted(PERSONA_DIR.glob("*.md")) if not p.name.startswith("_")]


def company_ids():
    return id_lines(COMPANY_FILE.read_text().splitlines())


def company_provenance():
    """Return ({K-ID: (text, [src])}, {S-ID: Source}) for company knowledge."""
    secs = sections(COMPANY_FILE.read_text())
    lines = [l for name, ls in secs.items() if name != "Sources" for l in ls]
    return id_lines_with_sources(lines), parse_sources(secs.get("Sources", []), COMPANY_FILE.parent)


class Initiative:
    def __init__(self, init_id):
        matches = sorted(INITIATIVE_DIR.glob(f"{init_id}*"))
        self.id = init_id
        self.dir = matches[0] if matches else None
        self.findings, self.design, self.feedback = {}, {}, {}
        if self.dir is None:
            return
        disc = self.dir / "discovery.md"
        des = self.dir / "design.md"
        if disc.exists():
            self.findings = id_lines(disc.read_text().splitlines())
        if des.exists():
            self.design = id_lines(des.read_text().splitlines())
        for f in sorted((self.dir / "feedback").glob("*.md")):
            self.feedback[f.name] = f.read_text()

    @property
    def found(self):
        return self.dir is not None

    @property
    def design_elements(self):
        return {k: v for k, v in self.design.items() if re.match(r"^D-\d+$", k)}

    @property
    def ids(self):
        return {**self.findings, **self.design}
