"""
NexusAOS - Privacy Shield (L08)
Version: 1.0.0
Description: Security and Privacy Sentry. Detects telemetry leaks and hardens the Windows host.
"""

import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any, List

class PrivacyShield:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.report_dir = base_dir / "archives" / "dna_core" / "security"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def scan_telemetry_leaks(self) -> Dict[str, Any]:
        """Scans for active connections to known telemetry endpoints."""
        results = {
            "microsoft_telemetry": [],
            "google_telemetry": [],
            "other_leaks": [],
            "timestamp": time.time()
        }
        
        try:
            # Check for common telemetry processes
            process_output = subprocess.check_output("tasklist /v", shell=True).decode(errors='ignore')
            telemetry_keywords = ["CompatTelRunner", "DeviceCensus", "mscorsvw", "vctip"]
            
            for kw in telemetry_keywords:
                if kw in process_output:
                    results["microsoft_telemetry"].append(f"Detected active process: {kw}")

            # Check network connections (Requires admin for full detail, but basic check works)
            net_output = subprocess.check_output("netstat -ano", shell=True).decode(errors='ignore')
            if "google" in net_output:
                 results["google_telemetry"].append("Detected active connections to Google-related IPs.")
                 
        except Exception as e:
            results["error"] = str(e)
            
        return results

    def harden_kernel_proposal(self) -> List[str]:
        """Generates proposals for hardening the Windows kernel."""
        proposals = [
            "Disable Connected User Experiences and Telemetry (DiagTrack) service.",
            "Disable Windows Error Reporting Service (WerSvc).",
            "Set 'AllowTelemetry' to 0 in Registry.",
            "Block outbound telemetry ports (443 to telemetry.microsoft.com) via Firewall."
        ]
        return proposals

    def shred_trash(self) -> Dict[str, Any]:
        """Identifies digital waste and orphaned files."""
        waste_stats = {"total_waste_kb": 0, "files_found": 0}
        temp_paths = [os.environ.get('TEMP'), os.environ.get('SystemRoot') + "\\Temp"]
        
        for p in temp_paths:
            if not p: continue
            path = Path(p)
            if path.exists():
                for f in path.glob("*"):
                    try:
                        waste_stats["total_waste_kb"] += f.stat().st_size / 1024
                        waste_stats["files_found"] += 1
                    except: pass
                    
        return waste_stats

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    shield = PrivacyShield(base)
    print(json.dumps(shield.scan_telemetry_leaks(), indent=2))
