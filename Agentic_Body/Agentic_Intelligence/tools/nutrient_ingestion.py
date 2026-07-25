# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
# TRANSPARENCY: simulated/file-based — Specialization framework referenced (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA.
"""
SeshaAOS - Nutrient Ingestion Pipeline
Version: 1.0.0
Description: Automates the transition from research discovery to DNA integration.
"""

import json
import sys
import time
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L06_Tool.deep_research_tool import DeepResearchTool
from layers.L11_Data.signal_router import SignalRouter

class NutrientIngestion:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.research = DeepResearchTool(base_dir)
        self.signals = SignalRouter(base_dir)
        self.dna_dir = base_dir / "archives" / "dna_core" / "learning_dna"
        self.dna_dir.mkdir(parents=True, exist_ok=True)

    def automate_ingestion(self, topic: str):
        """Runs the end-to-end ingestion pipeline."""
        print(f"Ingestion Pipeline: Starting for {topic}...")
        
        # 1. Research
        results = self.research.perform_deep_research(topic)
        
        # 2. Extract DNA
        dna = results.get("learning_dna", {})
        
        # 3. Commit to DNA Core
        dna_file = self.dna_dir / f"{topic.lower().replace(' ', '_')}_dna.json"
        with open(dna_file, "w", encoding="utf-8") as f:
            json.dump(dna, f, indent=4)
            
        # 4. Emit Growth Signal
        self.signals.emit_signal(
            "GROWTH",
            {"topic": topic, "dna_file": str(dna_file.relative_to(self.base_dir))},
            ttl_seconds=3600,
            evidentiality="!"
        )
        
        print(f"Ingestion Pipeline: Complete. DNA committed to {dna_file.name}")
        return dna

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="Topic to ingest")
    args = parser.parse_args()
    
    base = Path(__file__).resolve().parent.parent.parent.parent
    NutrientIngestion(base).automate_ingestion(args.topic)

