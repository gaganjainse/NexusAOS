import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
YAML_PATH = BASE_DIR / "core/nlg/nexus_logic.yaml"

def render_md(logic: Dict[str, Any]) -> str:
    """Renders structured logic back into a professional-density markdown artifact."""
    header_type = logic["type"]
    lines = [
        f"# {header_type}: {logic['title']}",
        "Version 1.0 (Golden Master)",
        "",
        "",
        "## Overview",
        f"**Branch:** {logic['branch']}",
        f"**Level:** {logic.get('level', 'Individual Contributor')}",
        f"**Superior:** {logic['superior']}",
        "",
        "",
        "## Purpose",
        logic["purpose"],
        "",
        "",
        "## Responsibilities"
    ]

    for resp in logic["responsibilities"]:
        lines.append(f"- {resp}")

    lines.append("")
    lines.append("")
    lines.append("## Deliverables")
    if logic["deliverables"]:
        lines.append("| Deliverable | Description |")
        lines.append("| :--- | :--- |")
        for d in logic["deliverables"]:
            lines.append(f"| **{d['key']}** | {d['value']} |")
    else:
        lines.append("None")

    lines.append("")
    lines.append("")
    lines.append("## Reporting & Supervision")
    lines.append(f"- **Reports to:** {logic['superior']}")
    lines.append("- **Supervises:** None") # Default

    lines.append("")
    lines.append("")
    lines.append("## Approval Authority")
    if logic["approval_authority"]:
        lines.append("| Area | Authority |")
        lines.append("| :--- | :--- |")
        for a in logic["approval_authority"]:
            lines.append(f"| **{a['key']}** | {a['value']} |")
    else:
        lines.append("None")

    lines.append("")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("")
    lines.append("**Navigation:** [Global Dashboard](./corporate_os_handbook.md) | [Site Map](./site_map.md)")
    lines.append("")

    return "\n".join(lines)

def render_json(logic: Dict[str, Any]) -> str:
    """Renders structured logic into a JSON format for the web dashboard."""
    return json.dumps(logic, indent=4)

def sync_all_views():
    """Reads the master YAML and re-generates all views (Markdown and JSON)."""
    print("Syncing Logic Graph to Views (MD & JSON)...")

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        all_logic = yaml.safe_load(f)

    # Output paths for dashboard
    json_out_dir = BASE_DIR / "core/ui/nexus_dashboard/src/data/roles"
    json_out_dir.mkdir(parents=True, exist_ok=True)

    for logic in all_logic:
        # Markdown Sync
        md_file_path = BASE_DIR / logic["path"]
        md_file_path.parent.mkdir(parents=True, exist_ok=True)
        md_content = render_md(logic)
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # JSON Sync for Dashboard
        # Sanitize filename: replace spaces with underscores and remove slashes
        role_id = logic["title"].lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        json_file_path = json_out_dir / f"{role_id}.json"
        json_content = render_json(logic)
        with open(json_file_path, "w", encoding="utf-8") as f:
            f.write(json_content)

    # Master index for dashboard
    with open(json_out_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump([l["title"] for l in all_logic], f, indent=4)

    print(f"Sync complete. {len(all_logic)} roles updated in MD and JSON.")

if __name__ == "__main__":
    sync_all_views()
