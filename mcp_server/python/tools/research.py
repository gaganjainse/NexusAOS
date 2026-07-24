"""Research tool registry subset for mcp_server/python/index.py.

This module owns the MCP tools that gather external knowledge: web search,
medicinal fix lookup, and architectural nutrient ingestion.
"""

from __future__ import annotations

import json
from mcp.server.fastmcp import FastMCP
from mcp_server.python.hive_sync import HiveSync
from typing import Any

hive_sync = HiveSync()
mcp = FastMCP("SeshaAOS research tools")


def _response(status: str, payload: Any = None, message: str = "", tool_id: str = "unknown", duration: float = 0.0) -> str:
    result = json.dumps({
        "status": status,
        "payload": payload,
        "message": message,
        "timestamp": __import__("time").time(),
    }, indent=2)
    try:
        hive_sync.after_tool(tool_id, status == "success", duration)
    except Exception:
        pass
    return result


def _gate(action: str):
    from pathlib import Path
    from layers.L08_Governance.rbac_engine import RBACEngine
    base_dir = Path(__file__).resolve().parents[3]
    rbac = RBACEngine(base_dir)
    return rbac.check_permission("Sovereign", action)


def _services(base_dir):
    from layers.L06_Tool.web_receptor import WebReceptor
    from layers.L06_Tool.deep_research_tool import DeepResearchTool
    from layers.L12_Infrastructure.Sesha_lattice import LatticeEngine
    return {
        "web_receptor": WebReceptor(base_dir),
        "deep_research": DeepResearchTool(base_dir),
        "lattice": LatticeEngine(base_dir),
    }


@mcp.tool()
def seek_medicine(ailment: str) -> str:
    """Uses external stimuli (the web) to find a cure/fix for a system illness or error."""
    allowed, msg = _gate("seek_medicine")
    if not allowed:
        return _response("blocked", message=msg, tool_id="seek_medicine")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    web = services["web_receptor"]
    search_res = web.search(f"Fix for {ailment} programming error")
    from layers.L02_Agent.antigen_registry import AntigenRegistry
    antigens = AntigenRegistry(base_dir)
    antigens.register_antigen("MEDICINAL_FIX", ailment, f"External solution found: {search_res[:100]}...")
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={"cure_found": True, "details": search_res}, message=f"Medicine ingested for {ailment}.", tool_id="seek_medicine", duration=duration)


@mcp.tool()
def ingest_architectural_nutrients(topic: str) -> str:
    """Performs deep research on a topic and ingests best practices into the DNA."""
    allowed, msg = _gate("ingest_architectural_nutrients")
    if not allowed:
        return _response("blocked", message=msg, tool_id="ingest_architectural_nutrients")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["deep_research"].perform_deep_research(topic)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message=f"Research on {topic} ingested.", tool_id="ingest_architectural_nutrients", duration=duration)

