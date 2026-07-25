"""
SeshaAOS - Logic Git
Version: 1.0.0
Description: Fractal decomposition and versioning of sub-atomic reasoning nodes.
"""

from pathlib import Path
from typing import Any, List, Optional
import hashlib
import json
import sys
import time

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

class LogicGit:
    """Git for Logic - maintains versioned state for sub-atomic task DAGs."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.logic_dir = base_dir / "core" / "monitoring" / "logic_history"
        self.logic_dir.mkdir(parents=True, exist_ok=True)

    def commit_node(self, task_id: str, atom_text: str, result: str) -> str:
        """Commits a sub-atomic logic node to the history."""
        node_hash = hashlib.sha256(f"{task_id}:{atom_text}".encode()).hexdigest()[:12]
        entry = {
            "task_id": task_id,
            "atom": atom_text,
            "result": result,
            "timestamp": time.time(),
            "status": "Committed"
        }
        
        path = self.logic_dir / f"{node_hash}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=4)
            
        return node_hash

    def get_node(self, node_hash: str) -> dict[str, Any]:
        path = self.logic_dir / f"{node_hash}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2]
    lg = LogicGit(base)
    h = lg.commit_node("test_task", "Sub-atomic logic unit", "SUCCESS")
    print(f"Logic Committed: {h}")
