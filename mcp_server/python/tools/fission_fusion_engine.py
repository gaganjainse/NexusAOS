"""
AOS Fission & Fusion Engine — split and merge organizational units.
Version: 2.0.0
Description:
 FISSION: Split a branch/plugin/subagent into independent child units (mitosis).
 FUSION: Merge two branches/plugins into a unified unit (hybridization).
"""

import json
from pathlib import Path
from typing import Dict, List

from tools.oxidation_model import OxidationModel


class FissionFusionEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.lineage_dir = base_dir / "archives" / "core" / "lineage"
        self.oxidation = OxidationModel(base_dir=base_dir)
        self.log_path = base_dir / "core" / "monitoring" / "fission_fusion_log.json"
        self._ensure_log()

    def _ensure_log(self):
        self.lineage_dir.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.write_text("[]", encoding="utf-8")

    def _log(self, event_type: str, details: Dict):
        import time
        log = json.loads(self.log_path.read_text(encoding="utf-8"))
        log.append({"timestamp": time.time(), "type": event_type, **details})
        self.log_path.write_text(json.dumps(log[-100:], indent=4), encoding="utf-8")

    def fission(self, parent_instance_id: str, child_name: Optional[str] = None) -> Dict:
        result = self.oxidation.fission(parent_instance_id=parent_instance_id)
        if not result.get("allowed"):
            return result
        self._log("fission", result)
        return result

    def fusion(self, instance_a: str, instance_b: str, merged_name: Optional[str] = None) -> Dict:
        result = self.oxidation.fuse(instance_a=instance_a, instance_b=instance_b)
        if not result.get("allowed"):
            return result
        self._log("fusion", result)
        return result

    def antioxidant_repair(self, instance_id: str) -> Dict:
        result = self.oxidation.antioxidant_repair(instance_id=instance_id)
        if result.get("repaired"):
            self._log("antioxidant_repair", result)
        return result

    def get_lineage_log(self) -> List[Dict]:
        if not self.log_path.exists():
            return []
        return json.loads(self.log_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = FissionFusionEngine(base)

