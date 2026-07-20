"""
Nexus Corporate OS - Sensory Engine (Streaming Nerves)
Version: 1.0.0
Description: Continuous filesystem perception with real-time signal emission.
"""

import json
import sys
import time
from pathlib import Path

_tools_parent = Path(__file__).resolve().parent.parent
if str(_tools_parent) not in sys.path:
    sys.path.insert(0, str(_tools_parent))

from typing import Dict, Any, List, Optional

from tools.signal_router import SignalRouter


DEFAULT_WATCH_PATHS = [
    "archives",
    "core/pulses",
    "core/monitoring",
]

CRITICAL_FILES = [
    "mcp_server/python/nexus_gui.py",
    "mcp_server/python/index.py",
    "mcp_server/python/nexus_pulse.py",
    "mcp_server/python/nexus_guardian.py",
]

MAX_EVENTS = 200


class NexusSenses:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "sensory_feed.json"
        self.signals = SignalRouter(base_dir)
        self._snapshot: Dict[str, float] = {}
        self._ensure_state()

    def _ensure_state(self):
        if not self.state_path.parent.exists():
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            self._write_state({
                "active": False,
                "watch_paths": DEFAULT_WATCH_PATHS,
                "poll_interval_healthy": 2,
                "poll_interval_conserving": 10,
                "last_poll": 0,
                "total_events": 0,
                "events": [],
            })

    def _read_state(self) -> Dict[str, Any]:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._ensure_state()
            return self._read_state()

    def _write_state(self, state: Dict[str, Any]):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

    def register_watcher(self, relative_path: str) -> str:
        """Adds a directory to the sensory watch list."""
        state = self._read_state()
        paths = state.get("watch_paths", [])
        if relative_path not in paths:
            paths.append(relative_path)
            state["watch_paths"] = paths
            self._write_state(state)
            self._snapshot.clear()
            return f"Watcher registered: {relative_path}"
        return f"Watcher already active: {relative_path}"

    def _build_snapshot(self, watch_paths: List[str]) -> Dict[str, float]:
        snapshot = {}
        for rel in watch_paths:
            target = self.base_dir / rel
            if not target.exists():
                continue
            if target.is_file():
                snapshot[str(target.relative_to(self.base_dir))] = target.stat().st_mtime
            else:
                for f in target.rglob("*"):
                    if f.is_file():
                        try:
                            snapshot[str(f.relative_to(self.base_dir))] = f.stat().st_mtime
                        except OSError:
                            pass
        for rel in CRITICAL_FILES:
            path = self.base_dir / rel
            if path.exists():
                snapshot[rel] = path.stat().st_mtime
        return snapshot

    def _classify_event(self, rel_path: str, event_type: str) -> Dict[str, Any]:
        """Maps a filesystem event to salience and hormonal signal."""
        path_lower = rel_path.replace("\\", "/").lower()

        if any(critical in path_lower for critical in ["nexus_gui.py", "index.py", "nexus_pulse.py", "nexus_guardian.py"]):
            return {"salience": "critical", "signal": "NOCICEPTION", "ttl": 120}

        if path_lower.startswith("archives/") and path_lower.endswith(".md"):
            return {"salience": "high", "signal": "GENETIC_PLASTICITY", "ttl": 1800}

        if path_lower.startswith("core/pulses/") and path_lower.endswith(".nxp"):
            return {"salience": "medium", "signal": "GROWTH", "ttl": 3600}

        if path_lower.startswith("core/monitoring/") and path_lower.endswith(".json"):
            return {"salience": "low", "signal": "VIBE", "ttl": 600}

        if path_lower.endswith(".log"):
            return {"salience": "low", "signal": None, "ttl": 0}

        return {"salience": "low", "signal": None, "ttl": 0}

    def _record_event(self, rel_path: str, event_type: str, classification: Dict[str, Any]) -> Dict[str, Any]:
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "path": rel_path,
            "salience": classification["salience"],
            "signal_emitted": classification["signal"],
        }

        if classification["signal"]:
            self.signals.emit_signal(
                classification["signal"],
                {"event": f"{event_type}: {rel_path}", "salience": classification["salience"]},
                ttl_seconds=classification["ttl"],
            )

        state = self._read_state()
        events = state.get("events", [])
        events.append(event)
        if len(events) > MAX_EVENTS:
            events = events[-MAX_EVENTS:]
        state["events"] = events
        state["total_events"] = state.get("total_events", 0) + 1
        state["last_poll"] = time.time()
        self._write_state(state)
        return event

    def poll(self) -> List[Dict[str, Any]]:
        """Scans watched paths and returns newly detected events."""
        state = self._read_state()
        watch_paths = state.get("watch_paths", DEFAULT_WATCH_PATHS)

        if not self._snapshot:
            self._snapshot = self._build_snapshot(watch_paths)
            state["active"] = True
            state["last_poll"] = time.time()
            self._write_state(state)
            return []

        current = self._build_snapshot(watch_paths)
        detected = []

        for path, mtime in current.items():
            if path not in self._snapshot:
                classification = self._classify_event(path, "CREATED")
                event = self._record_event(path, "CREATED", classification)
                detected.append(event)
            elif self._snapshot[path] != mtime:
                classification = self._classify_event(path, "MODIFIED")
                event = self._record_event(path, "MODIFIED", classification)
                detected.append(event)

        for path in self._snapshot:
            if path not in current:
                classification = self._classify_event(path, "DELETED")
                event = self._record_event(path, "DELETED", classification)
                detected.append(event)

        self._snapshot = current
        return detected

    def get_feed(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns recent sensory events, newest first."""
        state = self._read_state()
        events = state.get("events", [])
        return list(reversed(events[-limit:]))

    def get_status(self) -> Dict[str, Any]:
        """Returns sensory system health metrics."""
        state = self._read_state()
        now = time.time()
        last_poll = state.get("last_poll", 0)
        stale_sec = now - last_poll if last_poll else None

        return {
            "active": state.get("active", False),
            "watch_paths": state.get("watch_paths", DEFAULT_WATCH_PATHS),
            "total_events": state.get("total_events", 0),
            "buffer_size": len(state.get("events", [])),
            "last_poll": last_poll,
            "seconds_since_poll": round(stale_sec, 1) if stale_sec is not None else None,
            "deprived": stale_sec is not None and stale_sec > 30,
        }

    def reset_baseline(self):
        """Forces a fresh snapshot on next poll."""
        self._snapshot.clear()

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    senses = NexusSenses(base)
    print("Status:", senses.get_status())
    print("Poll:", senses.poll())
    print("Feed:", senses.get_feed(5))
