import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "archives"

def get_node_id(content: str) -> str:
    match = re.search(r"^# (?:Role|Document): (.*)", content, re.MULTILINE)
    return match.group(1).strip() if match else None

def seal():
    print("NexusOS Global Lattice Sync: Final Hardening...")

    # 1. Build Title Map: CleanTitle -> ActualTitleFromHeader
    title_map = {}
    for root, _, files in os.walk(str(BASE_DIR)):
        for file in files:
            if file.endswith(".md"):
                with open(Path(root)/file, "r", encoding="utf-8") as f:
                    content = f.read()
                node_id = get_node_id(content)
                if node_id:
                    # Map simple keyword and full title to the actual header
                    simple = file.replace(".md", "").replace("_", " ").lower()
                    title_map[simple] = node_id
                    title_map[node_id.lower()] = node_id

    # 2. Hardcoded Superior Logic (Functional Mapping)
    def resolve_superior(file_name, branch, dept, current_val):
        clean_val = current_val.lower().replace("[", "").replace("]", "").split("(")[0].strip()

        # Priority 1: Exact matches in title_map
        if clean_val in title_map: return title_map[clean_val]

        # Priority 2: Keyword mapping
        if "sovereign" in clean_val: return "THE SOVEREIGN"
        if "ceo" in clean_val: return "Chief Executive Officer (CEO)"
        if "cao" in clean_val: return "Chief Agentic Officer (CAO)"
        if "cko" in clean_val: return "Chief Knowledge Officer (CKO)"
        if "cso" in clean_val: return "Chief Systems Officer (CSO)"
        if "cfo" in clean_val: return "Chief Financial Officer (CFO)"
        if "chro" in clean_val: return "Chief Human Resources Officer (CHRO)"
        if "cmo" in clean_val: return "Chief Marketing Officer (CMO)"
        if "cro" in clean_val: return "Chief Revenue Officer (CRO)"
        if "coo" in clean_val: return "Chief Operating Officer (COO)"
        if "cae" in clean_val: return "Chief Audit Executive (CAE)"

        # Priority 3: Branch Hierarchy Fallback
        if branch and branch in title_map: return title_map[branch]

        return "None"

    # 3. Apply Fixes
    for root, _, files in os.walk(str(BASE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                parts = path.relative_to(BASE_DIR).parts
                branch = parts[1] if len(parts) > 1 else None
                dept = parts[2] if len(parts) > 2 else None

                # Match Superior
                match = re.search(r"\*\*Superior:\*\* (.*)", content)
                if match:
                    current_sup = match.group(1).strip()
                    new_sup = resolve_superior(file, branch, dept, current_sup)

                    if new_sup != current_sup:
                        content = content.replace(match.group(0), f"**Superior:** {new_sup}")

                # Footer fix
                content = re.sub(r"\[Superior: (.*?)\]\(.*?\)",
                                lambda m: f"[Superior: {resolve_superior(file, branch, dept, m.group(1))}]" + "(./site_map.md)",
                                content)

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

    print("Lattice Sealed.")

if __name__ == "__main__":
    seal()
