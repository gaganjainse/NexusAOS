"""
Nexus Corporate OS - Immune Engine
Version: 1.0.0
Description: Tracks system "Body Temperature" (Threat Level) based on anomalies and repairs.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

class ImmuneEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.health_path = base_dir / "core" / "monitoring" / "health.json"
        self._ensure_state_exists()

    def _ensure_state_exists(self):
        if not self.health_path.parent.exists():
            self.health_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.health_path.exists():
            initial_state = {
                "temperature": 98.6,
                "threat_level": "Negligible",
                "anomalies": [],
                "last_update": time.time()
            }
            self._write_health(initial_state)

    def register_anomaly(self, anomaly_type: str, severity: float) -> str:
        """Adds an anomaly and raises the system temperature."""
        health = self.get_health()

        anomaly = {
            "timestamp": time.time(),
            "type": anomaly_type,
            "severity": severity
        }
        health["anomalies"].append(anomaly)

        # Increase temperature based on severity
        health["temperature"] = min(106.0, health["temperature"] + severity)
        health["threat_level"] = self._calculate_threat(health["temperature"])
        health["last_update"] = time.time()

        self._write_health(health)
        return f"Anomaly registered: {anomaly_type}. System Temperature: {health['temperature']}°F"

    def heal(self, amount: float = 0.5):
        """Gradually lowers the system temperature over time or after repairs."""
        health = self.get_health()
        health["temperature"] = max(98.6, health["temperature"] - amount)
        health["threat_level"] = self._calculate_threat(health["temperature"])
        health["last_update"] = time.time()
        self._write_health(health)

    def _calculate_threat(self, temp: float) -> str:
        if temp >= 104.0:
            return "Sepsis"
        elif temp >= 102.0:
            return "Fever"
        elif temp >= 100.0:
            return "Inflammation"
        return "Negligible"

    def get_health(self) -> Dict[str, Any]:
        try:
            with open(self.health_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"temperature": 98.6, "threat_level": "Negligible", "anomalies": []}

    def _write_health(self, state: Dict):
        with open(self.health_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = ImmuneEngine(base)
    print(engine.register_anomaly("File Corruption", 2.0))
    print(f"Current Threat: {engine.get_health()['threat_level']}")
