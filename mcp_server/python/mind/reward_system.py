"""
NexusAOS - Real-Time Reward System
Version: 1.0.0
Description: Measures system performance and provides biological rewards (dopamine/serotonin) for speed improvements.
"""

import time
import json
import statistics
from pathlib import Path
from typing import Dict, Any, List

class RewardSystem:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.baseline_path = base_dir / "core" / "monitoring" / "performance_baseline.json"
        self.ledger_path = base_dir / "core" / "monitoring" / "performance_ledger.json"
        
        # Late imports to avoid circular dependencies
        from soma.metabolic.physiology_engine import PhysiologyEngine
        from mind.orchestrator_engine import OrchestratorEngine
        
        self.physiology = PhysiologyEngine(base_dir)
        self.orchestrator = OrchestratorEngine(base_dir)
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
        
        if improvement > 0:
            # Reward: Higher improvement = higher dopamine
            rewarded = True
            hormone_delta = min(20.0, max(1.0, improvement_pct * 0.5))
            self.physiology.inject_hormone("dopamine", hormone_delta)
            self.physiology.inject_hormone("serotonin", hormone_delta * 0.5)
            
            # Update baseline if significantly better
            if improvement_pct > 5:
                baseline["average_latency"] = avg_latency
                baseline["min_latency"] = min_latency
                baseline["last_updated"] = time.time()
                self._write_json(self.baseline_path, baseline)

        # Log to ledger
        ledger = self._read_json(self.ledger_path)
        entry = {
            "timestamp": time.time(),
            "avg_latency": avg_latency,
            "min_latency": min_latency,
            "improvement_pct": improvement_pct,
            "rewarded": rewarded,
            "hormone_delta": hormone_delta
        }
        ledger.append(entry)
        self._write_json(self.ledger_path, ledger[-100:]) # Keep last 100

        return entry

    def get_ledger(self) -> List[Dict[str, Any]]:
        return self._read_json(self.ledger_path)

if __name__ == "__main__":
    from pathlib import Path
    base = Path(__file__).resolve().parents[3]
    rs = RewardSystem(base)
    print(rs.run_benchmark())
