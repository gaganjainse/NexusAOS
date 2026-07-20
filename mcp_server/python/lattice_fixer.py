import os
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARCHIVE_DIR = BASE_DIR / "archives"

# Known valid titles (The systematic target state)
VALID_TITLES = [
    "Chief Agentic Officer (CAO)", "Chief Executive Officer (CEO)", "Chief Financial Officer (CFO)",
    "Chief Knowledge Officer (CKO)", "Chief Systems Officer (CSO)", "Chief Operating Officer (COO)",
    "Chief Human Resources Officer (CHRO)", "Chief Marketing Officer (CMO)", "Chief Revenue Officer (CRO)",
    "Chief Audit Executive (CAE)", "Chief Ethics & Trust Officer (CETO)", "Chief Information Security Officer (CISO)",
    "Sovereign Proxy (Nexus Omni-Lead)", "Nexus Orchestrator Agent", "VP of Agentic Workflows",
    "Head Model Governance", "Audit Director", "Head of Analytics (CDO)", "Head of Business Intelligence (BI)",
    "VP of Data Science", "VP of Finance (FP&A)", "Corporate Controller", "VP of People Operations",
    "General Counsel (CLO)", "VP of Legal (Corporate)", "Head of Workplace & Facilities",
    "Internal Infrastructure Lead", "Internal Systems Manager (Internal Services)",
    "Head of Research (Chief Scientist)", "SDR Manager (Sales Development)",
    "Customer Success Manager (CSM)", "Head of Customer Support",
    "Implementation Support Lead (Tier 2/3)", "Oracle Interface Design Manager",
    "Role: [PLATFORM_A] Lead", "Role: [PLATFORM_B] Lead", "Audit Planning Manager",
    "Audit Remediation Lead (Validation Supervisor)", "Findings & Reporting Lead",
    "Audit Knowledge Lead (Branch HQ)", "Tax Manager", "Treasury Manager",
    "Board of Directors", "Chief of Staff", "HR Manager (Personnel Relations)",
    "Payroll & Benefits Manager", "Head of Talent Acquisition", "Senior Recruiter",
    "Recruiter", "Contract Manager", "Creative Director", "Copy Chief", "Art Director",
    "Performance Marketing Manager", "[CORE_DOMAIN] Research Director", "Systems Innovation Lead",
    "Support Supervisor", "Support Operations Manager", "THE SOVEREIGN", "None"
]

# Map common input patterns to their target title
S_MAP = {
    "CAO": "Chief Agentic Officer (CAO)",
    "CAO / CKO": "Chief Agentic Officer (CAO)",
    "CEO": "Chief Executive Officer (CEO)",
    "CFO": "Chief Financial Officer (CFO)",
    "CKO": "Chief Knowledge Officer (CKO)",
    "CSO": "Chief Systems Officer (CSO)",
    "COO": "Chief Operating Officer (COO)",
    "CHRO": "Chief Human Resources Officer (CHRO)",
    "CMO": "Chief Marketing Officer (CMO)",
    "CRO": "Chief Revenue Officer (CRO)",
    "CAE": "Chief Audit Executive (CAE)",
    "CETO": "Chief Ethics & Trust Officer (CETO)",
    "CISO": "Chief Information Security Officer (CISO)",
    "Omni-Lead": "Sovereign Proxy (Nexus Omni-Lead)",
    "Sovereign Proxy": "Sovereign Proxy (Nexus Omni-Lead)",
    "Nexus Orchestrator": "Nexus Orchestrator Agent",
    "Head of Analytics": "Head of Analytics (CDO)",
    "Head of BI": "Head of Business Intelligence (BI)",
    "VP of Finance": "VP of Finance (FP&A)",
    "VP of People Ops": "VP of People Operations",
    "VP of Legal": "VP of Legal (Corporate)",
    "General Counsel": "General Counsel (CLO)",
    "Head of Workplace": "Head of Workplace & Facilities",
    "Head of Research": "Head of Research (Chief Scientist)",
    "Head of Support": "Head of Customer Support",
    "Audit Planning Manager": "Audit Planning Manager",
    "Audit Remediation Lead": "Audit Remediation Lead (Validation Supervisor)",
    "Audit Knowledge Lead": "Audit Knowledge Lead (Branch HQ)",
    "Internal Systems Manager": "Internal Systems Manager (Internal Services)",
    "Infrastructure Lead": "Internal Infrastructure Lead",
    "HR Manager": "HR Manager (Personnel Relations)",
    "Payroll Manager": "Payroll & Benefits Manager",
    "Support Supervisor": "Support Supervisor",
    "Support Ops Manager": "Support Operations Manager",
    "Interface Design Manager": "Oracle Interface Design Manager",
    "Platform A Lead": "Role: [PLATFORM_A] Lead",
    "Platform B Lead": "Role: [PLATFORM_B] Lead",
    "PLATFORM_A": "Role: [PLATFORM_A] Lead",
    "PLATFORM_B": "Role: [PLATFORM_B] Lead",
    "CORE_DOMAIN": "[CORE_DOMAIN] Research Director",
    "Product Director": "Firmware Asset Director",
    "Implementation Support Lead": "Implementation Support Lead (Tier 2/3)"
}

def resolve_superior(val: str) -> str:
    # 1. Strip link syntax
    val = re.sub(r"\[(.*?)\].*", r"\1", val).strip()
    # 2. Check Map
    if val in S_MAP: return S_MAP[val]
    # 3. Check for keywords
    if "Sovereign" in val.upper(): return "THE SOVEREIGN"
    if "Board" in val: return "Board of Directors"
    # 4. Fallback to valid titles if partial match
    for t in VALID_TITLES:
        if val in t or t in val: return t
    return val

def fix_all():
    print("NexusOS Lattice Hardening: Closing Circuits...")
    for root, _, files in os.walk(str(ARCHIVE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Update Superior tag
                new_content = re.sub(
                    r"\*\*Superior:\*\* (.*)",
                    lambda m: f"**Superior:** {resolve_superior(m.group(1))}",
                    content
                )

                # Update Navigation footer
                new_content = re.sub(
                    r"\[Superior: (.*?)\]\(.*?\)",
                    lambda m: f"[Superior: {resolve_superior(m.group(1))}](./site_map.md)",
                    new_content
                )

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
    print("Lattice Circuits Hardened.")

if __name__ == "__main__":
    fix_all()
