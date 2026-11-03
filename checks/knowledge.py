"""Load the three knowledge layers the skill is allowed to cite. No AI involved.

  company     knowledge/company.md                       K-n
  persona     personas/<id>.md                           U-, VD-, REG-, C-, Q-<PREFIX>-n
  initiative  initiatives/<INIT-ID>*/discovery.md         F-n
              initiatives/<INIT-ID>*/design.md            D-n, DC-n
              initiatives/<INIT-ID>*/feedback/*.md        verbatim quotes

Anything an output cites must exist in one of these, or be an ID the output itself defines.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSONA_DIR = ROOT / "personas"
COMPANY_FILE = ROOT / "knowledge" / "company.md"
INITIATIVE_DIR = ROOT / "initiatives"

ID_LINE = re.compile(r"^-\s+([A-Z]+(?:-[A-Z]+)?-\d+):\s*(.+?)\s*$")
PERSONA_ID = re.compile(r"^(U|VD|REG|C|Q)-([A-Z]{2,3})-(\d+)$")
SECTION = re.compile(r"^##\s+(.+?)\s*$")

PERSONA_SECTIONS = [
    "Domain", "Users", "Value drivers (ranked)", "Regulatory and quality context",
    "Non-negotiable constraints", "Requirement fields", "Banned terms", "Always ask",
    "Sign-offs", "Knowledge sources",
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
    """Return {ID: text} for '- ID: text' lines, in order."""
    found = {}
    for line in lines:
        m = ID_LINE.match(line)
        if m:
            found[m.group(1)] = m.group(2)
    return found


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
        self.ids = {}
        for name in ("Users", "Value drivers (ranked)", "Regulatory and quality context",
                     "Non-negotiable constraints", "Always ask"):
            self.ids.update(id_lines(self.sections.get(name, [])))

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
