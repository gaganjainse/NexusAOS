import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, List

_python_root = Path(__file__).resolve().parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L1_Physiology.physiology_engine import PhysiologyEngine

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PULSE_DIR = BASE_DIR / "core/pulses"

# Pulse Sigils
SIGILS = {
    "ID": "[[ID]]",
    "BRANCH": "::B",
    "SUPERIOR": "::S",
    "PURPOSE": "::P",
    "RESPONSIBILITY": "::R",
    "DELIVERABLE": "::D",
    "AUTHORITY": "::A",
    "VERSION": "::V",
    "HOOK": "::H",
    "CONSTRAINT": "::L",
    "HASH": "::#",
    "WEIGHT": "::W",
    "SENTIMENT": "::Z"
}

PHYSIOLOGY = PhysiologyEngine(BASE_DIR)

def get_hash(text: str) -> str:
    """Generates a stable 8-character hex hash for the given text."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]

def parse_md_for_pulse(file_path: Path) -> str:
    """Converts a markdown artifact into a high-density Sesha Logic Pulse string."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    title_match = re.search(r"^# (?:Document|Role): (.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else file_path.stem

    pulse = [f"{SIGILS['ID']} {title}"]

    branch_match = re.search(r"\*\*Branch:\*\* (.+)$", content, re.MULTILINE)
    if branch_match: pulse.append(f"{SIGILS['BRANCH']} {branch_match.group(1).strip()}")

    superior_match = re.search(r"\*\*Superior:\*\* (.+)$", content, re.MULTILINE)
    if superior_match: pulse.append(f"{SIGILS['SUPERIOR']} {superior_match.group(1).strip()}")

    pulse.append(f"{SIGILS['VERSION']} 1.0")
    pulse.append(f"{SIGILS['WEIGHT']} {5 if 'Head' in title or 'Chief' in title or 'CEO' in title else 3}")

    purpose_match = re.search(r"## Purpose\n(.*?)\n\n", content, re.DOTALL)
    if purpose_match: pulse.append(f"{SIGILS['PURPOSE']} {purpose_match.group(1).strip().replace('\n', ' ')}")

    resp_match = re.search(r"## Responsibilities\n(.*?)\n\n##", content, re.DOTALL)
    if resp_match:
        for r in resp_match.group(1).strip().split("\n"):
            line = r.strip("- ").strip()
            if line: pulse.append(f"{SIGILS['RESPONSIBILITY']} {line}")

    def extract_table_lines(section_name: str, sigil: str):
        table_match = re.search(rf"## {section_name}\n\| (?:.+?)\n\| (?:.+?)\n(.*?)\n\n", content, re.DOTALL)
        if table_match:
            for line in table_match.group(1).strip().split("\n"):
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    pulse.append(f"{sigil} {parts[0]} > {parts[1]}")
                    if "Input for" in parts[1]:
                        target_role = re.search(r"Input for (.*)", parts[1])
                        if target_role:
                            pulse.append(f"{SIGILS['HOOK']} {parts[0]} -> {target_role.group(1).strip()}")

    extract_table_lines("Deliverables", SIGILS["DELIVERABLE"])
    extract_table_lines("Approval Authority", SIGILS["AUTHORITY"])

    constraints = re.findall(r"> \[!IMPORTANT\]\n> (.*)", content)
    for c in constraints:
        pulse.append(f"{SIGILS['CONSTRAINT']} {c.strip()}")

    current_vibe = PHYSIOLOGY.get_state()["endocrine"]["vibe"]
    pulse.append(f"{SIGILS['SENTIMENT']} {current_vibe.upper()}")

    full_pulse_text = "\n".join(pulse)
    pulse.append(f"{SIGILS['HASH']} {get_hash(full_pulse_text)}")

    return "\n".join(pulse)

def forge_pulses():
    """Compiles all markdown artifacts from archives into branch-level pulse files."""
    print("SeshaAOS Pulse Forge Initializing...")

    branch_pulses = {}
    SOURCE_DIR = BASE_DIR / "archives"

    all_known_ids = set()
    pending_pulses = []

    for root, _, files in os.walk(str(SOURCE_DIR)):
        if any(x in root for x in ["mcp_server", ".git", "nlg", "pulses"]):
            continue

        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    parts = file_path.relative_to(SOURCE_DIR).parts
                    branch_name = parts[1] if len(parts) > 1 and parts[0] == "roles" else "core"

                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    title_match = re.search(r"^# (?:Document|Role): (.+)$", content, re.MULTILINE)
                    node_id = title_match.group(1).strip() if title_match else file_path.stem
                    all_known_ids.add(node_id)

                    pending_pulses.append((branch_name, file_path, node_id))
                except: pass

    for branch_name, file_path, node_id in pending_pulses:
        try:
            pulse_str = parse_md_for_pulse(file_path)

            if node_id in ["Sesha Constitution", "Sesha OS Core Philosophy"]:
                save_branch = "00_foundation"
            else:
                save_branch = branch_name

            if save_branch not in branch_pulses:
                branch_pulses[save_branch] = []
            branch_pulses[save_branch].append(pulse_str)
        except Exception as e:
            print(f"Error pulsing {file_path.name}: {e}")

    for branch, pulses in branch_pulses.items():
        pulse_path = PULSE_DIR / f"{branch}.nxp"
        with open(pulse_path, "w", encoding="utf-8") as f:
            f.write("\n\n---Pulse-Break---\n\n".join(pulses))
        print(f"Forged: {pulse_path}")

    print(f"Pulse Forge Complete. {len(branch_pulses)} branch pulses generated.")

if __name__ == "__main__":
    forge_pulses()

