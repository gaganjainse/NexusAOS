# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - Collective Memory Engine (Swarm Hippocampus)
Version: 1.0.0
Description: Syncs entities across the Synaptic Mesh using LWW conflict resolution.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L05_Memory.memory_receptor import MemoryReceptor
from layers.L12_Infrastructure.Sesha_mesh import SeshaMesh

class CollectiveMemory:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.receptor = MemoryReceptor(base_dir)
        self.mesh = SeshaMesh(base_dir)
        self.sync_dir = base_dir / "core" / "monitoring" / "mesh" / "memory_sync"
        self.sync_dir.mkdir(parents=True, exist_ok=True)

    def store_and_broadcast(self, entity_id: str, properties: Dict) -> Dict:
        """Stores locally and broadcasts to the mesh."""
        # Add timestamp for LWW
        properties["_timestamp"] = time.time()
        res = self.receptor.store_entity(entity_id, properties)

        # Broadcast sync signal
        sync_file = self.sync_dir / f"sync_{self.mesh.node_id}_{entity_id}.json"
        sync_file.write_text(json.dumps({
            "entity_id": entity_id,
            "properties": properties,
            "node_id": self.mesh.node_id
        }, indent=4), encoding="utf-8")

        return res

    def sync_mesh_knowledge(self) -> int:
        """Pulls sync signals from peers and merges knowledge."""
        synced_count = 0
        local_entities = self.receptor._load_entities()

        for sync_file in self.sync_dir.glob("sync_*.json"):
            # Don't sync own signals
            if self.mesh.node_id in sync_file.name:
                continue

            try:
                data = json.loads(sync_file.read_text(encoding="utf-8"))
                eid = data["entity_id"]
                remote_props = data["properties"]

                # LWW Resolution
                if eid not in local_entities or remote_props.get("_timestamp", 0) > local_entities[eid].get("_timestamp", 0):
                    local_entities[eid] = remote_props
                    synced_count += 1
            except Exception:
                continue

        if synced_count > 0:
            self.receptor._save_entities(local_entities)

        return synced_count

    def recall_collective(self, entity_id: str) -> Dict:
        """Recalls from the collective knowledge base."""
        # Try local first
        res = self.receptor.recall_entity(entity_id)
        if res["success"]:
            return res

        # In a real system, we might query peers here.
        # For simulation, we assume sync_mesh_knowledge has already populated local store.
        return res

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    col_mem = CollectiveMemory(base)
    print(col_mem.store_and_broadcast("PROJECT_ALPHA", {"status": "Active", "lead": "Sesha"}))
    print(f"Synced {col_mem.sync_mesh_knowledge()} entities from mesh.")

