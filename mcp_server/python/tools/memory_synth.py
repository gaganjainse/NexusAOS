"""
Nexus Corporate OS - Memory Synth
Version: 1.0.0
Description: Synthesizes historical task data into learned patterns and wisdom.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

class MemorySynth:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.lattice_path = base_dir / "core" / "monitoring" / "lattice_state.json"
        self.learning_dir = base_dir / "archives" / "core" / "learning"
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.learning_dir.exists():
            self.learning_dir.mkdir(parents=True, exist_ok=True)

    def consolidate(self) -> str:
        """Processes historical tasks and generates learning artifacts."""
        try:
            with open(self.lattice_path, "r", encoding="utf-8") as f:
                history = json.load(f).get("history", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return "No history found for consolidation."

        if not history:
            return "History is empty. No memories to consolidate."

        # 1. Pattern Analysis: Common Paths
        paths = [f"{t['from']} -> {t['to']}" for t in history]
        path_counts = Counter(paths)

        # 2. Success Rate Analysis
        # (Assuming 'result' existence implies success for now)
        successes = [p for p in history if "result" in p]

        # 3. Generate Learning Artifact
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.learning_dir / f"consolidation_{timestamp}.md"

        report = [
            f"# Learning Consolidation Report: {timestamp}",
            f"\n**Consolidated Tasks:** {len(history)}",
            f"**Success Rate:** {(len(successes)/len(history))*100:.1f}%",
            "\n## Observed Synaptic Patterns",
            "| Pattern | Frequency | Status |",
            "| :--- | :--- | :--- |"
        ]

        for path, count in path_counts.most_common(5):
            status = "Strong" if count > 3 else "Emerging"
            report.append(f"| {path} | {count} | {status} |")

        report.append("\n## Synaptic Pruning Recommendations")
        # Placeholder for pruning logic
        report.append("- No nodes recommended for pruning at this time.")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))

        return f"Memory Consolidation Complete. Artifact: {report_path.name}"

    def get_wisdom_summary(self) -> dict:
        """Returns a high-level summary of consolidated learning."""
        reports = list(self.learning_dir.glob("consolidation_*.md"))
        return {
            "total_memories": len(reports),
            "last_consolidation": reports[-1].name if reports else "Never"
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    synth = MemorySynth(base)
    print(synth.consolidate())
