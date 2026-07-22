"""
NexusAOS - Digestive Engine (Data Metabolism)
Version: 2.0.0
Description: Converts raw external data (stimuli) into Semantic Nutrients (BSF/JSON).
Biological analog: Stomach/Intestines (Breaking down complex matter into absorption-ready units).
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from layers.L11_Data.signal_router import SignalRouter

class DigestiveEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        self.nutrient_path = base_dir / "active_core" / "monitoring_active" / "nutrients.json"
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.nutrient_path.parent.exists():
            self.nutrient_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.nutrient_path.exists():
            self.nutrient_path.write_text(json.dumps({"nutrients": []}), encoding="utf-8")

    def ingest(self, raw_data: str, source: str) -> Dict[str, Any]:
        """Digests raw text into structured 'Nutrients' (Facts/Signals)."""
        print(f"Digestive: Ingesting data from {source}...")
        
        # 1. Mastication (Cleaning/Normalization)
        cleaned = raw_data.strip()
        data_hash = hashlib.sha256(cleaned.encode()).hexdigest()[:12]
        
        # 2. Nutrient Extraction (Heuristic Logic Parsing)
        # In a full 5.0, this would use an SLM to extract BSF-encoded facts.
        nutrient = {
            "id": f"NUT_{data_hash}",
            "source": source,
            "absorption_rate": 0.8,
            "semantic_protein": cleaned[:200], # The 'Meat' of the data
            "timestamp": hashlib.datetime.datetime.now().isoformat() if hasattr(hashlib, "datetime") else ""
        }
        
        # 3. Absorption (Persistence to nutrient buffer)
        self._absorb(nutrient)
        
        # 4. Metabolic Signal
        self.signals.emit_signal(
            "NUTRIENT_ABSORBED", 
            {"id": nutrient["id"], "type": "DATA_PROTEIN"}, 
            evidentiality="~"
        )
        
        return nutrient

    def _absorb(self, nutrient: Dict):
        with open(self.nutrient_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data["nutrients"].append(nutrient)
            if len(data["nutrients"]) > 100:
                data["nutrients"] = data["nutrients"][-100:]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def get_stomach_status(self) -> Dict:
        with open(self.nutrient_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"nutrient_count": len(data["nutrients"]), "fullness_pct": len(data["nutrients"])}

if __name__ == "__main__":

    base = Path(__file__).resolve().parent.parent.parent.parent
    de = DigestiveEngine(base)
    print(de.ingest("RDMA enables zero-copy transfer between agents.", "WebSearch"))
