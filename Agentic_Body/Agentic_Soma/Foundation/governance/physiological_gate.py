# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - Physiological Gate
Version: 1.0.0
Description: Hard-wires hormonal levels to tool permissions (Biological Compulsion).
"""

import sys
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

from typing import Dict, Any, Tuple

from layers.L02_Agent.physiology_engine import PhysiologyEngine


class PhysiologicalGate:
    """Enforces physiological constraints on high-risk operations."""

    TOOL_CONSTRAINTS = {
        "propose_dna_mutation": {
            "max_cortisol": 90.0,
            "min_energy_pct": 20.0,
            "max_threat": "Inflammation",
            "blocked_message": "Mutation blocked: Cortisol too high or immune inflammation active.",
        },
        "spawn_child_instance": {
            "max_cortisol": 70.0,
            "min_energy_pct": 50.0,
            "max_threat": "Fever",
            "blocked_message": "Replication blocked: System stressed or energy insufficient.",
        },
        "generate_spore_export": {
            "min_energy_pct": 30.0,
            "max_threat": "Fever",
            "blocked_message": "Spore export blocked: Energy low or fever active.",
        },
        "trigger_self_healing": {
            "max_cortisol": 95.0,
            "blocked_message": "Self-healing blocked: Extreme cortisol — system in panic lockdown.",
        },
        "dispatch_task": {
            "max_cortisol": 85.0,
            "min_energy_pct": 10.0,
            "max_threat": "Sepsis",
            "blocked_message": "Task dispatch blocked: System in emergency state.",
        },
        "collect_intelligence": {
            "min_energy_pct": 25.0,
            "max_threat": "Fever",
            "blocked_message": "Intelligence collection blocked: Low energy or fever.",
        },
        "trigger_memory_consolidation": {
            "min_energy_pct": 15.0,
            "max_cortisol": 80.0,
            "blocked_message": "Dream cycle blocked: Energy too low or stress too high.",
        },
        "execute_motor_command": {
            "max_cortisol": 90.0,
            "min_energy_pct": 10.0,
            "max_threat": "Sepsis",
            "blocked_message": "Motor command blocked: Physiological emergency.",
        },
        "spawn_parallel_subagent": {
            "max_cortisol": 75.0,
            "min_energy_pct": 30.0,
            "max_threat": "Fever",
            "blocked_message": "Subagent spawn blocked: System stressed.",
        },
        "browse_page": {
            "min_energy_pct": 25.0,
            "max_threat": "Fever",
            "blocked_message": "Browsing blocked: low energy or fever active.",
        },
        "fetch_url": {
            "min_energy_pct": 10.0,
            "max_threat": "Sepsis",
            "blocked_message": "Fetch blocked: critical energy or sepsis.",
        },
        "search_web": {
            "min_energy_pct": 25.0,
            "max_threat": "Fever",
            "blocked_message": "Search blocked: low energy or fever active.",
        },
        "store_entity": {
            "min_energy_pct": 15.0,
            "blocked_message": "Storage blocked: low energy.",
        },
        "gh_create_issue": {
            "min_energy_pct": 25.0,
            "max_threat": "Fever",
            "blocked_message": "GitHub issue creation blocked: low energy or fever active.",
        },
        "geo_lookup": {
            "min_energy_pct": 10.0,
            "blocked_message": "Geocoding blocked: low energy.",
        },
        "query_db": {
            "min_energy_pct": 15.0,
            "blocked_message": "Database query blocked: low energy.",
        },
        "slack_send": {
            "min_energy_pct": 20.0,
            "max_threat": "Fever",
            "blocked_message": "Slack message blocked: low energy or fever active.",
        },
        "pull_sentry_errors": {
            "min_energy_pct": 15.0,
            "blocked_message": "Sentry error pull blocked: low energy.",
        },
        "trigger_sleep": {
            "min_energy_pct": 10.0,
            "blocked_message": "Sleep initiation blocked: critically low energy.",
        },
        "force_wake": {
            "min_energy_pct": 5.0,
            "blocked_message": "Force wake blocked: energy critically low.",
        },
        "get_sleep_state": {
            "min_energy_pct": 0.0,
            "blocked_message": "Sleep state query blocked.",
        },
    }

    THREAT_RANK = {
        "Negligible": 0,
        "Inflammation": 1,
        "Fever": 2,
        "Sepsis": 3,
    }

    def __init__(self, base_dir: Path):
        self.engine = PhysiologyEngine(base_dir)

    def _energy_pct(self, state: Dict[str, Any]) -> float:
        met = state["metabolism"]
        return (met["current_energy"] / met["max_energy"]) * 100

    def _threat_exceeds(self, current: str, max_allowed: str) -> bool:
        return self.THREAT_RANK.get(current, 0) > self.THREAT_RANK.get(max_allowed, 0)

    def check(self, tool_name: str) -> Tuple[bool, str]:
        """
        Returns (allowed, message).
        If allowed is False, the tool must not execute.
        """
        constraints = self.TOOL_CONSTRAINTS.get(tool_name)
        if not constraints:
            return True, "No physiological constraints."

        state = self.engine.get_state()
        hormones = state["endocrine"]["hormones"]
        immune = state["immune"]
        energy_pct = self._energy_pct(state)

        if "max_cortisol" in constraints and hormones["cortisol"] > constraints["max_cortisol"]:
            return False, (
                f"{constraints['blocked_message']} "
                f"(Cortisol: {hormones['cortisol']:.1f}% > {constraints['max_cortisol']}%)"
            )

        if "min_energy_pct" in constraints and energy_pct < constraints["min_energy_pct"]:
            return False, (
                f"{constraints['blocked_message']} "
                f"(Energy: {energy_pct:.1f}% < {constraints['min_energy_pct']}%)"
            )

        if "max_threat" in constraints and self._threat_exceeds(immune["threat_level"], constraints["max_threat"]):
            return False, (
                f"{constraints['blocked_message']} "
                f"(Threat: {immune['threat_level']} exceeds {constraints['max_threat']})"
            )

        return True, "Physiological clearance granted."

    def get_dampening_report(self) -> Dict[str, Any]:
        """Returns current dampening state for all gated tools."""
        state = self.engine.get_state()
        hormones = state["endocrine"]["hormones"]
        immune = state["immune"]
        energy_pct = self._energy_pct(state)

        report = {
            "cortisol": hormones["cortisol"],
            "energy_pct": round(energy_pct, 1),
            "threat_level": immune["threat_level"],
            "vibe": state["endocrine"]["vibe"],
            "tools": {},
        }

        for tool_name, constraints in self.TOOL_CONSTRAINTS.items():
            allowed, msg = self.check(tool_name)
            report["tools"][tool_name] = {"allowed": allowed, "reason": msg}

        return report

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    gate = PhysiologicalGate(base)
    import json
    print(json.dumps(gate.get_dampening_report(), indent=2))

