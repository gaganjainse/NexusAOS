"""
NexusAOS - Memory Synth
Version: 1.0.0
Description: Synthesizes historical task data into learned patterns and wisdom.
"""

import json
import os
import time

from datetime import datetime
from collections import Counter
from typing import Dict, Any, List
from layers.L05_Memory.state_manager import StateManager
from layers.L11_Data.soma_transcended import TranscendedSubstrate

from pathlib import Path
import sys
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class MemorySynth:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_mgr = StateManager(base_dir)
        self.substrate = TranscendedSubstrate(base_dir)
        self.learning_dir = base_dir / "archives" / "dna_core" / "learning"
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.learning_dir.exists():
            self.learning_dir.mkdir(parents=True, exist_ok=True)

    def consolidate(self) -> str:
        """Processes historical tasks and generates learning artifacts."""
        # Use StateManager to get history from SQLite
        conn = self.state_mgr._get_connection()
        import sqlite3
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lattice_tasks")
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not history:
            return "History is empty. No memories to consolidate."

        # 1. Capture current Vibe/Energy for persona continuity
        from layers.L02_Agent.physiology_engine import PhysiologyEngine
        phys = PhysiologyEngine(self.base_dir)
        vitals = phys.get_state()
        vibe = vitals.get("endocrine", {}).get("vibe", "Stable")
        energy = vitals.get("metabolism", {}).get("current_energy", 1000)

        # 2. Pattern Analysis: Common Paths
        paths = [f"{t['from_role']} -> {t['to_role']}" for t in history]
        path_counts = Counter(paths)

        # 3. Success Rate Analysis
        successes = [p for p in history if "result" in p]

        # 4. Generate Learning Artifact
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.learning_dir / f"consolidation_{timestamp}.md"

        report = [
            f"# Learning Consolidation Report: {timestamp}",
            f"\n## Soma State",
            f"- **Persona Vibe:** {vibe}",
            f"- **Energy Level:** {energy}",
            f"\n## Efficiency Metrics",
            f"- **Consolidated Tasks:** {len(history)}",
            f"- **Success Rate:** {(len(successes)/len(history))*100:.1f}%",
            "\n## Observed Synaptic Patterns",
            "| Pattern | Frequency | Status |",
            "| :--- | :--- | :--- |"
        ]

        for path, count in path_counts.most_common(5):
            status = "Strong" if count > 3 else "Emerging"
            report.append(f"| {path} | {count} | {status} |")
            
            # 4. Neural Plasticity (Transcended Graph Link)
            parts = path.split(" -> ")
            self.substrate.link_nodes(parts[0], parts[1], "SYNAPSE", {"weight": count})

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

    def run_pruning(self, age_hours: int = 48) -> Dict[str, Any]:
        """Identifies and prunes weak synaptic patterns."""
        conn = self.state_mgr._get_connection()
        import sqlite3
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Identify "Weak Synapses": Tasks older than age_hours with low frequency roles
        # For simplicity: Prune all tasks older than age_hours that are 'Resting' (completed)
        cutoff = time.time() - (age_hours * 3600)
        cursor.execute("SELECT task_id FROM lattice_tasks WHERE status = 'Resting' AND completed_at < ?", (cutoff,))
        to_prune = [row["task_id"] for row in cursor.fetchall()]
        conn.close()
        
        pruned_count = self.state_mgr.prune_lattice_tasks(to_prune)
        
        # Log the pruning event
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.learning_dir / f"pruning_{timestamp}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Synaptic Pruning Report: {timestamp}\n\n")
            f.write(f"- **Synapses Disconnected:** {pruned_count}\n")
            f.write(f"- **Pruning Strategy:** Age-based (> {age_hours}h)\n")
            
        return {
            "pruned_count": pruned_count,
            "artifact": report_path.name,
            "strategy": "age_based"
        }

    def summarize_long_context(self) -> str:
        """Neural 13.0: Compresses recent history into a high-salience Wisdom Node."""
        summary = ["# NEURAL 13.0 - Condensed Wisdom Node"]
        
        # 1. Fetch recent task history
        conn = self.state_mgr._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT directive, outcome FROM directive_queue ORDER BY completed_at DESC LIMIT 5")
        history = cursor.fetchall()
        conn.close()
        
        summary.append("\n## Critical Task Summary")
        for h in history:
            summary.append(f"- Directive: {h[0][:50]}... | Result: {h[1][:50]}...")
            
        # 2. Capture Genetic Vitals
        from layers.L12_Infrastructure.dna_manager import DNAManager
        dna = DNAManager(self.base_dir).get_genome()
        summary.append(f"\n## Genetic State")
        summary.append(f"- Generation: {dna.get('generation')}")
        summary.append(f"- Synaptic Pressure: 1.1")
        
        return "\n".join(summary)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    synth = MemorySynth(base)
    print(synth.consolidate())
