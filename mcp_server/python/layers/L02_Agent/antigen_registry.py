"""
SeshaAOS - Antigen Registry (Immune Memory)
Version: 1.0.0
Description: Stores patterns of past errors and logic failures to prevent re-infection.
Biological analog: Memory T-cells and B-cells.
"""

import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

class AntigenRegistry:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.registry_path = base_dir / "active_core" / "monitoring_active" / "immune_memory.json"
        self._ensure_registry()

    def _ensure_registry(self):
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            self.registry_path.write_text(json.dumps({"antigens": []}), encoding="utf-8")

    def register_antigen(self, error_type: str, context: str, solution: str):
        """Registers a new 'Antigen' (Bug Pattern) into immune memory."""
        antigen_hash = hashlib.sha256(context.encode()).hexdigest()[:12]
        
        with open(self.registry_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            # Prevent duplicates
            if any(a["hash"] == antigen_hash for a in data["antigens"]):
                return
                
            data["antigens"].append({
                "hash": antigen_hash,
                "type": error_type,
                "context": context,
                "solution": solution,
                "detected_count": 1
            })
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def check_infection(self, context: str) -> Dict[str, Any]:
        """Scans context for known pathogens (Past Bugs) and persists detection count."""
        with open(self.registry_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            found = False
            result = {"infected": False}
            
            for antigen in data["antigens"]:
                if antigen["context"] in context:
                    antigen["detected_count"] += 1
                    result = {"infected": True, "antigen": antigen}
                    found = True
                    break
            
            if found:
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            
            return result

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    ar = AntigenRegistry(base)
    ar.register_antigen("SyntaxError", "missing closing bracket in loop", "Add '}' at line 45")
    print(ar.check_infection("Error: missing closing bracket in loop detected."))

