import os
import json
import re
from typing import List, Dict, Any

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_FILE = os.path.join(BASE_DIR, "core", "exports", "nexus_file_index.json")

def parse_md_file(file_path: str) -> Dict[str, Any]:
    """Parses a markdown file to extract metadata and structural info."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Title/Role Name
    title_match = re.search(r"^# (?:Document|Role): (.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(file_path)

    # Extract Branch (for roles)
    branch_match = re.search(r"\*\*Branch:\*\* (.+)$", content, re.MULTILINE)
    branch = branch_match.group(1).strip() if branch_match else "Core"

    # Extract Purpose/Summary
    purpose_match = re.search(r"## Purpose\n(.+?)\n\n", content, re.DOTALL)
    purpose = purpose_match.group(1).strip() if purpose_match else ""

    # Extract Sections
    sections = re.findall(r"^## (.+)$", content, re.MULTILINE)

    return {
        "title": title,
        "branch": branch,
        "path": os.path.relpath(file_path, BASE_DIR).replace("\\", "/"),
        "purpose": purpose,
        "sections": sections,
        "keywords": list(set(re.findall(r"\w{4,}", content.lower())))[:50] # Basic keyword extraction
    }

def build_index():
    """Recursively scans the nexus_corporate_os directory and builds a JSON index."""
    index = []
    print(f"Indexing NexusAOS at: {BASE_DIR}...")

    for root, _, files in os.walk(BASE_DIR):
        # Skip mcp_server and hidden folders
        if "mcp_server" in root or ".git" in root:
            continue

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    metadata = parse_md_file(file_path)
                    index.append(metadata)
                except Exception as e:
                    print(f"Error indexing {file}: {e}")

    # Write the index
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    print(f"Indexing complete. {len(index)} files processed. Saved to {INDEX_FILE}")

if __name__ == "__main__":
    build_index()
