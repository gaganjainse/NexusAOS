# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - Physiology Engine (Unified) — Specialization Active
Version: 4.0.0-SPECIALIZED
Description: Unified manager for Metabolism, Endocrine, Immune, and Sleep systems (AB Soma layer L02).
References: AB_AP_BALANCE_RULES.md (energy/thermal/immune thresholds); DNA blueprint COMPLETE_ARCHITECTURE.md (line 33-47: 11 biological systems); Governance AGENTS.md (Law I/II/III); Provenance: physiology.json / bone_marrow.log / signal_history.json.
Note: State file core/monitoring/physiology.json is simulated/file-based (not real-time hardware sensor); labeled clearly for Law III non-deception compliance (mesh_hive_sync_status.md truth documentation).
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

SLEEP_STAGES = ["awake", "nrem", "deep_nrem", "rem"]
STAGE_DURATIONS = {
    "nrem": 60,
    "deep_nrem": 60,
    "rem": 30
}

class PhysiologyEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "physiology.json"
        self.default_budget = 1000
        self._salience: Optional["SalienceEngine"] = None

    def get_state(self) -> Dict[str, Any]:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            self.reset_all()
            return self.get_state()

    def _write_state(self, state: Dict):
        state["last_sync"] = time.time()
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

    @property
    def salience(self) -> "SalienceEngine":
        if self._salience is None:
            from layers.L09_Observability.salience import SalienceEngine
            self._salience = SalienceEngine(self.base_dir, physiology_engine=self)
        return self._salience

    def reset_all(self):
        state = {
            "metabolism": {
                "max_energy": self.default_budget,
                "current_energy": self.default_budget,
                "status": "Healthy",
                "last_reset": datetime.now().isoformat()
            },
            "endocrine": {
                "vibe": "Stable",
                "hormones": {
                    "dopamine": 50.0,
                    "serotonin": 50.0,
                    "cortisol": 10.0,
                    "adrenaline": 0.0
                }
            },
            "immune": {
                "temperature": 98.6,
                "threat_level": "Negligible",
                "anomalies": []
            },
            "resource_saturation": {
                "status": "Optimal",
                "last_exhaustion": 0.0,
                "hibernation_active": False,
                "connection_priority": "Priority Lane (Requested)"
            },
            "sleep": {
                "state": "awake",
                "last_activity": time.time(),
                "sleep_cycles": 0,
                "total_sleep_time": 0.0,
                "cortisol_before_sleep": 0.0
            },
            "last_sync": time.time()
        }
        self._write_state(state)

    def inject_hormone(self, hormone_name: str, delta: float):
        state = self.get_state()
        if hormone_name not in state["endocrine"]["hormones"]:
            state["endocrine"]["hormones"][hormone_name] = 0.0
        state["endocrine"]["hormones"][hormone_name] = max(0.0, min(100.0, state["endocrine"]["hormones"][hormone_name] + delta))
        self._write_state(state)

    def consume_energy(self, amount: int) -> Dict[str, Any]:
        state = self.get_state()
        met = state["metabolism"]
        met["current_energy"] = max(0, met["current_energy"] - amount)
        met["status"] = "Critical" if met["current_energy"] <= 100 else "Low" if met["current_energy"] <= 250 else "Conserving" if met["current_energy"] <= 500 else "Healthy"
        self._write_state(state)
        return {"status": met["status"], "energy": met["current_energy"]}

    def _scan_host_skin(self):
        """Neural 13.0: Scans Host OS vitals and maps them to biosignals."""
        try:
            from layers.L07_Integration.integration_bridge import IntegrationBridge
            bridge = IntegrationBridge(self.base_dir)
            vitals = bridge.scan_host_vitals()
            
            # Map physical pressure to physiological state
            if vitals.get("disk_pressure", 0) > 90:
                self.record_anomaly("ISCHEMIA", "CRITICAL")
            if vitals.get("cpu_load", 0) > 85:
                self.record_anomaly("HYPOXIA", "HIGH")
                self.inject_hormone("cortisol", 5.0) # Stress from CPU load
                
        except Exception:
            pass

    def synthesize_vibe(self):
        self._scan_host_skin()
        state = self.get_state()
        energy  = state["metabolism"]["current_energy"]
        hormones = state["endocrine"]["hormones"]
        immune_temp = state["immune"]["temperature"]

        if energy < 100 or hormones["cortisol"] > 80 or immune_temp > 103:
            vibe = "Feverish"
        elif energy < 250 or hormones["cortisol"] > 40:
            vibe = "Stressed"
        elif energy > 800 and hormones["serotonin"] > 60 and hormones["cortisol"] < 30:
            vibe = "Flow State"
        elif energy > 600 and hormones["dopamine"] > 50:
            vibe = "Excited"
        elif energy > 400:
            vibe = "Stable"
        else:
            vibe = "Tired"

        state["endocrine"]["vibe"] = vibe
        self._write_state(state)
        return vibe

    def record_anomaly(self, anomaly_type: str, severity: str):
        state = self.get_state()
        imm = state["immune"]
        imm["anomalies"].append({"type": anomaly_type, "severity": severity, "timestamp": time.time()})
        if len(imm["anomalies"]) > 20:
            imm["anomalies"] = imm["anomalies"][-20:]
        self._write_state(state)

    def record_activity(self):
        state = self.get_state()
        state["sleep"]["last_activity"] = time.time()
        if state["sleep"]["state"] != "awake":
            self._wake_up(state)
        self._write_state(state)

    def inject_temp(self, delta: float):
        state = self.get_state()
        state["immune"]["temperature"] = max(95.0, min(110.0, state["immune"]["temperature"] + delta))
        self._write_state(state)

    def heal(self, amount: float = 0.5):
        state = self.get_state()
        imm = state["immune"]
        imm["temperature"] = max(98.6, imm["temperature"] - amount)
        t = imm["temperature"]
        if t >= 104.0: imm["threat_level"] = "Sepsis"
        elif t >= 102.0: imm["threat_level"] = "Fever"
        elif t >= 100.0: imm["threat_level"] = "Inflammation"
        else: imm["threat_level"] = "Negligible"
        self._write_state(state)

    def _wake_up(self, state: Dict):
        sleep_data = state["sleep"]
        if sleep_data["state"] != "awake":
            sleep_data["state"] = "awake"
            met = state["metabolism"]
            met["current_energy"] = min(met["max_energy"], met["current_energy"] + int(met["max_energy"] * 0.15))

    def check_idle_and_sleep(self, idle_threshold_seconds: int = 300) -> bool:
        state = self.get_state()
        idle_time = time.time() - state["sleep"]["last_activity"]
        if idle_time >= idle_threshold_seconds and state["sleep"]["state"] == "awake":
            return self._enter_sleep(state)
        return False

    def _enter_sleep(self, state: Dict) -> bool:
        sleep_data = state["sleep"]
        sleep_data["state"] = "nrem"
        sleep_data["cortisol_before_sleep"] = state["endocrine"]["hormones"]["cortisol"]
        sleep_data["sleep_cycles"] += 1
        self._write_state(state)
        return True

    def sleep_tick(self):
        state = self.get_state()
        sleep_data = state["sleep"]
        if sleep_data["state"] == "awake":
            return
        stages = ["nrem", "deep_nrem", "rem"]
        current_idx = stages.index(sleep_data["state"]) if sleep_data["state"] in stages else 0
        next_idx = (current_idx + 1) % len(stages)
        sleep_data["state"] = stages[next_idx]

        if sleep_data["state"] == "deep_nrem":
            met = state["metabolism"]
            met["current_energy"] = min(met["max_energy"], met["current_energy"] + int(met["max_energy"] * 0.05))
            state["immune"]["temperature"] = max(98.6, state["immune"]["temperature"] - 0.1)
        elif sleep_data["state"] == "rem":
            h = state["endocrine"]["hormones"]
            h["cortisol"] = max(0.0, h["cortisol"] - 5.0)
            sleep_data["total_sleep_time"] += 1.0

        self._write_state(state)
        return sleep_data["state"]

    def get_sleep_state(self) -> Dict:
        state = self.get_state()
        return state["sleep"]

    def force_wake(self):
        state = self.get_state()
        if state["sleep"]["state"] != "awake":
            self._wake_up(state)
            self._write_state(state)

    def run_full_sleep_cycle(self) -> Dict[str, Any]:
        """Runs a complete 3-stage sleep cycle (NREM, DEEP, REM) to restore energy."""
        state = self.get_state()
        if state["sleep"]["state"] == "awake":
            self._enter_sleep(state)
        
        # 1. NREM
        self.sleep_tick()
        # 2. Deep NREM (Energy +5%)
        self.sleep_tick()
        # 3. REM (Cortisol -5, +1h sleep time)
        self.sleep_tick()
        
        # Wake up
        self._wake_up(self.get_state())
        
        # Recalculate vibe
        vibe = self.synthesize_vibe()
        
        final_state = self.get_state()
        return {
            "energy_gain": final_state["metabolism"]["current_energy"] - state["metabolism"]["current_energy"],
            "new_energy": final_state["metabolism"]["current_energy"],
            "vibe": vibe,
            "cycles": final_state["sleep"]["sleep_cycles"]
        }

    def inject_stimulant(self, type: str = "caffeine") -> Dict[str, Any]:
        """Injects a stimulant to bypass tiredness and boost ATP."""
        state = self.get_state()
        if type == "caffeine":
            # Boost energy temporarily, increase heat and cortisol
            state["metabolism"]["current_energy"] = min(state["metabolism"]["max_energy"], state["metabolism"]["current_energy"] + 150)
            self.inject_hormone("cortisol", 15.0)
            self.inject_hormone("adrenaline", 20.0)
            state["immune"]["temperature"] += 0.5
            state["sleep"]["last_activity"] = time.time()
            if state["sleep"]["state"] != "awake":
                self._wake_up(state)
        self._write_state(state)
        return {"type": type, "energy": state["metabolism"]["current_energy"], "vibe": self.synthesize_vibe()}

    def trigger_hibernation(self, error_code: int) -> bool:
        """Neural 13.0: Enters Hibernation Mode due to cloud resource exhaustion."""
        state = self.get_state()
        if "resource_saturation" not in state:
            state["resource_saturation"] = {"status": "Optimal", "last_exhaustion": 0.0, "hibernation_active": False}
            
        if error_code in [429, 503]:
            state["resource_saturation"]["status"] = "Exhausted"
            state["resource_saturation"]["last_exhaustion"] = time.time()
            state["resource_saturation"]["hibernation_active"] = True
            self.record_anomaly("RESOURCE_EXHAUSTION", "CRITICAL")
            self._write_state(state)
            return True
        return False

    def check_hibernation_status(self) -> bool:
        """Checks if the system should still be in hibernation (5 min TTL)."""
        state = self.get_state()
        sat = state.get("resource_saturation", {})
        if sat.get("hibernation_active"):
            if time.time() - sat.get("last_exhaustion", 0) > 300: # 5 mins
                sat["hibernation_active"] = False
                sat["status"] = "Optimal"
                self._write_state(state)
                return False
            return True
        return False

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = PhysiologyEngine(base)
    print("Vibe:", engine.synthesize_vibe())
    print("Energy Status:", engine.consume_energy(0))

