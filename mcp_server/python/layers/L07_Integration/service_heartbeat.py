"""
NexusAOS - Service Heartbeat
Version: 1.0.0
Description: Liveness signals for autonomic background services.
"""

import json
import os
import time

from typing import Dict, Any, List, Optional

from pathlib import Path
import sys
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))


class ServiceHeartbeat:
    def __init__(self, base_dir: Path, service_name: str):
        self.base_dir = base_dir
        self.service_name = service_name
        self.heartbeat_dir = base_dir / "core" / "monitoring" / "heartbeats"
        self.heartbeat_path = self.heartbeat_dir / f"{service_name}.json"
        self._ensure_dir()

    def _ensure_dir(self):
        if not self.heartbeat_dir.exists():
            self.heartbeat_dir.mkdir(parents=True, exist_ok=True)

    def beat(self, status: str = "alive", metadata: Optional[Dict[str, Any]] = None):
        payload = {
            "service": self.service_name,
            "status": status,
            "timestamp": time.time(),
            "pid": os.getpid(),
            "metadata": metadata or {},
        }
        with open(self.heartbeat_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

    def read(self) -> Optional[Dict[str, Any]]:
        if not self.heartbeat_path.exists():
            return None
        try:
            with open(self.heartbeat_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def is_stale(self, max_age_seconds: float) -> bool:
        data = self.read()
        if not data:
            return True
        return (time.time() - data.get("timestamp", 0)) > max_age_seconds

    @staticmethod
    def all_services(base_dir: Path) -> List[Dict[str, Any]]:
        hb_dir = base_dir / "core" / "monitoring" / "heartbeats"
        if not hb_dir.exists():
            return []
        results = []
        for path in hb_dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    results.append(json.load(f))
            except (json.JSONDecodeError, OSError):
                results.append({"service": path.stem, "status": "corrupt", "timestamp": 0})
        return results
