import os
import re
import yaml
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "core/exports/nexus_os.db"
YAML_PATH = BASE_DIR / "core/nlg/nexus_logic.yaml"

def parse_md_file(file_path: Path) -> Dict[str, Any]:
    """Extracts structured logic from a professional-density markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine type
    doc_type = "Role" if "# Role:" in content else "Document"

    # Basic Metadata
    title_match = re.search(r"^# (?:Document|Role): (.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else file_path.stem

    branch_match = re.search(r"\*\*Branch:\*\* (.+)$", content, re.MULTILINE)
    branch = branch_match.group(1).strip() if branch_match else "Core"

    superior_match = re.search(r"\*\*Superior:\*\* (.+)$", content, re.MULTILINE)
    superior = superior_match.group(1).strip() if superior_match else "None"

    purpose_match = re.search(r"## Purpose\n(.*?)\n\n", content, re.DOTALL)
    purpose = purpose_match.group(1).strip() if purpose_match else ""

    # Responsibilities (List)
    resp_match = re.search(r"## Responsibilities\n(.*?)\n\n##", content, re.DOTALL)
    responsibilities = []
    if resp_match:
        responsibilities = [r.strip("- ").strip() for r in resp_match.group(1).strip().split("\n") if r.strip()]

    # Table Parsers (Deliverables and Approval Authority)
    def parse_table(section_name: str) -> List[Dict[str, str]]:
        table_match = re.search(rf"## {section_name}\n\| (?:.+?)\n\| (?:.+?)\n(.*?)\n\n", content, re.DOTALL)
        if not table_match: return []
        rows = []
        for line in table_match.group(1).strip().split("\n"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                rows.append({"key": parts[0], "value": parts[1]})
        return rows

    deliverables = parse_table("Deliverables")
    authority = parse_table("Approval Authority")

    return {
        "type": doc_type,
        "title": title,
        "branch": branch,
        "superior": superior,
        "path": file_path.relative_to(BASE_DIR).as_posix(),
        "purpose": purpose,
        "responsibilities": responsibilities,
        "deliverables": deliverables,
        "approval_authority": authority,
        "version": "1.0",
        "last_compiled": "2026-07-20"
    }

def init_db():
    """Initializes the SQLite database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS artifacts")
    cursor.execute("""
        CREATE TABLE artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            title TEXT,
            branch TEXT,
            superior TEXT,
            path TEXT,
            purpose TEXT,
            responsibilities TEXT,
            deliverables TEXT,
            approval_authority TEXT,
            version TEXT
        )
    """)
    conn.commit()
    return conn

def compile_nlg():
    """Builds the YAML and SQLite Logic Graph."""
    print("Compiling Nexus Logic Graph...")
    all_logic = []

    db_conn = init_db()
    cursor = db_conn.cursor()

    for root, _, files in os.walk(BASE_DIR):
        if "mcp_server" in root or ".git" in root or "nlg" in root:
            continue

        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    logic = parse_md_file(file_path)
                    all_logic.append(logic)

                    # Insert into DB
                    cursor.execute("""
                        INSERT INTO artifacts (type, title, branch, superior, path, purpose, responsibilities, deliverables, approval_authority, version)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        logic["type"], logic["title"], logic["branch"], logic["superior"],
                        logic["path"], logic["purpose"], json.dumps(logic["responsibilities"]),
                        json.dumps(logic["deliverables"]), json.dumps(logic["approval_authority"]),
                        logic["version"]
                    ))
                except Exception as e:
                    print(f"Error compiling {file}: {e}")

    db_conn.commit()
    db_conn.close()

    # Save Master YAML
    with open(YAML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(all_logic, f, sort_keys=False, default_flow_style=False)

    print(f"NLG Compilation Successful: {len(all_logic)} nodes indexed.")
    print(f"Logic Graph: {YAML_PATH}")
    print(f"Database: {DB_PATH}")

if __name__ == "__main__":
    compile_nlg()
