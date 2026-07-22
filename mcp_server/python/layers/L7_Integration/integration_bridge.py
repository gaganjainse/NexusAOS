"""
NexusAOS - Integration Bridge (L7)
Version: 13.0.0
Description: The Skin - Connects Nexus to Host OS vitals.
"""

import os
import shutil
import time
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any

# Ensure root is in path
_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from layers.L2_Substrate.signal_router import SignalRouter

class IntegrationBridge:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)

    def scan_host_vitals(self) -> Dict[str, Any]:
        vitals = {}
        total, used, free = shutil.disk_usage(self.base_dir)
        disk_pct = (used / total) * 100
        vitals["disk_pressure"] = disk_pct
        
        if disk_pct > 90:
            self.signals.emit_signal("ISCHEMIA", {"source": "disk", "level": disk_pct}, ttl_seconds=600)
            
        return vitals

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    bridge = IntegrationBridge(base)
    print(json.dumps(bridge.scan_host_vitals(), indent=2))
