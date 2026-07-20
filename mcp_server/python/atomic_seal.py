import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os/archives")

# Definite titles for the core and branch heads
TITLES = {
    "ceo.md": "Chief Executive Officer (CEO)",
    "cao.md": "Chief Agentic Officer (CAO)",
    "cko.md": "Chief Knowledge Officer (CKO)",
    "cso.md": "Chief Systems Officer (CSO)",
    "cfo.md": "Chief Financial Officer (CFO)",
    "chro.md": "Chief Human Resources Officer (CHRO)",
    "cmo.md": "Chief Marketing Officer (CMO)",
    "cro.md": "Chief Revenue Officer (CRO)",
    "coo.md": "Chief Operating Officer (COO)",
    "cae.md": "Chief Audit Executive (CAE)",
    "ceto.md": "Chief Ethics & Trust Officer (CETO)",
    "nexus_omni_lead.md": "Sovereign Proxy (Nexus Omni-Lead)",
    "nexus_orchestrator_agent.md": "Nexus Orchestrator Agent"
}

def atomic_seal():
    print("NexusOS Atomic Hierarchy Seal: HARDENING CORE...")

    for root, _, files in os.walk(str(BASE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Fix specific orphan patterns
                content = content.replace("Department Assistant", "Department Firmware")
                content = content.replace("Assistant to the CEO", "Firmware to the CEO")
                content = content.replace("Chief AI Officer", "Chief Agentic Officer (CAO)")

                # Ensure correct superiors for orphans found in audit
                if "department_firmware.md" in file or "assistant" in file:
                    # Map to the correct branch head
                    branch = path.parent.parent.name
                    if branch == "agentic": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Agentic Officer (CAO)", content)
                    if branch == "analytics": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Head of Analytics (CDO)", content)
                    if branch == "audit": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Audit Director", content)
                    if branch == "bizdev": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Head of Business Development", content)
                    if branch == "finance": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Financial Officer (CFO)", content)
                    if branch == "hr": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** VP of People Operations", content)
                    if branch == "legal": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** General Counsel (CLO)", content)
                    if branch == "marketing": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Marketing Officer (CMO)", content)
                    if branch == "operations": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Operating Officer (COO)", content)
                    if branch == "research": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Head of Research (Chief Scientist)", content)
                    if branch == "sales": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Chief Revenue Officer (CRO)", content)
                    if branch == "support": content = re.sub(r"\*\*Superior:\*\* .*", "**Superior:** Head of Customer Support", content)

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    print("Atomic Seal Complete.")

if __name__ == "__main__":
    atomic_seal()
