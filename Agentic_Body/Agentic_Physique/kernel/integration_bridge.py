"""
SeshaAOS - Integration Bridge (L7)
Version: 13.0.0
Description: The Skin - Connects Sesha to Host OS vitals.
"""

from pathlib import Path
from typing import Any
import json
import os
import shutil
import subprocess
import sys
import time

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from Agentic_Body.Agentic_Physique.nervous.signal_router import SignalRouter

class IntegrationBridge:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        
        from Agentic_Body.Agentic_Intelligence.tools.google_cloud_receptor import GoogleCloudReceptor
        self.cloud = GoogleCloudReceptor(base_dir)

    def scan_host_vitals(self) -> dict[str, Any]:
        """Scans the host (Windows/Linux) and emits biosignals."""
        vitals = {}
        
        # 1. Disk Pressure (Ischemia Analog)
        try:
            total, used, free = shutil.disk_usage(self.base_dir)
            disk_pct = (used / total) * 100
            vitals["disk_pressure"] = disk_pct
            
            if disk_pct > 90:
                self.signals.emit_signal("ISCHEMIA", {"source": "disk", "level": disk_pct}, ttl_seconds=600)
        except Exception:  # noqa: BLE001
            pass
        
        # 2. CPU Pressure (Hypoxia Analog)
        try:
            res = subprocess.check_output("wmic cpu get loadpercentage", shell=True).decode()
            load = float(res.split("\n")[1].strip())
            vitals["cpu_load"] = load
            
            if load > 85:
                self.signals.emit_signal("HYPOXIA", {"source": "cpu", "level": load}, ttl_seconds=300)
        except Exception:  # noqa: BLE001
            pass
        except Exception:  # noqa: BLE001
            pass
        
        return vitals

    def execute_with_backoff(self, func: callable, *args, **kwargs) -> Any:
        """Executes a cloud function with jittered exponential backoff."""
        attempt = 1
        max_attempts = 4
        
        while attempt <= max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                err_msg = str(e).upper()
                if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
                    # Trigger Somatic Hibernation
                    from Agentic_Body.Agentic_Physique.physiology_engine import PhysiologyEngine
                    phys = PhysiologyEngine(self.base_dir)
                    phys.trigger_hibernation(429)
                    
                    wait_time = self.cloud.handle_resource_exhaustion(attempt)
                    time.sleep(wait_time)
                    attempt += 1
                else:
                    raise e
        
        raise RuntimeError("Cloud connection paralyzed after max retries.")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    bridge = IntegrationBridge(base)
    print(json.dumps(bridge.scan_host_vitals(), indent=2))
