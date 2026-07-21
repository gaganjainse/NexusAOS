import json
import os
from pathlib import Path

# Configuration
BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os")
PULSE_DIR = BASE_DIR / "core/pulses"
INDEX_PATH = PULSE_DIR / "master.nxi"

def audit_lattice():
    """Performs a comprehensive structural audit on the Nexus Pulse Lattice."""
    print("NexusAOS Lattice Integrity Audit Initializing...")

    if not INDEX_PATH.exists():
        print("Error: Pulse Index not found. Run Forge/Indexer first.")
        return

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    errors = []
    warnings = []

    # 1. Orphan Check (Disconnected from Superior)
    for node_id, data in nodes.items():
        superior = data["superior"]
        # Basic clean-up for link syntax
        if "[" in superior: superior = superior.split("[")[1].split("]")[0]

        if superior != "None" and superior not in nodes:
            # Check for common non-role superior placeholders
            if superior not in ["THE SOVEREIGN", "THE USER", "Board of Directors"]:
                errors.append(f"ORPHAN NODE: '{node_id}' reports to unknown superior '{superior}'")

    # 2. Terminal Node Check (Roles with no subordinates - legitimate but good to track)
    terminal_nodes = [id for id, data in nodes.items() if not data["downstream"]]
    print(f"Audit Metric: {len(terminal_nodes)} terminal personnel roles detected.")

    # 3. Logic Loop Check (Circular Reporting)
    def check_circular(node_id, visited):
        if node_id in visited:
            return True
        visited.add(node_id)
        superior = nodes[node_id]["superior"]
        if "[" in superior: superior = superior.split("[")[1].split("]")[0]

        if superior in nodes:
            return check_circular(superior, visited)
        return False

    for node_id in nodes:
        if check_circular(node_id, set()):
             errors.append(f"LOGIC LOOP: Circular reporting detected at '{node_id}'")

    # 4. Hash Verification
    for node_id, data in nodes.items():
        if data["hash"] == "None":
            warnings.append(f"UNSECURED NODE: '{node_id}' is missing an integrity hash.")

    # Summary
    print("\n--- Audit Summary ---")
    print(f"Total Nodes: {len(nodes)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nERRORS DETECTED:")
        for err in errors: print(f"  [!] {err}")

    if warnings:
        print("\nWARNINGS:")
        for warn in warnings: print(f"  [-] {warn}")

    if not errors:
        print("\nSKELETON HARDENED: All reporting circuits verified.")

if __name__ == "__main__":
    audit_lattice()
