"""
Nexus Corporate OS - Signal Router
Version: 1.0.0
Description: Manages global "Hormonal Signals" with time-based decay (TTL).
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

class SignalRouter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signal_path = base_dir / "core" / "monitoring" / "signals.json"
        self._ensure_signal_file()

    def _ensure_signal_file(self):
        if not self.signal_path.parent.exists():
            self.signal_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.signal_path.exists():
            with open(self.signal_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def emit_signal(self, signal_type: str, payload: Dict[str, Any], ttl_seconds: int = 300):
        """Emits a signal with a specific TTL (Time To Live)."""
        signals = self._read_signals()
        signals[signal_type] = {
            "payload": payload,
            "expires_at": time.time() + ttl_seconds,
            "emitted_at": time.time()
        }
        self._write_signals(signals)
        return f"Signal '{signal_type}' emitted. TTL: {ttl_seconds}s"

    def get_active_signals(self) -> Dict[str, Any]:
        """Returns all signals that haven't expired, cleaning up the file in the process."""
        signals = self._read_signals()
        now = time.time()
        active_signals = {}
        changed = False

        for sig_type, data in signals.items():
            if data["expires_at"] > now:
                active_signals[sig_type] = data
            else:
                changed = True

        if changed:
            self._write_signals(active_signals)

        return active_signals

    def _read_signals(self) -> Dict[str, Any]:
        try:
            with open(self.signal_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_signals(self, signals: Dict[str, Any]):
        with open(self.signal_path, "w", encoding="utf-8") as f:
            json.dump(signals, f, indent=4)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    router = SignalRouter(base)
    print(router.emit_signal("ADRENALINE", {"event": "System Start"}, ttl_seconds=10))
    print("Active Signals:", router.get_active_signals())
