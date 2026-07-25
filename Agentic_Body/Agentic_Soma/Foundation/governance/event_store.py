# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - Event Store
Version: 1.0.0
Description: Structured event log for system events.
"""
import json
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent


class EventStore:
    """Structured event store using WAL as backend."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.events_dir = base_dir / "core" / "monitoring" / "events"
        self.events_dir.mkdir(parents=True, exist_ok=True)
        self.current_log = self.events_dir / f"events_{int(time.time())}.jsonl"

    def append(self, event_type: str, data: Dict):
        """Append an event to the store."""
        event = {
            "id": f"{int(time.time())}",
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        }
        with open(self.current_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def get_recent(self, limit: int = 100) -> List[Dict]:
        """Get recent events from the store."""
        events = []
        for log_file in sorted(self.events_dir.glob("*.jsonl"), reverse=True):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            events.append(json.loads(line))
                            if len(events) >= limit:
                                return events
                        except json.JSONDecodeError:
                            continue
        return events

