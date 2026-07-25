"""
SeshaAOS - State WAL (Write-Ahead Log)
Version: 1.0.0
Description: Standalone WAL wrapper for state persistence.
"""
from pathlib import Path
from typing import Dict
import json
import sys
import time

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent


class StateWAL:
    """Append-only write-ahead log for state reconstruction."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.wal_dir = base_dir / "core" / "monitoring" / "wal"
        self.wal_dir.mkdir(parents=True, exist_ok=True)
        self.wal_file = self.wal_dir / "state.wal"

    def append(self, event_type: str, data: Dict) -> None:
        """Append an event to the WAL."""
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        }
        with open(self.wal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def read_all(self) -> list[Dict]:
        """Read all events from the WAL."""
        events = []
        if not self.wal_file.exists():
            return events
        with open(self.wal_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return events

    def truncate(self) -> None:
        """Clear the WAL (after snapshot)."""
        self.wal_file.write_text("")
