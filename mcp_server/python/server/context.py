# NexusAOS Server Context
# Version: 0.1.0
# Description: Holds shared services and configuration for the MCP server.

import sys
from pathlib import Path
from typing import Any, Dict, Optional

_python_root = Path(__file__).resolve().parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

BASE_DIR = _python_root.parent.parent


class ServiceContainer:
    pass


class ServerContext:
    def __init__(self, base_dir: Path, services: Optional[ServiceContainer] = None):
        self.base_dir = base_dir
        self.services = services or ServiceContainer()
