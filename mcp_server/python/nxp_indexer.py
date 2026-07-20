import os
import json
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os")
PULSE_DIR = BASE_DIR / "core/pulses"
INDEX_PATH = PULSE_DIR / "master.nxi"

def build_nxi():
    """Builds a high-fidelity Graph Map index of all Nexus Pulse nodes."""
    print("Building Pulse Graph Index (.nxi)...")
    nodes = {}

    # 1. Parse all pulses
    for nxp_file in PULSE_DIR.glob("*.nxp"):
        with open(nxp_file, "r", encoding="utf-8") as f:
            content = f.read()

        pulses = content.split("---Pulse-Break---")
        for pulse in pulses:
            id_match = re.search(r"\[\[ID\]\] (.*)", pulse)
            if not id_match: continue

            node_id = id_match.group(1).strip()

            # Extract basic structure for the graph
            branch_match = re.search(r"::B (.*)", pulse)
            sup_match = re.search(r"::S (.*)", pulse)
            weight_match = re.search(r"::W (.*)", pulse)
            hash_match = re.search(r"::# (.*)", pulse)

            # Extract Hooks
            hooks = re.findall(r"::H (.*?) -> (.*)", pulse)

            nodes[node_id] = {
                "id": node_id,
                "file": nxp_file.name,
                "branch": branch_match.group(1).strip() if branch_match else "Core",
                "superior": sup_match.group(1).strip() if sup_match else "None",
                "weight": int(weight_match.group(1).strip()) if weight_match else 3,
                "hash": hash_match.group(1).strip() if hash_match else "None",
                "hooks": [{"out": h[0], "to": h[1]} for h in hooks],
                "downstream": [] # To be filled in second pass
            }

    # 2. Second Pass: Map Downstream (Subordinates)
    for node_id, data in nodes.items():
        superior = data["superior"]
        # Clean superior if it's a markdown link [Name](path)
        clean_sup = superior
        if "[" in superior and "]" in superior:
            link_match = re.search(r"\[(.*?)\]", superior)
            if link_match: clean_sup = link_match.group(1).strip()

        if clean_sup in nodes:
            nodes[clean_sup]["downstream"].append(node_id)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(nodes, f, indent=4)

    print(f"Graph Index Built: {INDEX_PATH} ({len(nodes)} logic nodes)")

if __name__ == "__main__":
    build_nxi()
