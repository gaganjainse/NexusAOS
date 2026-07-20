"""
AOS Core Plugin — bundles rules, MCP tools, skills, and subagent routes.
Version: 2.0.0
"""

from pathlib import Path
from typing import Dict, Any, List


class AOSPlugin:
    """Base plugin interface matching Cursor IDE extension model."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.name = "AOS Core"
        self.version = "2.0.0"
        self.id = "core"

    def get_mcp_tools(self) -> List[str]:
        return ["boot_nexus_os", "submit_directive", "get_orchestrator_status", "diagnose_os"]

    def get_skills(self) -> List[str]:
        return [".cursor/skills/aos-boot/SKILL.md", ".cursor/skills/aos-orchestrator/SKILL.md"]

    def get_rules(self) -> List[str]:
        return [".cursor/rules/aos-constitution.mdc", ".cursor/rules/aos-physiology.mdc"]

    def get_commands(self) -> List[str]:
        return [".cursor/commands/boot.md", ".cursor/commands/directive.md", ".cursor/commands/status.md"]

    def get_hooks(self) -> List[str]:
        return [".cursor/hooks.json"]

    def get_subagents(self) -> Dict[str, str]:
        return {
            "orchestrator": "Nexus Orchestrator Agent — closed-loop CPU",
            "motor": "Motor Agent — file write and command execution",
            "immune": "Immune Agent — self-healing and fever response",
        }

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "tools": self.get_mcp_tools(),
            "subagents": list(self.get_subagents().keys()),
        }


# Backward compat alias
NexusPlugin = AOSPlugin
