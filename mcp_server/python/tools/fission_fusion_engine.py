"""
AOS Fission & Fusion Engine — split and merge organizational units.
Version: 1.0.0
Description:
  FISSION: Split a branch/plugin/subagent into independent child units (mitosis).
  FUSION: Merge two branches/plugins into a unified unit (hybridization).
"""

import json
import shutil
import sys
import time
import uuid
import zipfile
from pathlib import Path

_tools_parent = Path(__file__).resolve().parent.parent
if str(_tools_parent) not in sys.path:
    sys.path.insert(0, str(_tools_parent))

from typing import Dict, Any, List


class FissionFusionEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.lineage_dir = base_dir / "archives" / "core" / "lineage"
        self.log_path = base_dir / "core" / "monitoring" / "fission_fusion_log.json"
        self._ensure_log()

    def _ensure_log(self):
        self.lineage_dir.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _log(self, event_type: str, details: Dict):
        with open(self.log_path, "r", encoding="utf-8") as f:
            log = json.load(f)
        log.append({"timestamp": time.time(), "type": event_type, **details})
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(log[-100:], f, indent=4)

    def fission(self, source_branch: str, target_name: str) -> str:
        """
        FISSION (Mitosis): Split a branch into an independent child AOS instance.
        Packages branch DNA + pulses into a spore and optionally extracts to target.
        """
        branch_paths = [
            self.base_dir / "archives" / "roles" / source_branch.lower(),
            self.base_dir / f"core/pulses/{source_branch.lower()}.nxp",
        ]

        spore_id = f"fission_{target_name}_{uuid.uuid4().hex[:8]}"
        spore_path = self.lineage_dir / f"{spore_id}.zip"

        found = False
        with zipfile.ZipFile(spore_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for bp in branch_paths:
                if bp.exists():
                    found = True
                    if bp.is_dir():
                        for f in bp.rglob("*"):
                            if f.is_file():
                                zf.write(f, f"branch/{f.relative_to(bp)}")
                    else:
                        zf.write(bp, f"pulse/{bp.name}")

            metadata = {
                "type": "fission",
                "parent": str(self.base_dir),
                "source_branch": source_branch,
                "child_name": target_name,
                "created_at": time.time(),
            }
            zf.writestr("metadata.json", json.dumps(metadata, indent=2))

        if not found:
            spore_path.unlink(missing_ok=True)
            return f"FISSION FAILED: Branch '{source_branch}' not found."

        self._log("fission", {"source": source_branch, "target": target_name, "spore": spore_path.name})
        return f"FISSION OK: Child spore '{spore_path.name}' created from branch '{source_branch}'."

    def fusion(self, branch_a: str, branch_b: str, merged_name: str) -> str:
        """
        FUSION (Hybridization): Merge two branch pulse files into a unified AXP pulse.
        """
        pulse_a = self.base_dir / f"core/pulses/{branch_a.lower()}.nxp"
        pulse_b = self.base_dir / f"core/pulses/{branch_b.lower()}.nxp"

        if not pulse_a.exists() or not pulse_b.exists():
            return f"FUSION FAILED: Missing pulse for {branch_a} and/or {branch_b}."

        content_a = pulse_a.read_text(encoding="utf-8")
        content_b = pulse_b.read_text(encoding="utf-8")

        merged_path = self.base_dir / f"core/pulses/{merged_name.lower()}.nxp"
        merged_content = (
            f"[[ID]] Fused Branch: {merged_name}\n"
            f"::B {merged_name}\n"
            f"::P Fusion of {branch_a} + {branch_b}\n"
            f"::V 1.0\n"
            f"::Z STABLE\n"
            f"::# {uuid.uuid4().hex[:8]}\n\n"
            f"---Pulse-Break---\n\n"
            f"--- FUSION SOURCE: {branch_a} ---\n\n"
            f"{content_a}\n\n"
            f"--- FUSION SOURCE: {branch_b} ---\n\n"
            f"{content_b}\n"
        )
        merged_path.write_text(merged_content, encoding="utf-8")

        self._log("fusion", {"branch_a": branch_a, "branch_b": branch_b, "merged": merged_name})
        return f"FUSION OK: Created '{merged_path.name}' from {branch_a} + {branch_b}."

    def get_lineage_log(self) -> List[Dict]:
        if not self.log_path.exists():
            return []
        with open(self.log_path, "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = FissionFusionEngine(base)
    print(engine.fusion("hq", "core", "hq_core_fused"))
