"""
SeshaAOS - RBAC Engine
Version: 1.0.0
Description: Enforces Role-Based Access Control for tool execution.
Biological analog: Hormonal gating and blood-brain barrier permissions.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class RBACEngine:
    # Default Permissions Map: tool_id -> set of roles allowed
    DEFAULT_PERMISSIONS = {
        "diagnose_os": {"Admin", "Orchestrator", "Security"},
        "trigger_self_healing": {"Admin", "Immune", "Security"},
        "assimilate_external_tool": {"Admin"},
        "install_organ": {"Admin"},
        "execute_motor_command": {"Admin", "Motor", "Orchestrator"},
        "execute_motor_write": {"Admin", "Motor"},
        "collect_intelligence": {"Admin", "Researcher", "Orchestrator"},
        "broadcast_directive": {"Admin", "Orchestrator"},
        "trigger_quorum_vote": {"Admin", "Orchestrator"},
        "propose_dna_mutation": {"Admin", "CKO"},
        "authorize_federation_peer": {"Admin"},
        "export_wisdom_spore": {"Admin", "CKO"}
    }

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.config_path = base_dir / "core" / "monitoring" / "rbac_config.json"
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            # Serialize sets as lists for JSON
            config = {
                "roles": {
                    "Admin": ["root", "Sovereign"],
                    "Orchestrator": ["local_orch"],
                    "Researcher": ["research_agent"],
                    "Motor": ["motor_agent"],
                    "Immune": ["immune_agent"],
                    "Security": ["security_guard"]
                },
                "permissions": {k: list(v) for k, v in self.DEFAULT_PERMISSIONS.items()}
            }
            self.config_path.write_text(json.dumps(config, indent=4), encoding="utf-8")

    def check_permission(self, agent_id: str, tool_id: str) -> tuple[bool, str]:
        """Verifies if an agent has permission to use a specific tool."""
        try:
            config = json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception as e:
            return False, f"RBAC Error: Config unreadable: {str(e)}"

        # 1. Identify Agent Roles
        agent_roles = []
        for role, agents in config.get("roles", {}).items():
            if agent_id in agents:
                agent_roles.append(role)
        
        # Default for unknown agents (e.g. basic workers)
        if not agent_roles:
            agent_roles = ["Worker"]

        # 2. Check Tool Permissions
        required_roles = config.get("permissions", {}).get(tool_id)
        
        # If tool is not in map, assume it's open (Public)
        if not required_roles:
            return True, "Success: Public tool access granted."

        # 3. Match
        for role in agent_roles:
            if role in required_roles:
                return True, f"Success: Role '{role}' authorized for '{tool_id}'."
        
        return False, f"Permission Denied: Agent '{agent_id}' lacks required roles for '{tool_id}' (Requires: {required_roles})."

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    rbac = RBACEngine(base)
    allowed, msg = rbac.check_permission("research_agent", "install_organ")
    print(f"Result: {allowed} | {msg}")

