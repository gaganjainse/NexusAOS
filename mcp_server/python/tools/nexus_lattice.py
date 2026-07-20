"""
Nexus Corporate OS - Lattice Engine
Version: 1.0.0
Description: Manages inter-agent synaptic handoffs and task state tracking.
"""

import json
import uuid
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class LatticeEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "lattice_state.json"
        self._ensure_state_exists()

    def _ensure_state_exists(self):
        if not self.state_path.parent.exists():
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            with open(self.state_path, "w", encoding="utf-8") as f:
                json.dump({"active_tasks": {}, "history": []}, f)

    def fire_synapse(self, from_role: str, to_role: str, directive: str, context: Optional[Dict] = None) -> str:
        """Initiates a task handoff from one role to another."""
        task_id = str(uuid.uuid4())[:8]
        state = self._read_state()

        task_data = {
            "task_id": task_id,
            "from": from_role,
            "to": to_role,
            "directive": directive,
            "context": context or {},
            "status": "Firing",
            "started_at": time.time()
        }

        state["active_tasks"][task_id] = task_data
        self._write_state(state)
        return f"Synapse Fired [{task_id}]: {from_role} -> {to_role}"

    def complete_task(self, task_id: str, result: str):
        """Marks a synaptic task as complete and moves it to history."""
        state = self._read_state()
        if task_id in state["active_tasks"]:
            task = state["active_tasks"].pop(task_id)
            task["status"] = "Resting"
            task["completed_at"] = time.time()
            task["result"] = result
            state["history"].append(task)
            # Keep history manageable
            if len(state["history"]) > 50:
                state["history"].pop(0)
            self._write_state(state)
            return f"Task [{task_id}] consolidated to memory."
        return f"Error: Task [{task_id}] not found in active lattice."

    def get_active_nodes(self) -> List[Dict]:
        """Returns a list of all roles currently 'Firing'."""
        state = self._read_state()
        return list(state["active_tasks"].values())

    def _read_state(self) -> Dict:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"active_tasks": {}, "history": []}

    def _write_state(self, state: Dict):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    lattice = LatticeEngine(base)
    print(lattice.fire_synapse("Orchestrator", "Research Lead", "Analyze Market Trends"))
    print("Active Nodes:", lattice.get_active_nodes())
