"""
SeshaAOS - Mutation Engine
Version: 1.0.0
Description: Enables autonomous rewriting of the OS DNA (Markdown artifacts).
"""

from datetime import datetime
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class MutationEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.archive_dir = base_dir / "archives"
        self.mutation_log_path = base_dir / "core" / "monitoring" / "mutation_history.json"
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.mutation_log_path.parent.exists():
            self.mutation_log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.mutation_log_path.exists():
            with open(self.mutation_log_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def apply_mutation(self, file_rel_path: str, old_text: str, new_text: str, reason: str) -> str:
        """Surgically replaces text in a DNA artifact and triggers re-forging."""
        file_path = self.base_dir / file_rel_path
        if not file_path.exists():
            return f"Error: File {file_rel_path} not found in DNA."

        # Safety Check: Protected Files
        if "Sesha_constitution.md" in file_rel_path.lower():
            if "LAW I" in old_text or "LAW I" in new_text:
                return "CRITICAL ERROR: LAW I (Sovereign Supremacy) is immutable. Mutation aborted."

        try:
            # 1. Backup
            backup_path = file_path.with_suffix(".md.bak")
            shutil.copy2(file_path, backup_path)

            # 2. Read and Replace
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if old_text not in content:
                return "Error: Target DNA snippet not found in artifact."

            new_content = content.replace(old_text, new_text)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            # 3. Log Mutation
            self._log_mutation(file_rel_path, reason)

            # 4. Trigger Re-forge
            self._reforge()

            return f"Mutation successful in {file_rel_path}. Logic circuits updated."

        except Exception as e:
            return f"Mutation failed: {str(e)}"

    def _log_mutation(self, file_path: str, reason: str):
        with open(self.mutation_log_path, "r", encoding="utf-8") as f:
            history = json.load(f)

        history.append({
            "timestamp": datetime.now().isoformat(),
            "artifact": file_path,
            "reason": reason
        })

        with open(self.mutation_log_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def _reforge(self):
        """Runs the compiler and forge to apply changes to the pulses."""
        compiler = self.base_dir / "mcp_server" / "python" / "compiler" / "nlg_compiler.py"
        forge = self.base_dir / "mcp_server" / "python" / "compiler" / "nxp_forge.py"

        subprocess.run([sys.executable, str(compiler)], capture_output=True)
        subprocess.run([sys.executable, str(forge)], capture_output=True)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = MutationEngine(base)
    # Test: Add a line to Site Map
    print(engine.apply_mutation(
        "archives/dna_core/foundation/site_map.md",
        "**Navigation:**",
        "**Evolutionary Note:** Tested Mutation.\n\n**Navigation:**",
        "Verifying Phase 8 Mutation Engine."
    ))
