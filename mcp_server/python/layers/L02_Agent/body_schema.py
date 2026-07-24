"""
SeshaAOS - Body Schema (Proprioception)
Version: 1.0.0
Description: Real-time component health, capabilities, and system structure.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any, List

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root


class BodySchema:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.schema_file = base_dir / "core" / "monitoring" / "body_schema.json"
        self._init_schema()

    def _init_schema(self):
        if not self.schema_file.exists():
            self.schema_file.parent.mkdir(exist_ok=True, parents=True)
            schema = {
                "anatomy_version": "3.0-GM",
                "organs": {
                    "Nervous": {"path": "soma/nervous", "status": "active", "functions": ["state", "signals", "gating"]},
                    "Metabolic": {"path": "soma/metabolic", "status": "active", "functions": ["energy", "atp", "thermal"]},
                    "Immune": {"path": "soma/immune", "status": "active", "functions": ["antibody", "rbac", "repair"]},
                    "Integumentary": {"path": "soma/integumentary", "status": "active", "functions": ["senses", "skin"]},
                    "Excretory": {"path": "soma/excretory", "status": "active", "functions": ["filtration", "toxins"]},
                    "Mind": {"path": "mind", "status": "active", "functions": ["cognition", "evolution", "instinct"]}
                },
                "synaptic_pressure": 1.0,  # Speed of internal communication
                "sensory_map": {
                    "mcp_server/python/index.py": 10.0, # High sensitivity
                    "archives/dna_core": 8.0,
                    "active_core/monitoring_active": 5.0
                }
            }
            with open(self.schema_file, "w") as f:
                json.dump(schema, f, indent=4)

    def get_body_schema(self) -> Dict[str, Any]:
        try:
            with open(self.schema_file, "r") as f:
                return json.load(f)
        except Exception:
            return {"error": "Failed to load body schema"}

    def can_execute(self, capability: str) -> bool:
        schema = self.get_body_schema()
        for comp in schema.get("components", {}).values():
            if capability in comp.get("capabilities", []) and comp.get("status") == "healthy":
                return True
        return False

