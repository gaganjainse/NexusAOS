"""
Nexus Corporate OS - The Liver
Version: 1.0.0
Description: Filters "Data Toxins" (redundant logs, stale reports) to prevent bloat.
"""

import os
import time
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta

class NexusLiver:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.bladder_dir = base_dir / "archives" / "excreta"
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.bladder_dir.exists():
            self.bladder_dir.mkdir(parents=True, exist_ok=True)

    def filter_toxins(self) -> str:
        """Executes a full filtration cycle."""
        report = ["--- Liver Filtration Report ---"]

        # 1. Log Rotation
        rotated = self._rotate_logs()
        report.append(f"[METABOLISM] Log Rotation: {rotated} files truncated.")

        # 2. Archive Pruning (Stale Wisdom)
        pruned = self._prune_stale_reports()
        report.append(f"[WISDOM] Stale Reports: {pruned} artifacts moved to Bladder.")

        # 3. Lattice Compaction
        compacted = self._compact_lattice_history()
        report.append(f"[NERVOUS] Lattice Compaction: {compacted} tasks flushed.")

        return "\n".join(report)

    def _rotate_logs(self):
        count = 0
        max_size = 5 * 1024 * 1024 # 5MB
        for log_file in self.base_dir.rglob("*.log"):
            if log_file.stat().st_size > max_size:
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                # Keep last 50%
                half = len(lines) // 2
                with open(log_file, "w", encoding="utf-8") as f:
                    f.writelines(lines[half:])
                count += 1
        return count

    def _prune_stale_reports(self):
        count = 0
        learn_dir = self.base_dir / "archives" / "core" / "learning"
        if learn_dir.exists():
            threshold = datetime.now() - timedelta(days=30)
            for report in learn_dir.glob("consolidation_*.md"):
                if datetime.fromtimestamp(report.stat().st_mtime) < threshold:
                    shutil.move(str(report), str(self.bladder_dir / report.name))
                    count += 1
        return count

    def _compact_lattice_history(self):
        lattice_path = self.base_dir / "core" / "monitoring" / "lattice_state.json"
        if not lattice_path.exists():
            lattice_path = self.base_dir / "mcp_server" / "core" / "monitoring" / "lattice_state.json"

        if lattice_path.exists():
            try:
                with open(lattice_path, "r", encoding="utf-8") as f:
                    state = json.load(f)

                old_count = len(state.get("history", []))
                if old_count > 50:
                    state["history"] = state["history"][-20:] # Keep only recent 20
                    with open(lattice_path, "w", encoding="utf-8") as f:
                        json.dump(state, f, indent=4)
                    return old_count - 20
            except: pass
        return 0

    def get_toxic_load(self) -> dict:
        """Calculates current system toxicity metrics."""
        total_log_size = sum(f.stat().st_size for f in self.base_dir.rglob("*.log"))
        stale_count = 0
        learn_dir = self.base_dir / "archives" / "core" / "learning"
        if learn_dir.exists():
            stale_count = len(list(learn_dir.glob("consolidation_*.md")))

        return {
            "log_load_bytes": total_log_size,
            "stale_artifact_count": stale_count,
            "toxicity_pct": min(100.0, (total_log_size / (50 * 1024 * 1024)) * 100) # Threshold 50MB
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    liver = NexusLiver(base)
    print(liver.filter_toxins())
    print("Toxic Load:", liver.get_toxic_load())
