import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os")
ARCHIVE_DIR = BASE_DIR / "archives"

# 1. Systematic Name Map
RENAME_MAP = {
    "AI": "Agentic",
    "Assistant": "Firmware",
    "Implementer": "Technician",
    "Task": "Directive",
    "Tasks": "Directives",
    "User": "Sovereign"
}

# 2. Definitive Hierarchy (Filename -> Superior Filename)
HIERARCHY = {
    # Ultimate Command
    "nexus_omni_lead.md": "SOVEREIGN",
    "nexus_orchestrator_agent.md": "nexus_omni_lead.md",
    "nexus_input_parser_agent.md": "nexus_orchestrator_agent.md",
    "oracle_interface_agent.md": "nexus_orchestrator_agent.md",
    "learning_synthesis_agent.md": "nexus_omni_lead.md",
    "system_health_supervisor.md": "nexus_omni_lead.md",

    # Executive
    "ceo.md": "board_of_directors.md",
    "board_of_directors.md": "SOVEREIGN",
    "cao.md": "ceo.md",
    "cko.md": "ceo.md",
    "cso.md": "ceo.md",
    "cae.md": "ceo.md",
    "coo.md": "ceo.md",
    "chro.md": "ceo.md",
    "cmo.md": "ceo.md",
    "cro.md": "ceo.md",
    "ceto.md": "ceo.md",
    "chief_ethics_officer.md": "ceo.md",
    "general_counsel.md": "ceo.md",
    "head_research.md": "ceo.md",
    "head_bizdev.md": "ceo.md",
    "head_support.md": "ceo.md",
    "head_analytics.md": "ceo.md",

    # Branch: Agentic
    "agentic_engineer.md": "vp_agentic_workflows.md",
    "vp_agentic_workflows.md": "cao.md",
    "agentic_knowledge_lead.md": "cao.md",
    "head_model_governance.md": "cao.md",
    "nexus_logic_engine.md": "cao.md",
    "specialization_agent.md": "cao.md",
    "model_auditor.md": "head_model_governance.md",
    "self_repair_agent.md": "cko.md",
    "global_dependency_agent.md": "cko.md",
    "structural_efficiency_agent.md": "cko.md"
}

def clean_title(filename):
    name = filename.replace(".md", "").replace("_", " ")
    words = name.split()
    capitalized = []
    for w in words:
        if w.lower() in ["ai", "bi", "qa", "sdr", "sme", "ip", "hq", "ncc", "ceo", "cfo", "cko", "cso", "coo", "chro", "cmo", "cro", "cae", "ceto", "ciso", "cao"]:
            capitalized.append(w.upper())
        elif w.lower() == "fpa": capitalized.append("FP&A")
        else: capitalized.append(w.capitalize())
    title = " ".join(capitalized)
    if "Cao" in title: title = title.replace("Cao", "(CAO)") # Fix for CAO
    return title

def lock():
    print("NexusAOS Systematic Hierarchy Lock: SECURING SKELETON...")

    # Pre-build titles map for all files in archives
    file_to_title = {}
    for root, _, files in os.walk(str(ARCHIVE_DIR)):
        for file in files:
            if file.endswith(".md"):
                file_to_title[file] = clean_title(file)

    for root, _, files in os.walk(str(ARCHIVE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 1. Systematic Text Replacement
                for old, new in RENAME_MAP.items():
                    content = re.sub(rf"\b{old}\b", new, content)
                    content = re.sub(rf"\b{old.lower()}\b", new.lower(), content)

                # 2. Fix Header
                title = file_to_title[file]
                prefix = "Role" if "roles" in str(path) else "Document"
                content = re.sub(r"^# (?:Role|Document): .*", f"# {prefix}: {title}", content, flags=re.MULTILINE)

                # 3. Secure Superior Line
                superior_title = "None"
                if file in HIERARCHY:
                    sup_target = HIERARCHY[file]
                    if sup_target == "SOVEREIGN": superior_title = "THE SOVEREIGN"
                    elif sup_target in file_to_title: superior_title = file_to_title[sup_target]
                    else: superior_title = clean_title(sup_target)
                else:
                    # Generic fallback: search for lead in same branch
                    pass

                content = re.sub(r"\*\*Superior:\*\* .*", f"**Superior:** {superior_title}", content)
                content = re.sub(r"\[Superior: .*?\]\(.*?\)", f"[Superior: {superior_title}](./site_map.md)", content)

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

    print("Hierarchy Locked.")

if __name__ == "__main__":
    lock()
