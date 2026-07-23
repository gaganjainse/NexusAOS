"""Speech and canvas tool registry subset for mcp_server/python/index.py.

This module owns the MCP tools that render or transmit agent voice/text output,
including neural thought translation, sovereign briefing, and Neural Canvas writes.
"""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_server.python.hive_sync import HiveSync

hive_sync = HiveSync()

mcp = FastMCP("NexusAOS speech tools")

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
    from layers.L08_Governance.rbac_engine import RBACEngine
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    rbac = RBACEngine(base_dir)
    return rbac.check_permission("Sovereign", action)


@mcp.tool()
def get_neural_thought(pulse: str) -> str:
    """Translates a high-density NEURAL pulse into a readable explanation for the Sovereign."""
    from pathlib import Path
    from layers.L10_Intelligence.thought_agent import ThoughtAgent
    base_dir = Path(__file__).resolve().parents[3]
    thought_agent = ThoughtAgent(base_dir)
    thought = thought_agent.explain_pulse(pulse)
    return _response("success", payload={"thought": thought}, tool_id="get_neural_thought")


@mcp.tool()
def push_sovereign_briefing(title: str, content: str, salience: str = "MEDIUM") -> str:
    """Manually pushes a high-salience update to the Sovereign Wisdom Feed."""
    allowed, msg = _gate("push_sovereign_briefing")
    if not allowed:
        return _response("blocked", message=msg, tool_id="push_sovereign_briefing")
    start = __import__("time").perf_counter()
    from pathlib import Path
    from layers.L09_Observability.wisdom_feed import WisdomFeed
    base_dir = Path(__file__).resolve().parents[3]
    wisdom_feed = WisdomFeed(base_dir)
    res = wisdom_feed.push_briefing(title, content, salience)
    duration = __import__("time").perf_counter() - start
    return _response("success", message=res, tool_id="push_sovereign_briefing", duration=duration)


@mcp.tool()
def write_canvas_node(node_id: str, content: str, agent_id: str, zone: str = "Nervous") -> str:
    """Writes to the sharded Neural Canvas using CRDT logic."""
    allowed, msg = _gate("write_canvas_node")
    if not allowed:
        return _response("blocked", message=msg, tool_id="write_canvas_node")
    start = __import__("time").perf_counter()
    from pathlib import Path
    from layers.L12_Infrastructure.neural_canvas import NeuralCanvas
    base_dir = Path(__file__).resolve().parents[3]
    canvas = NeuralCanvas(base_dir)
    res = canvas.write_node(node_id, content, agent_id, organ_zone=zone)
    duration = __import__("time").perf_counter() - start
    return _response("success" if res["success"] else "collision", payload=res, tool_id="write_canvas_node", duration=duration)
