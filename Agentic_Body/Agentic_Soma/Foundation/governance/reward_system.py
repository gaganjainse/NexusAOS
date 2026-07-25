# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - Real-Time Reward System
Version: 1.0.0
Description: Measures system performance and provides biological rewards (dopamine/serotonin) for speed improvements.
"""

import json
import statistics
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

class RewardSystem:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.baseline_path = base_dir / "core" / "monitoring" / "performance_baseline.json"
        self.ledger_path = base_dir / "core" / "monitoring" / "performance_ledger.json"
        
        # Late imports to avoid circular dependencies
        from layers.L02_Agent.endocrine_engine import EndocrineEngine
        from layers.L01_Planning.orchestrator_engine import OrchestratorEngine
        from layers.L08_Governance.moral_cortex import MoralCortex
        
        self.endocrine = EndocrineEngine(base_dir)
        self.orchestrator = OrchestratorEngine(base_dir)
        self.morals = MoralCortex(base_dir)
        
        from layers.L00_Experience.performance_visualizer import PerformanceVisualizer
        self.visualizer = PerformanceVisualizer(base_dir)
        
        self._ensure_paths()

    def _ensure_paths(self):
        self.baseline_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.baseline_path.exists():
            with open(self.baseline_path, "w", encoding="utf-8") as f:
                json.dump({"average_latency": 0.5, "min_latency": 0.5, "last_updated": 0}, f, indent=4)
        if not self.ledger_path.exists():
            with open(self.ledger_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def _read_json(self, path: Path) -> Any:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _write_json(self, path: Path, data: Any):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def run_benchmark(self, iterations: int = 5) -> Dict[str, Any]:
        """Runs a performance benchmark and calculates the reward."""
        latencies = []
        
        # 1. Warm up
        self.orchestrator.tick()
        
        # 2. Measure
        for _ in range(iterations):
            start = time.perf_counter()
            self.orchestrator.tick()
            latencies.append(time.perf_counter() - start)
            
        avg_latency = statistics.mean(latencies)
        min_latency = min(latencies)
        
        baseline = self._read_json(self.baseline_path)
        old_avg = baseline.get("average_latency", 0.5)
        
        improvement = old_avg - avg_latency
        improvement_pct = (improvement / old_avg) * 100 if old_avg > 0 else 0
        
        rewarded = False
        hormone_delta = 0.0
        punished = False
        
        if improvement > 0:
            # Reward: Higher improvement = higher dopamine
            rewarded = True
            hormone_delta = min(20.0, max(1.0, improvement_pct * 0.5))
            self.endocrine.inject("dopamine", hormone_delta)
            self.endocrine.inject("serotonin", hormone_delta * 0.5)
            
            # Update baseline if significantly better
            if improvement_pct > 5:
                baseline["average_latency"] = avg_latency
                baseline["min_latency"] = min_latency
                baseline["last_updated"] = time.time()
                self._write_json(self.baseline_path, baseline)
        else:
            # Punishment: Performance drop = cortisol spike
            punished = True
            punish_delta = min(15.0, abs(improvement_pct) * 0.3)
            self.endocrine.inject("cortisol", punish_delta)
            self.endocrine.inject("dopamine", -punish_delta * 0.5)

        # Log to ledger
        ledger = self._read_json(self.ledger_path)
        entry = {
            "timestamp": time.time(),
            "avg_latency": avg_latency,
            "min_latency": min_latency,
            "improvement_pct": improvement_pct,
            "rewarded": rewarded,
            "punished": punished,
            "hormone_delta": hormone_delta
        }
        ledger.append(entry)
        self._write_json(self.ledger_path, ledger[-100:]) # Keep last 100

        # Generate visual reward
        self.visualizer.generate_reward_artifact(entry)

        return entry

    def get_ledger(self) -> List[Dict[str, Any]]:
        return self._read_json(self.ledger_path)

if __name__ == "__main__":

    base = Path(__file__).resolve().parents[3]
    rs = RewardSystem(base)
    print(rs.run_benchmark())

