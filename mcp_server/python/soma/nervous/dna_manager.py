"""
NexusAOS - DNA Manager
Version: 1.0.0
Description: Orchestrates the link between permanent archives (DNA) and active configuration (Genome).
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

class DNAManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.genome_path = base_dir / "active_core" / "monitoring_active" / "evolution" / "biological_genome.json"
        self.dna_archive_path = base_dir / "archives" / "dna_core" / "foundation"
        
    def get_genome(self) -> Dict[str, Any]:
        """Reads the active biological genome."""
        if not self.genome_path.exists():
            self._initialize_default_genome()
        
        try:
            return json.loads(self.genome_path.read_text(encoding="utf-8"))
        except Exception:
            return self._initialize_default_genome()

    def update_genome(self, new_genome: Dict[str, Any]):
        """Updates the active genome and increments the generation."""
        new_genome["last_mutation"] = time.time()
        self.genome_path.parent.mkdir(parents=True, exist_ok=True)
        self.genome_path.write_text(json.dumps(new_genome, indent=4), encoding="utf-8")
        
    def _initialize_default_genome(self) -> Dict[str, Any]:
        default = {
            "reflex_parameters": {
                "nociception_sensitivity": 0.8,
                "hypoxia_threshold": 20.0,
                "ischemia_threshold": 15.0,
                "fever_threshold": 85.0
            },
            "instinct_drives": {
                "curiosity_threshold": 80.0,
                "curiosity_frequency": 3600,
                "consolidation_threshold": 40.0,
                "consolidation_frequency": 7200,
                "evolution_threshold": 90.0
            },
            "metabolic_constants": {
                "basal_metabolic_rate": 0.5,
                "atp_conversion_efficiency": 0.8,
                "heat_per_op": 2.0
            },
            "generation": 1,
            "last_mutation": time.time()
        }
        self.update_genome(default)
        return default

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    dm = DNAManager(base)
    print("Active DNA:", dm.get_genome())
