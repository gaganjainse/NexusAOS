"""
SeshaAOS - Native Senses (Watchdog-Based File Watching)
Version: 15.0.0
Description: Real-time filesystem monitoring for sensory events using watchdog.
"""
from pathlib import Path
from typing import Optional
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class SensesHandler(FileSystemEventHandler):
    def __init__(self, recorder):
        self.recorder = recorder

    def on_modified(self, event):
        if not event.is_directory:
            self.recorder.record_event("MODIFIED", event.src_path, "medium")

    def on_created(self, event):
        self.recorder.record_event("CREATED", event.src_path, "high")

class NativeSenses:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.watch_paths: list[Path] = []
        self.events: list[dict] = []
        self.observer = Observer()
        self.handler = SensesHandler(self)

    def register_watch(self, relative_path: str) -> dict:
        full_path = self.base_dir / relative_path
        if full_path.exists() and full_path not in self.watch_paths:
            self.watch_paths.append(full_path)
            self.observer.schedule(self.handler, str(full_path), recursive=True)
            if not self.observer.is_alive():
                self.observer.start()
        return {"status": "registered", "path": str(full_path)}

    def poll_events(self, limit: int = 25) -> list[dict]:
        """Get recent sensory events."""
        return self.events[-limit:]

    def record_event(self, event_type: str, path: str, salience: str = "low"):
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "path": path,
            "salience": salience
        }
        self.events.append(event)
        print(f"[SENSE] {event_type}: {path} ({salience})")

    def shutdown(self):
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
