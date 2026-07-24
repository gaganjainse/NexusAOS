import hashlib
import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/Sesha_corporate_os")
ARCHIVE_DIR = BASE_DIR / "archives"

# The Definitive Map of File -> Systematic Title
SYSTEM_MAP = {
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
    "Sesha_omni_lead.md": "Sovereign Proxy (Sesha Omni-Lead)",
    "Sesha_orchestrator_agent.md": "Sesha Orchestrator Agent",
    "Sesha_input_parser_agent.md": "Sesha Input Parser Agent",
    "oracle_interface_agent.md": "Oracle Interface Agent (OIA)",
    "learning_synthesis_agent.md": "Learning Synthesis Agent",
    "system_health_supervisor.md": "System Health Supervisor",
    "board_of_directors.md": "Board of Directors",
    "chief_of_staff.md": "Chief of Staff",
    "internal_comms_lead.md": "Internal Communications Lead",
    "audit_director.md": "Audit Director",
    "head_analytics.md": "Head of Analytics (CDO)",
    "head_bi.md": "Head of Business Intelligence (BI)",
    "vp_data_science.md": "VP of Data Science",
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
    "agentic_engineer.md": "Agentic Engineer",
    "agentic_knowledge_lead.md": "Agentic Knowledge Lead",
    "agentic_intern.md": "Agentic Intern",
    "vp_agentic_workflows.md": "VP of Agentic Workflows",
    "head_model_governance.md": "Head Model Governance",
    "model_auditor.md": "Model Auditor",
    "corporate_registry_agent.md": "Corporate Registry Agent",
    "global_dependency_agent.md": "Global Dependency Agent",
    "Sesha_logic_engine.md": "Sesha Logic Engine",
    "red_team_agent.md": "Red Team Agent",
    "self_repair_agent.md": "Self Repair Agent",
    "specialization_agent.md": "Specialization Agent",
    "structural_efficiency_agent.md": "Structural Efficiency Agent",
    "platform_lead_a.md": "Role: [PLATFORM_A] Lead",
    "platform_lead_b.md": "Role: [PLATFORM_B] Lead"
}

# Systematic Hierarchy (Role ID -> Superior ID)
SUPERIORS = {
    "Chief Agentic Officer (CAO)": "Chief Executive Officer (CEO)",
    "Chief Knowledge Officer (CKO)": "Chief Executive Officer (CEO)",
    "Chief Systems Officer (CSO)": "Chief Executive Officer (CEO)",
    "Chief Financial Officer (CFO)": "Chief Executive Officer (CEO)",
    "Chief Human Resources Officer (CHRO)": "Chief Executive Officer (CEO)",
    "Chief Marketing Officer (CMO)": "Chief Executive Officer (CEO)",
    "Chief Revenue Officer (CRO)": "Chief Executive Officer (CEO)",
    "Chief Operating Officer (COO)": "Chief Executive Officer (CEO)",
    "Chief Audit Executive (CAE)": "Chief Executive Officer (CEO)",
    "General Counsel (CLO)": "Chief Executive Officer (CEO)",
    "Head of Research (Chief Scientist)": "Chief Executive Officer (CEO)",
    "Head of Business Development": "Chief Executive Officer (CEO)",
    "Head of Customer Support": "Chief Executive Officer (CEO)",
    "Head of Analytics (CDO)": "Chief Executive Officer (CEO)",
    "Chief Executive Officer (CEO)": "Board of Directors",
    "Board of Directors": "THE SOVEREIGN",
    "Sovereign Proxy (Sesha Omni-Lead)": "THE SOVEREIGN",
    "Sesha Orchestrator Agent": "Sovereign Proxy (Sesha Omni-Lead)",
    "Sesha Input Parser Agent": "Sesha Orchestrator Agent",
    "Oracle Interface Agent (OIA)": "Sesha Orchestrator Agent",
    "Learning Synthesis Agent": "Sovereign Proxy (Sesha Omni-Lead)",
    "System Health Supervisor": "Sovereign Proxy (Sesha Omni-Lead)",
    "Chief of Staff": "Chief Executive Officer (CEO)",
    "Internal Communications Lead": "Chief of Staff",
    "Agentic Engineer": "VP of Agentic Workflows",
    "VP of Agentic Workflows": "Chief Agentic Officer (CAO)",
    "Agentic Knowledge Lead": "Chief Agentic Officer (CAO)",
    "Head Model Governance": "Chief Agentic Officer (CAO)",
    "Sesha Logic Engine": "Chief Agentic Officer (CAO)",
    "Specialization Agent": "Chief Agentic Officer (CAO)",
    "Corporate Registry Agent": "Chief Knowledge Officer (CKO)",
    "Global Dependency Agent": "Chief Knowledge Officer (CKO)",
    "Self Repair Agent": "Chief Knowledge Officer (CKO)",
    "Structural Efficiency Agent": "Chief Knowledge Officer (CKO)",
    "Red Team Agent": "Chief Ethics & Trust Officer (CETO)",
    "Chief Ethics & Trust Officer (CETO)": "Chief Executive Officer (CEO)",
    "Agentic Department Firmware": "Chief Agentic Officer (CAO)",
    "Analytics Department Firmware": "Head of Analytics (CDO)",
    "Audit Department Firmware": "Audit Director",
    "Bizdev Department Firmware": "Head of Business Development",
    "Finance Department Firmware": "Chief Financial Officer (CFO)",
    "Hr Department Firmware": "Chief Human Resources Officer (CHRO)",
    "Legal Department Firmware": "General Counsel (CLO)",
    "Marketing Department Firmware": "Chief Marketing Officer (CMO)",
    "Ops Department Firmware": "Chief Operating Officer (COO)",
    "Research Department Firmware": "Head of Research (Chief Scientist)",
    "Sales Department Firmware": "Chief Revenue Officer (CRO)",
    "Support Department Firmware": "Head of Customer Support",
    "Executive Assistant CEO": "Chief Executive Officer (CEO)"
}

def clean_title(filename):
    if filename in SYSTEM_MAP: return SYSTEM_MAP[filename]
    name = filename.replace(".md", "").replace("_", " ")
    return " ".join([w.capitalize() for w in name.split()])

def repair():
    print("SeshaAOS Final Systematic Polish: Securing Entire Vault...")
    for root, _, files in os.walk(str(ARCHIVE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 1. Force Systematic Header
                title = clean_title(file)
                prefix = "Role" if "roles" in str(path) else "Document"
                content = re.sub(r"^# (?:Role|Document): .*", f"# {prefix}: {title}", content, flags=re.MULTILINE)

                # 2. Hard-Code Superior
                superior = SUPERIORS.get(title, "Chief Executive Officer (CEO)")
                if title == "Sovereign Proxy (Sesha Omni-Lead)" or title == "Board of Directors":
                    superior = "THE SOVEREIGN"
                if title == "THE SOVEREIGN": superior = "None"

                content = re.sub(r"\*\*Superior:\*\* .*", f"**Superior:** {superior}", content)

                # 3. Clean Terminology
                content = content.replace("Department Assistant", "Department Firmware")
                content = content.replace("Assistant", "Firmware")
                content = content.replace("AI", "Agentic")
                content = content.replace("User", "Sovereign")

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    print("Systematic Polish Complete.")

if __name__ == "__main__":
    repair()

