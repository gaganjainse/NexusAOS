"""
SeshaAOS - Lattice Engine
Version: 1.0.0
Description: Manages inter-agent synaptic handoffs and task state tracking.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import sqlite3
import sys
import time
import uuid

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from Agentic_Body.Agentic_Soma.Foundation.dna.sesha_mesh import SeshaMesh
from Agentic_Body.Agentic_Intelligence.memory.state_manager import StateManager

class LatticeEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_mgr = StateManager(base_dir)
        self.mesh = SeshaMesh(base_dir)

    def fire_synapse(self, from_role: str, to_role: str, directive: str, context: Dict | None = None) -> str:
        """Initiates a task handoff from one role to another."""
        task_id = str(uuid.uuid4())[:8]

        # Check for remote role in mesh
        peers = self.mesh.discover_peers()
        target_node = None
        for peer in peers:
            if to_role in peer.get("roles", []):
                target_node = peer["node_id"]
                break

        if target_node:
            # Dispatch to remote node
            synapse_data = {
                "task_id": task_id,
                "from": from_role,
                "to": to_role,
                "directive": directive,
                "context": context or {}
            }
            if self.mesh.send_synapse(target_node, synapse_data):
                return f"Synapse Fired REMOTE [{task_id}] -> Node {target_node} ({to_role})"

        # Fallback to local dispatch via StateManager
        task_data = {
            "task_id": task_id,
            "from": from_role,
            "to": to_role,
            "directive": directive,
            "context": context or {},
            "status": "Firing",
            "started_at": time.time()
        }

        self.state_mgr.create_lattice_task(task_data)
        return f"Synapse Fired LOCAL [{task_id}]: {from_role} -> {to_role}"

    def complete_task(self, task_id: str, result: str):
        """Marks a synaptic task as complete in the DB."""
        conn = self.state_mgr._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE lattice_tasks 
            SET status = 'Resting', completed_at = ?, result = ?
            WHERE task_id = ?
        """, (time.time(), result, task_id))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected > 0:
            return f"Task [{task_id}] consolidated to memory."
        return f"Error: Task [{task_id}] not found in active lattice."

    def get_active_nodes(self) -> list[Dict]:
        """Returns a list of all roles currently 'Firing' from the DB."""
        return self.state_mgr.get_active_tasks()

    def _read_state(self) -> Dict:
        """Compatibility method for OrchestratorEngine."""
        conn = self.state_mgr._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lattice_tasks")
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"history": history}

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    lattice = LatticeEngine(base)
    print(lattice.fire_synapse("Orchestrator", "Research Lead", "Analyze Market Trends"))
    print("Active Nodes:", lattice.get_active_nodes())
