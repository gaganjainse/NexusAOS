"""
NexusAOS - Integration Bridge (L7)
Version: 13.0.0
Description: The Skin - Connects Nexus to Host OS vitals and maps system events to biosignals.
"""

import os
import shutil
import time
import subprocess
from pathlib import Path
from typing import Dict, Any

class IntegrationBridge:
    """Universal Host Bridge - Translates hardware pressure into physiological signals."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        from soma.nervous.signal_router import SignalRouter
        self.signals = SignalRouter(base_dir)

    def scan_host_vitals(self) -> Dict[str, Any]:
        """Scans the host (Windows/Linux) and emits biosignals."""
        vitals = {}
        
        # 1. Disk Pressure (Ischemia Analog)
        total, used, free = shutil.disk_usage(self.base_dir)
        disk_pct = (used / total) * 100
        vitals["disk_pressure"] = disk_pct
        
        if disk_pct > 90:
            self.signals.emit_signal("ISCHEMIA", {"source": "disk", "level": disk_pct}, ttl_seconds=600, evidentiality="!")
            
        # 2. CPU Pressure (Hypoxia Analog)
        # Using a simple portable check via 'wmic' for Windows
        try:
            res = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode()
            load = float(res.split("\n")[1].strip())
            vitals["cpu_load"] = load
            
            if load > 85:
                self.signals.emit_signal("HYPOXIA", {"source": "cpu", "level": load}, ttl_seconds=300, evidentiality="!")
        except:
            pass
            
        return vitals

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2]
    bridge = IntegrationBridge(base)
    print("Scanning Host Vitals...")
    print(json.dumps(bridge.scan_host_vitals(), indent=2))

import json
