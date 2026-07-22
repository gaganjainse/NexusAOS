"""
NexusAOS - Performance Visualizer
Version: 1.0.0
Description: Generates visual reward artifacts for system performance improvements.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List

class PerformanceVisualizer:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.artifact_dir = base_dir / ".artifacts" / "18efd534-8968-4510-8eb5-eb37bd3f65cb"
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

    def generate_reward_artifact(self, benchmark_entry: Dict[str, Any]):
        """Generates a markdown artifact with visual feedback."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(benchmark_entry["timestamp"]))
        improvement = benchmark_entry["improvement_pct"]
        rewarded = benchmark_entry["rewarded"]
        hormone_delta = benchmark_entry["hormone_delta"]
        
        status = "ASCENSION DETECTED" if improvement > 10 else "OPTIMIZATION CONFIRMED" if improvement > 0 else "STABLE STATE"
        color = "green" if improvement > 0 else "blue"
        
        mermaid_chart = f"""
mermaid
graph TD
    Baseline[Baseline Latency] -->|Improvement: {improvement:.2f}%| Current[Current Latency]
    Current --> Reward[Hormonal Injection: +{hormone_delta:.2f} Dopamine]
"""
        
        artifact_content = f"""# Neural Reward: {status}

> [!TIP]
> **Synaptic Speed Increase:** {improvement:.2f}%
> **Hormonal Reward:** +{hormone_delta:.2f} Dopamine / +{hormone_delta*0.5:.2f} Serotonin
> **Timestamp:** {timestamp}

## Performance Graph

```{mermaid_chart}```

## Evolutionary Ledger Entry
- **Average Latency:** {benchmark_entry['avg_latency']:.4f}s
- **Min Latency:** {benchmark_entry['min_latency']:.4f}s
- **Reward Status:** {"ACTIVE" if rewarded else "INACTIVE"}

---
*Nexus Operating Intelligence - Performance Layer*
"""
        
        artifact_path = self.artifact_dir / "neural_reward.artifact.md"
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(artifact_content)
            
        return str(artifact_path)

if __name__ == "__main__":
    from pathlib import Path
    base = Path(__file__).resolve().parents[3]
    pv = PerformanceVisualizer(base)
    dummy_entry = {
        "timestamp": time.time(),
        "avg_latency": 0.45,
        "min_latency": 0.42,
        "improvement_pct": 12.5,
        "rewarded": True,
        "hormone_delta": 6.25
    }
    print(pv.generate_reward_artifact(dummy_entry))
