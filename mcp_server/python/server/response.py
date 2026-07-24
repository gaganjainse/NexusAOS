"""SeshaAOS response formatter."""

import json
import time
from typing import Any, Optional


class AOSResponse:
    def build(self, *, status: str, payload: Any = None, message: str = "", tool_id: str = "unknown") -> str:
        result = {
            "status": status,
            "payload": payload,
            "message": message,
            "timestamp": time.time(),
        }
        return json.dumps(result, indent=2)

