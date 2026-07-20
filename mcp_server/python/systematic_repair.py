import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os/archives")

# Definitive Map: Filename -> Systematic Title
TITLE_MAP = {
    "cao.md": "Chief Agentic Officer (CAO)",
    "ceo.md": "Chief Executive Officer (CEO)",
    "cfo.md": "Chief Financial Officer (CFO)",
    "cko.md": "Chief Knowledge Officer (CKO)",
    "cso.md": "Chief Systems Officer (CSO)",
    "coo.md": "Chief Operating Officer (COO)",
    "chro.md": "Chief Human Resources Officer (CHRO)",
    "cmo.md": "Chief Marketing Officer (CMO)",
    "cro.md": "Chief Revenue Officer (CRO)",
    "cae.md": "Chief Audit Executive (CAE)",
    "chief_ethics_officer.md": "Chief Ethics & Trust Officer (CETO)",
    "ciso.md": "Chief Information Security Officer (CISO)",
    "nexus_omni_lead.md": "Sovereign Proxy (Nexus Omni-Lead)",
    "nexus_orchestrator_agent.md": "Nexus Orchestrator Agent",
    "agentic_engineer.md": "Agentic Engineer",
    "agentic_knowledge_lead.md": "Agentic Knowledge Lead",
    "agentic_intern.md": "Agentic Intern",
    "vp_agentic_workflows.md": "VP of Agentic Workflows",
    "head_model_governance.md": "Head Model Governance",
    "model_auditor.md": "Model Auditor",
    "corporate_registry_agent.md": "Corporate Registry Agent",
    "global_dependency_agent.md": "Global Dependency Agent",
    "nexus_logic_engine.md": "Nexus Logic Engine",
    "red_team_agent.md": "Red Team Agent",
    "self_repair_agent.md": "Self Repair Agent",
    "specialization_agent.md": "Specialization Agent",
    "structural_efficiency_agent.md": "Structural Efficiency Agent",
    "head_analytics.md": "Head of Analytics (CDO)",
    "vp_data_science.md": "VP of Data Science",
    "bi_manager.md": "Business Intelligence Manager",
    "head_bi.md": "Head of Business Intelligence (BI)",
    "vp_finance.md": "VP of Finance (FP&A)",
    "corporate_controller.md": "Corporate Controller",
    "vp_people_ops.md": "VP of People Operations",
    "vp_legal.md": "VP of Legal (Corporate)",
    "general_counsel.md": "General Counsel (CLO)",
    "head_workplace.md": "Head of Workplace & Facilities",
    "head_research.md": "Head of Research (Chief Scientist)",
    "head_partnerships.md": "Head of Partnerships",
    "head_customer_success.md": "Head of Customer Success",
    "head_support.md": "Head of Customer Support",
    "vp_implementation.md": "VP of Systems Delivery",
    "product_director.md": "Firmware Asset Director",
    "platform_lead_a.md": "Role: [PLATFORM_A] Lead",
    "platform_lead_b.md": "Role: [PLATFORM_B] Lead"
}

# Systematic replacements for any other filename
def generate_systematic_title(filename):
    if filename in TITLE_MAP: return TITLE_MAP[filename]
    name = filename.replace(".md", "").replace("_", " ")
    words = name.split()
    capitalized = []
    for w in words:
        if w.lower() in ["ai", "bi", "qa", "sdr", "sme", "ip", "hq", "ncc", "ceo", "cfo", "cko", "cso", "coo", "chro", "cmo", "cro", "cae", "ceto", "ciso", "cao"]:
            capitalized.append(w.upper())
        elif w.lower() == "fpa":
            capitalized.append("FP&A")
        else:
            capitalized.append(w.capitalize())
    return " ".join(capitalized)

def repair():
    print("NexusOS Systematic Repair: Syncing Titles and Hierarchies...")
    for root, _, files in os.walk(str(BASE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 1. Fix Header
                new_title = generate_systematic_title(file)
                prefix = "Role" if "roles" in str(path) else "Document"
                content = re.sub(r"^# (Role|Document): .*", f"# {prefix}: {new_title}", content, flags=re.MULTILINE)

                # 2. Global Terminology Fix (Double spaces, cleanup)
                content = content.replace("  ", " ").replace("The The Sovereign", "The Sovereign")

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    print("Repair Step 1 Complete: Headers Synced.")

if __name__ == "__main__":
    repair()
