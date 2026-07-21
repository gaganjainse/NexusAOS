"""
NexusAOS GUI Launcher
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE / "mcp_server" / "python"))

from gui.nexus_gui import NexusAOSGUI

if __name__ == "__main__":
    app = NexusAOSGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
