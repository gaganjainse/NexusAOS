"""
Nexus Corporate OS - GUI Stub
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE / "mcp_server" / "python"))

if __name__ == "__main__":
    print("Nexus GUI stub: full CustomTkinter implementation pending.")
