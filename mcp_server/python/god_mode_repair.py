import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os/archives")

# Definitive Map
MAP = {
    "cao.md": "Chief Agentic Officer (CAO)",
    "ceo.md": "Chief Executive Officer (CEO)",
    "cko.md": "Chief Knowledge Officer (CKO)",
    "cso.md": "Chief Systems Officer (CSO)",
    "cfo.md": "Chief Financial Officer (CFO)",
    "chro.md": "Chief Human Resources Officer (CHRO)",
    "cmo.md": "Chief Marketing Officer (CMO)",
    "cro.md": "Chief Revenue Officer (CRO)",
    "coo.md": "Chief Operating Officer (COO)",
    "cae.md": "Chief Audit Executive (CAE)",
    "ceto.md": "Chief Ethics & Trust Officer (CETO)",
    "chief_ethics_officer.md": "Chief Ethics & Trust Officer (CETO)",
    "ciso.md": "Chief Information Security Officer (CISO)",
    "nexus_omni_lead.md": "Sovereign Proxy (Nexus Omni-Lead)",
    "nexus_orchestrator_agent.md": "Nexus Orchestrator Agent",
    "nexus_input_parser_agent.md": "Nexus Input Parser Agent",
    "oracle_interface_agent.md": "Oracle Interface Agent (OIA)",
    "learning_synthesis_agent.md": "Learning Synthesis Agent",
    "system_health_supervisor.md": "System Health Supervisor",
    "board_of_directors.md": "Board of Directors",
    "chief_of_staff.md": "Chief of Staff",
    "internal_comms_lead.md": "Internal Communications Lead",
    "audit_director.md": "Audit Director"
}

HIERARCHY = {
    "agentic_department_firmware.md": "Chief Agentic Officer (CAO)",
    "analytics_department_firmware.md": "Head of Analytics (CDO)",
    "audit_department_firmware.md": "Audit Director",
    "bizdev_department_firmware.md": "Head of Business Development",
    "finance_department_firmware.md": "Chief Financial Officer (CFO)",
    "hr_department_firmware.md": "Chief Human Resources Officer (CHRO)",
    "legal_department_firmware.md": "General Counsel (CLO)",
    "marketing_department_firmware.md": "Chief Marketing Officer (CMO)",
    "ops_department_firmware.md": "Chief Operating Officer (COO)",
    "research_department_firmware.md": "Head of Research (Chief Scientist)",
    "sales_department_firmware.md": "Chief Revenue Officer (CRO)",
    "support_department_firmware.md": "Head of Customer Support"
}

def clean_title(filename):
    if filename in MAP: return MAP[filename]
    name = filename.replace(".md", "").replace("_", " ")
    words = name.split()
    capitalized = []
    for w in words:
        if w.lower() in ["ai", "bi", "qa", "sdr", "sme", "ip", "hq", "ncc", "ceo", "cfo", "cko", "cso", "coo", "chro", "cmo", "cro", "cae", "ceto", "ciso", "cao"]:
            capitalized.append(w.upper())
        elif w.lower() == "fpa": capitalized.append("FP&A")
        else: capitalized.append(w.capitalize())
    return " ".join(capitalized)

def repair():
    print("NexusOS God-Mode Repair: Total Synchronization...")
    for root, _, files in os.walk(str(BASE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                title = clean_title(file)
                # Fix Header
                prefix = "Role" if "roles" in str(path) else "Document"
                content = re.sub(r"^# (?:Role|Document): .*", f"# {prefix}: {title}", content, flags=re.MULTILINE)

                # Fix Superior
                if file in HIERARCHY:
                    content = re.sub(r"\*\*Superior:\*\* .*", f"**Superior:** {HIERARCHY[file]}", content)
                elif "cao.md" in file:
                     content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Executive Officer (CEO)", content)
                elif "ceo.md" in file:
                     content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Board of Directors", content)
                elif "cko.md" in file or "cso.md" in file or "cfo.md" in file:
                     content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Executive Officer (CEO)", content)

                # Terminology
                content = content.replace("AI Assistant", "Agentic Firmware")
                content = content.replace("Department Assistant", "Department Firmware")

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    print("God-Mode Sync Complete.")

if __name__ == "__main__":
    repair()
