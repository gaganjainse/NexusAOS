"""
Nexus Corporate OS - Reproduction Engine
Version: 1.0.0
Description: Handles the serialization (Spore creation) and instantiation (Birth) of OS instances.
"""

import os
import json
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

class ReproductionEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.spore_dir = base_dir / "archives" / "core" / "lineage" / "spores"
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.spore_dir.exists():
            self.spore_dir.mkdir(parents=True, exist_ok=True)

    def create_spore(self) -> str:
        """Packages DNA, Wisdom, and Logic into a .nexus_spore file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        spore_name = f"nexus_spore_{timestamp}.zip"
        spore_path = self.spore_dir / spore_name

        # Define what to include in the "Spore"
        targets = [
            ("archives/core/foundation", "dna/foundation"),
            ("archives/core/rules", "dna/rules"),
            ("archives/core/learning", "wisdom"),
            ("core/pulses", "logic"),
            ("archives/core/protocols", "dna/protocols")
        ]

        try:
            with zipfile.ZipFile(spore_path, 'w', zipfile.ZIP_DEFLATED) as spore:
                for src_rel, arc_root in targets:
                    src_path = self.base_dir / src_rel
                    if src_path.exists():
                        for file in src_path.rglob("*"):
                            if file.is_file():
                                arc_name = os.path.join(arc_root, file.relative_to(src_path))
                                spore.write(file, arc_name)

                # Metadata
                metadata = {
                    "birth_date": timestamp,
                    "parent_base": str(self.base_dir),
                    "generation": self._get_current_generation() + 1
                }
                spore.writestr("metadata.json", json.dumps(metadata, indent=4))

            return f"Spore created successfully: {spore_name}"
        except Exception as e:
            return f"Reproduction Error: {str(e)}"

    def _get_current_generation(self) -> int:
        # Simplified: Check for existing lineage files or default to 1
        return 1

    def instantiate_spore(self, spore_name: str, target_dir: Path) -> str:
        """Unpacks a spore into a new OS directory structure."""
        spore_path = self.spore_dir / spore_name
        if not spore_path.exists():
            return "Error: Spore not found."

        try:
            if not target_dir.exists():
                target_dir.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(spore_path, 'r') as spore:
                spore.extractall(target_dir)

            return f"Child OS instantiated at {target_dir}. Ready for boot-up."
        except Exception as e:
            return f"Instantiation Error: {str(e)}"

if __name__ == "__main__":
    # Self-test
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = ReproductionEngine(base)
    print(engine.create_spore())
