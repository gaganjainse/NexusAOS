"""
SeshaAOS - Reproduction Engine
Version: 2.0.0
Description: Handles the serialization (Spore creation) and instantiation (Birth)
of OS instances with oxidation-aware lineage tracking.
"""

from __future__ import annotations

import json
import os
import sys
import zipfile
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from datetime import datetime
from typing import Optional, Dict

from layers.L02_Agent.oxidation_model import OxidationModel


class ReproductionEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.spore_dir = base_dir / "archives" / "core" / "lineage" / "spores"
        self.lineage_dir = base_dir / "archives" / "core" / "lineage"
        self.oxidation = OxidationModel(base_dir=base_dir)
        self._ensure_paths()

    def _ensure_paths(self):
        self.spore_dir.mkdir(parents=True, exist_ok=True)
        self.lineage_dir.mkdir(parents=True, exist_ok=True)

    def create_spore(self, parent_instance_id: Optional[str] = None) -> Dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        spore_name = f"Sesha_spore_{timestamp}.zip"
        spore_path = self.spore_dir / spore_name

        targets = [
            ("archives/core/foundation", "dna/foundation"),
            ("archives/core/rules", "dna/rules"),
            ("archives/core/learning", "wisdom"),
            ("core/pulses", "logic"),
            ("archives/core/protocols", "dna/protocols"),
        ]

        try:
            with zipfile.ZipFile(spore_path, "w", zipfile.ZIP_DEFLATED) as spore:
                for src_rel, arc_root in targets:
                    src_path = self.base_dir / src_rel
                    if not src_path.exists():
                        continue
                    for file in src_path.rglob("*"):
                        if file.is_file():
                            arc_name = os.path.join(arc_root, file.relative_to(src_path))
                            spore.write(file, arc_name)

                parent_id = parent_instance_id
                if parent_id is None:
                    parent = self.oxidation.create_instance()
                    parent_id = parent.instance_id
                else:
                    fission_result = self.oxidation.fission(parent_id)
                    if not fission_result.get("allowed"):
                        return {"created": False, "reason": fission_result}

                metadata = {
                    "birth_date": timestamp,
                    "parent_base": str(self.base_dir),
                    "generation": self._get_current_generation() + 1,
                    "parent_instance_id": parent_id,
                    "oxidative_load": self.oxidation.get_instance_status(parent_id).get(
                        "oxidative_load", 0.0
                    ),
                }
                spore.writestr("metadata.json", json.dumps(metadata, indent=4))
                return {"created": True, "spore": spore_name, "metadata": metadata}
        except Exception as e:
            return {"created": False, "error": str(e)}

    def _get_current_generation(self) -> int:
        return 1

    def instantiate_spore(self, spore_name: str, target_dir: Path) -> str:
        spore_path = self.spore_dir / spore_name
        if not spore_path.exists():
            return "Error: Spore not found."

        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(spore_path, "r") as spore:
                spore.extractall(target_dir)
            return f"Child OS instantiated at {target_dir}. Ready for boot-up."
        except Exception as e:
            return f"Instantiation Error: {str(e)}"


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = ReproductionEngine(base)
    print(engine.create_spore())

