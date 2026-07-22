"""
AOS Cellular Engine — maps biological cell components to AOS runtime units.
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root


# Biological component -> AOS runtime mapping
CELLULAR_MAP = {
    "nucleus": {
        "biology": "Contains DNA, controls cell function",
        "aos": "archives/dna_core/foundation/ + constitution",
        "engine": "mutation_engine.py",
        "status_field": "dna_integrity",
    },
    "mitochondria": {
        "biology": "ATP production, energy metabolism",
        "aos": "physiology.json metabolism",
        "engine": "physiology_engine.py",
        "status_field": "energy_pct",
    },
    "cell_membrane": {
        "biology": "Boundary, selective permeability",
        "aos": "physiological_gate.py + motor path guards",
        "engine": "physiological_gate.py",
        "status_field": "gate_active",
    },
    "ribosome": {
        "biology": "Protein synthesis from mRNA",
        "aos": "nxp_forge.py — DNA to pulse firmware",
        "engine": "nxp_forge.py",
        "status_field": "pulse_count",
    },
    "golgi_apparatus": {
        "biology": "Package and ship proteins",
        "aos": "signal_router.py — hormonal packaging",
        "engine": "signal_router.py",
        "status_field": "active_signals",
    },
    "lysosome": {
        "biology": "Digest waste and damaged organelles",
        "aos": "nexus_liver.py — filtration",
        "engine": "nexus_liver.py",
        "status_field": "toxicity_pct",
    },
    "neuron": {
        "biology": "Electrical signal transmission",
        "aos": "nexus_lattice.py — synaptic handoffs",
        "engine": "nexus_lattice.py",
        "status_field": "active_synapses",
    },
    "blood": {
        "biology": "Transport medium (O2, hormones, cells)",
        "aos": "signals.json + physiology.json circulation",
        "engine": "signal_router.py + nexus_pulse.py",
        "status_field": "circulation_active",
    },
    "rbc": {
        "biology": "Oxygen transport",
        "aos": "Energy/token delivery to agents",
        "engine": "physiology_engine.consume_energy",
        "status_field": "rbc_health",
    },
    "wbc": {
        "biology": "Immune patrol and pathogen destruction",
        "aos": "antibody_engine.patrol()",
        "engine": "antibody_engine.py",
        "status_field": "wbc_count",
    },
    "platelet": {
        "biology": "Clotting, wound repair",
        "aos": "auto_repair + lattice stale task pruning",
        "engine": "auto_repair.py",
        "status_field": "platelet_clotting",
    },
    "antibody": {
        "biology": "Specific pathogen neutralization",
        "aos": "antibody_engine corrective templates",
        "engine": "antibody_engine.py",
        "status_field": "active_antibodies",
    },
}


class CellularEngine:
    """Reports health of all mapped cellular components."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _measure(self, component: str, mapping: Dict) -> Dict[str, Any]:
        result = {"component": component, "aos_path": mapping["aos"], "engine": mapping["engine"]}
        try:
            if component == "mitochondria":
                from layers.L02_Agent.physiology_engine import PhysiologyEngine
                s = PhysiologyEngine(self.base_dir).get_state()["metabolism"]
                pct = (s["current_energy"] / s["max_energy"]) * 100
                result["value"] = round(pct, 1)
                result["healthy"] = pct > 20
            elif component == "nucleus":
                const = self.base_dir / "archives/dna_core/foundation/nexus_constitution.md"
                result["value"] = const.exists()
                result["healthy"] = const.exists()
            elif component == "neuron":
                from layers.L12_Infrastructure.nexus_lattice import LatticeEngine
                result["value"] = len(LatticeEngine(self.base_dir).get_active_nodes())
                result["healthy"] = True
            elif component == "lysosome":
                from layers.L02_Agent.nexus_liver import NexusLiver
                t = NexusLiver(self.base_dir).get_toxic_load()
                result["value"] = t["toxicity_pct"]
                result["healthy"] = t["toxicity_pct"] < 75
            elif component == "wbc":
                from layers.L02_Agent.antibody_engine import AntibodyEngine
                s = AntibodyEngine(self.base_dir).get_immune_cells_status()
                result["value"] = s["wbc_count"]
                result["healthy"] = s["threat_level"] == "Negligible"
            elif component == "rbc":
                from layers.L02_Agent.antibody_engine import AntibodyEngine
                s = AntibodyEngine(self.base_dir).get_immune_cells_status()
                result["value"] = s["rbc_health_pct"]
                result["healthy"] = s["rbc_health_pct"] > 50
            elif component == "platelet":
                from layers.L02_Agent.antibody_engine import AntibodyEngine
                s = AntibodyEngine(self.base_dir).get_immune_cells_status()
                result["value"] = s["platelet_clotting"]
                result["healthy"] = s["platelet_clotting"] < 5
            elif component == "antibody":
                from layers.L02_Agent.antibody_engine import AntibodyEngine
                s = AntibodyEngine(self.base_dir).get_immune_cells_status()
                result["value"] = s["active_antibodies"]
                result["healthy"] = s["active_antibodies"] == 0
            elif component == "blood":
                from layers.L11_Data.signal_router import SignalRouter
                result["value"] = len(SignalRouter(self.base_dir).get_active_signals())
                result["healthy"] = True
            elif component == "ribosome":
                pulses = list((self.base_dir / "core/pulses").glob("*.nxp"))
                result["value"] = len(pulses)
                result["healthy"] = len(pulses) >= 5
            elif component == "cell_membrane":
                from layers.L08_Governance.physiological_gate import PhysiologicalGate
                r = PhysiologicalGate(self.base_dir).get_dampening_report()
                blocked = sum(1 for t in r["tools"].values() if not t["allowed"])
                result["value"] = blocked
                result["healthy"] = blocked < 5
            else:
                result["value"] = "mapped"
                result["healthy"] = True
        except Exception as e:
            result["value"] = f"error: {e}"
            result["healthy"] = False
        return result

    def full_cell_report(self) -> Dict[str, Any]:
        cells = {}
        healthy = 0
        for name, mapping in CELLULAR_MAP.items():
            m = self._measure(name, mapping)
            cells[name] = m
            if m.get("healthy"):
                healthy += 1
        return {
            "total_components": len(CELLULAR_MAP),
            "healthy_components": healthy,
            "health_pct": round(healthy / len(CELLULAR_MAP) * 100, 1),
            "cells": cells,
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    print(json.dumps(CellularEngine(base).full_cell_report(), indent=2))
