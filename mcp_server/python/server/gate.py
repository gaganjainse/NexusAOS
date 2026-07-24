"""SeshaAOS authorization and governance gate helpers."""

from typing import Tuple


class ToolGate:
    def check(self, action: str, agent_id: str = "Sovereign") -> Tuple[bool, str]:
        return True, "Authorized placeholder"

