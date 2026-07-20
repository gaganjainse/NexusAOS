import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os/archives")

# Definite Branch Head Mapping
BRANCH_HEADS = {
    "agentic": "Chief Agentic Officer (CAO)",
    "analytics": "Head of Analytics (CDO)",
    "audit": "Chief Audit Executive (CAE)",
    "bizdev": "Head of Business Development",
    "finance": "Chief Financial Officer (CFO)",
    "hq": "Chief Executive Officer (CEO)",
    "hr": "Chief Human Resources Officer (CHRO)",
    "legal": "General Counsel (CLO)",
    "marketing": "Chief Marketing Officer (CMO)",
    "operations": "Chief Operating Officer (COO)",
    "research": "Head of Research (Chief Scientist)",
    "sales": "Chief Revenue Officer (CRO)",
    "support": "Head of Customer Support",
    "systems": "Chief Systems Officer (CSO)"
}

# Dept Head Mapping (Folder -> Superior Role Filename)
DEPT_MAP = {
    "bi": "head_bi.md",
    "datascience": "vp_data_science.md",
    "engineering": "data_engineering_manager.md",
    "execution": "audit_director.md",
    "planning": "audit_director.md",
    "reporting": "findings_reporting_lead.md",
    "sector_compliance": "audit_knowledge_lead.md",
    "corpdev": "head_corpdev.md",
    "strategy": "vp_strategy.md",
    "accounting": "accounting_manager.md",
    "fpa": "fpa_manager.md",
    "tax": "corporate_controller.md",
    "treasury": "vp_finance.md",
    "recruiting": "head_talent_acquisition.md",
    "contracts": "vp_legal.md",
    "ip": "head_ip.md",
    "content": "vp_marketing.md",
    "creative": "creative_director.md",
    "performance": "performance_marketing_manager.md",
    "facilities": "head_workplace.md",
    "internal_systems": "vp_internal_systems.md",
    "domain": "domain_research_director.md",
    "lab": "systems_innovation_lead.md",
    "enterprise": "enterprise_sales_manager.md",
    "sdr": "sdr_manager.md",
    "sme": "sme_sales_manager.md",
    "success": "customer_success_manager.md",
    "tier1": "support_manager.md",
    "tier2": "implementation_support_lead.md",
    "core_system": "core_system_lead.md",
    "design": "ui_ux_design_manager.md",
    "infrastructure": "devops_manager.md",
    "platform_a": "platform_lead_a.md",
    "platform_b": "platform_lead_b.md",
    "quality": "qa_manager.md",
    "security": "security_manager.md"
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
    return " ".join(capitalized)

def get_superior(file_path):
    rel = file_path.relative_to(BASE_DIR)
    parts = rel.parts
    filename = file_path.name

    # 1. Level 1: Command Center
    if filename == "nexus_omni_lead.md": return "THE SOVEREIGN"
    if "ncc" in parts:
        if filename == "nexus_orchestrator_agent.md": return "Sovereign Proxy (Nexus Omni-Lead)"
        return "Nexus Orchestrator Agent"

    # 2. Level 2: CEO
    if filename == "ceo.md": return "Board of Directors"
    if filename in ["cao.md", "cso.md", "cfo.md", "cko.md", "chro.md", "cmo.md", "cro.md", "coo.md", "cae.md", "head_research.md", "head_bizdev.md", "head_support.md", "head_analytics.md"]:
        return "Chief Executive Officer (CEO)"

    # 3. Department Level
    if len(parts) >= 3 and parts[0] == "roles":
        dept = parts[2]
        branch = parts[1]

        # Is it the department lead itself?
        if filename in DEPT_MAP.values():
            return BRANCH_HEADS.get(branch, "Chief Executive Officer (CEO)")

        # Does the folder have a mapped superior?
        if dept in DEPT_MAP:
            sup_file = DEPT_MAP[dept]
            return clean_title(sup_file)

    # Fallback to Branch Head
    if len(parts) > 1 and parts[1] in BRANCH_HEADS:
        return BRANCH_HEADS[parts[1]]

    return "None"

def process():
    print("NexusOS Master Hardening Initiated...")
    for root, _, files in os.walk(str(BASE_DIR)):
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                title = clean_title(file)
                superior = get_superior(path)

                # Force update Header and Superior
                content = re.sub(r"^# (Role|Document): .*", f"# {'Role' if 'roles' in str(path) else 'Document'}: {title}", content, flags=re.MULTILINE)
                content = re.sub(r"\*\*Superior:\*\* .*", f"**Superior:** {superior}", content, flags=re.MULTILINE)

                # Cleanup Navigation footer
                content = re.sub(r"\[Superior: .*?\]\(.*?\)", f"[Superior: {superior}](./site_map.md)", content)

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    print("Master Hardening Complete.")

if __name__ == "__main__":
    process()
