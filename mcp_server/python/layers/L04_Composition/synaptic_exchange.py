"""
NexusAOS - Synaptic Exchange (Marketplace)
Version: 1.0.0
Description: Handles the discovery, metabolic validation, and immune-safe installation of new Organs (Plugins).
"""

import json
import time
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L02_Agent.auto_repair import AutoRepairEngine
from layers.L02_Agent.metabolism_engine import MetabolismEngine

class SynapticExchange:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.exchange_dir = base_dir / "core" / "monitoring" / "mesh" / "exchange"
        self.exchange_dir.mkdir(parents=True, exist_ok=True)
        self.plugins_dir = base_dir / "plugins"
        self.repair_engine = AutoRepairEngine(base_dir)
        self.metabolism = MetabolismEngine(base_dir)

    def search_exchange(self, query: str) -> List[Dict]:
        """Simulates searching a remote registry for available organs."""
        # Simulated registry
        registry = [
            {"id": "crypto_organ", "name": "Cryptographic Cortex", "cost": 50, "description": "Adds advanced encryption receptors."},
            {"id": "social_organ", "name": "Social Synapse", "cost": 30, "description": "Integrates with Slack and Discord swarms."},
            {"id": "logic_wisdom", "name": "Logic Wisdom artifact", "type": "wisdom", "description": "Consolidated logic from high-performant swarms."}
        ]
        return [item for item in registry if query.lower() in item["name"].lower() or query.lower() in item["description"].lower()]

    def install_organ(self, organ_id: str) -> Dict:
        """Downloads, validates, and installs a new biological organ."""
        # 1. Metabolic Check
        state = self.metabolism._report()
        if state["atp"] < 20:
            return {"success": False, "error": "Insufficient ATP for transplantation (need > 20)."}

        # 2. Simulated Download (Creating a dummy file)
        organ_path = self.exchange_dir / f"{organ_id}.py"
        organ_path.write_text(f'# {organ_id} installed via Synaptic Exchange\ndef status(): return "Operational"', encoding="utf-8")

        # 3. Immune/Sanctity Check
        # Using ARE to scan the file (simulated)
        # In a real system, ARE would check for syntax errors and malicious patterns
        immune_check = self.repair_engine.scan_and_fix()
        if "Critical" in immune_check:
            organ_path.unlink()
            return {"success": False, "error": f"Organ rejected by Immune System: {immune_check}"}

        # 4. Metabolic Consumption
        self.metabolism.consume_energy(10)

        # 5. Transplant (Move to plugins dir)
        target_path = self.plugins_dir / f"{organ_id}.py"
        shutil.move(str(organ_path), str(target_path))

        return {
            "success": True, 
            "organ_id": organ_id, 
            "message": "Transplantation successful. Organ is now part of the Soma.",
            "metabolic_cost": 10
        }

    def package_wisdom_spore(self, artifact_name: str) -> Dict:
        """Packages a local learning artifact as a wisdom spore for the exchange."""
        learning_dir = self.base_dir / "archives" / "core" / "learning"
        source_file = learning_dir / artifact_name
        
        if not source_file.exists():
            return {"success": False, "error": "Artifact not found."}
            
        spore_id = f"spore_{int(time.time())}_{artifact_name}"
        target_path = self.exchange_dir / spore_id
        shutil.copy2(source_file, target_path)
        
        return {"success": True, "spore_id": spore_id, "path": str(target_path)}

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    exchange = SynapticExchange(base)
    print(exchange.search_exchange("Synapse"))
