#!/usr/bin/env python3
"""Validate specification documents against the documentation conventions.

Checks every numbered document under specification/:
  1. Header line matches '# NNN – Title' (en-dash).
  2. Required header fields: Document ID, Version, Status, Category.
  3. Category matches the directory's range.
  4. References use en-dash ('DEVOS-SPEC-NNN – Title') and titles match
     the canonical document map.
  5. No calendar dates anywhere (Revision History stays 'TBD').
  6. File ends with the Revision History table plus a single newline.
  7. At least one mermaid diagram per document.
  8. Sequence diagrams have balanced alt/opt/loop ... end blocks.
  9. Forward-looking ranges (06x Enterprise, 07x Future) declare their
     activation gate and stay near the short length convention.

Exit code 0 on success, 1 on any failure.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / "specification"

TITLES = {
    "000": "Specification Governance", "001": "Executive Summary", "002": "Vision",
    "003": "Problem Statement", "004": "Design Philosophy", "005": "Guiding Principles",
    "006": "Terminology", "007": "Scope", "008": "Non Goals", "009": "Success Metrics",
    "010": "Glossary", "011": "Domain Model", "012": "Domain Relationships",
    "013": "Object Lifecycle", "014": "State Model", "015": "Object Ownership",
    "020": "Workspace Specification", "021": "Project Specification",
    "022": "Profile Specification", "023": "Environment Specification",
    "024": "Provider Specification", "025": "Connection Specification",
    "026": "Plugin Specification", "027": "Template Specification",
    "028": "Secret Specification", "029": "Workspace Manifest",
    "030": "System Architecture", "031": "Workspace Engine", "032": "Plugin Engine",
    "033": "Provider Engine", "034": "Connection Engine", "035": "Template Engine",
    "036": "Security Engine", "037": "Event System", "038": "Memory Engine",
    "039": "AI Router", "040": "CLI", "041": "Dashboard", "042": "Project Import",
    "043": "Project Detection", "044": "Workspace Lifecycle",
    "045": "Configuration System", "046": "Health System", "047": "Settings",
    "048": "Update System", "049": "Logging", "050": "SDK Overview",
    "051": "Plugin SDK", "052": "Provider SDK", "053": "Template SDK",
    "054": "Workspace SDK", "055": "API Specification", "056": "Hooks API",
    "057": "Events API", "058": "CLI API", "059": "Versioning Policy",
    "060": "Organizations", "061": "Teams", "062": "RBAC", "063": "Policy Engine",
    "064": "Cloud Sync", "065": "Audit System", "066": "Workspace Sharing",
    "067": "License Management", "068": "Remote Agents", "069": "Enterprise Roadmap",
    "070": "Marketplace", "071": "AI Agents", "072": "Research Platform",
    "073": "Desktop Platform", "074": "Web Platform", "075": "Mobile Platform",
    "076": "Cloud Platform", "077": "Ecosystem", "078": "V2 Roadmap",
    "079": "Future Vision",
}

CATEGORY_BY_DIR = {
    "00-overview": "Overview",
    "01-domain-model": "Domain Model",
    "02-foundation": "Foundation",
    "03-core-architecture": "Core Architecture",
    "04-platform": "Platform",
    "05-sdk": "SDK",
    "06-enterprise": "Enterprise",
    "07-future": "Future",
}

FORWARD_LOOKING = ("06-enterprise", "07-future")
MERMAID_TYPES = {"graph TD", "graph LR", "stateDiagram-v2", "sequenceDiagram", "classDiagram"}
ACTIVATION_RE = re.compile(r"(forward-looking|RFC and ADR|approved RFC and ADR)", re.I)


def check_document(path):
    problems = []
    text = path.read_text()
    rel = path.relative_to(REPO_ROOT)

    match = re.match(r".*/(\d{3})-", str(path))
    if not match:
        return [f"{rel}: filename lacks NNN- prefix"]
    num = match.group(1)

    if not text.startswith(f"# {num} – "):
        problems.append("header line must be '# NNN – Title' with en-dash")
    for field in ("**Document ID:** DEVOS-SPEC-%s" % num, "**Version:** 0.1", "**Status:** Draft"):
        if field not in text:
            problems.append(f"missing header field: {field}")
    category = CATEGORY_BY_DIR.get(path.parent.name)
    if f"**Category:** {category}" not in text:
        problems.append(f"missing Category '{category}'")

    for line_m in re.finditer(r"^.*DEVOS-SPEC-(\d{3}) – (.+)$", text, re.M):
        ref_num, candidate = line_m.group(1), line_m.group(2).strip()
        candidate = re.split(r"[.;]", candidate)[0].strip().rstrip(" .)]\"'")
        line = line_m.group(0)
        if ref_num not in TITLES:
            problems.append(f"unknown referenced ID DEVOS-SPEC-{ref_num}")
            continue
        want = TITLES[ref_num]
        if re.match(r"^\d{3}", candidate):
            continue  # range shorthand like '020 – 029' or '031 - 036
        if candidate == want or candidate.startswith(want + " ") or candidate.startswith(want + ","):
            continue
        if re.search(r"specifications$", candidate) or re.search(r"through\s+DEVOS-SPEC-\d{3}$", line[:line.rfind(candidate)].rstrip()):
            continue  # collective range references
        problems.append(f"title mismatch for {ref_num}: got '{candidate}' want '{want}'")
    for m in re.finditer(r"DEVOS-SPEC-\d{3} - [A-Z]", text):
        problems.append(f"plain-hyphen reference (use en-dash): {m.group(0)}")
    for m in re.finditer(r"\b20\d{2}\b", text):
        problems.append(f"calendar date token {m.group(0)}; only 'TBD' is permitted")

    raw = path.read_bytes()
    if not raw.endswith(b"|\n") or raw.endswith(b"\n\n"):
        problems.append("must end with revision table plus exactly one newline")
    if "| 0.1     | TBD  | DevOS Contributors | Initial Draft |" not in text:
        problems.append("missing canonical revision history row")

    blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
    if not blocks and path.parent.name != "00-overview":
        problems.append("no mermaid diagram found (Rule 16)")
    for block in blocks:
        first = block.strip().splitlines()[0].strip()
        if first not in MERMAID_TYPES:
            problems.append(f"non-canonical diagram type '{first}'")
        if first == "sequenceDiagram":
            depth = 0
            for line in block.splitlines():
                stripped = line.strip()
                if stripped.startswith(("alt ", "opt ", "loop ", "par ", "critical ", "break")):
                    depth += 1
                elif stripped == "end":
                    depth -= 1
                if depth < 0:
                    problems.append("stray 'end' in sequenceDiagram")
                    depth = 0
            if depth != 0:
                problems.append("unclosed alt/opt/loop in sequenceDiagram")

    if path.parent.name in FORWARD_LOOKING:
        lines = len(text.splitlines())
        if not ACTIVATION_RE.search(text):
            problems.append("forward-looking doc lacks RFC+ADR activation statement")
        if not (140 <= lines <= 260):
            problems.append(f"forward-looking length {lines} outside ~150-250 convention")
    return problems


def main():
    if not SPEC_DIR.is_dir():
        print(f"specification/ not found at {SPEC_DIR}", file=sys.stderr)
        return 1
    total = 0
    failures = 0
    for path in sorted(SPEC_DIR.rglob("[0-9]*-*.md")):
        total += 1
        for problem in check_document(path):
            failures += 1
            print(f"FAIL {path.relative_to(REPO_ROOT)}: {problem}")
    print(f"\nresult: {'FAILED' if failures else 'OK'} "
          f"({failures} problems across {total} documents)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
