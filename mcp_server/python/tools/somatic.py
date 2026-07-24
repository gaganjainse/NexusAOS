"""Somatic tool registry: host-facing motor, retina, and desktop sensing tools."""

from __future__ import annotations

import json
from mcp.server.fastmcp import FastMCP
from typing import Any


def register(mcp: FastMCP, services: dict[str, Any]) -> None:
    hive_sync = services.get("hive_sync")

    def _response(status: str, payload: Any = None, message: str = "", tool_id: str = "unknown", duration: float = 0.0) -> str:
        result = json.dumps({
            "status": status,
            "payload": payload,
            "message": message,
            "timestamp": __import__("time").time(),
        }, indent=2)
        if hive_sync:
            try:
                hive_sync.after_tool(tool_id, status == "success", duration)
            except Exception:
                pass
        return result

    async def _gate(action: str):
        rbac = services.get("rbac")
        if rbac is None:
            return True, "Authorized"
        return rbac.check_permission("Sovereign", action)

    @mcp.tool()
    async def trigger_optical_burst(signal_type: str, packet_count: int = 10) -> str:
        """Fires a high-frequency optical burst through the photonic synaptic bus."""
        allowed, msg = await _gate("trigger_optical_burst")
        if not allowed:
            return _response("blocked", message=msg, tool_id="trigger_optical_burst")
        start = __import__("time").perf_counter()
        optics = services["optics"]
        latency = await optics.emit_optical_burst(signal_type, packet_count)
        duration = __import__("time").perf_counter() - start
        return _response("success", payload={"avg_latency_us": latency}, message=f"Optical burst fired for {signal_type}.", tool_id="trigger_optical_burst", duration=duration)

    @mcp.tool()
    def capture_host_retina(left: int = 0, top: int = 0, right: int = 1920, bottom: int = 1080) -> str:
        """Captures a screenshot of the host PC."""
        import asyncio
        allowed, msg = asyncio.run(_gate("capture_host_retina"))
        if not allowed:
            return _response("blocked", message=msg, tool_id="capture_host_retina")
        start = __import__("time").perf_counter()
        vision = services["vision"]
        path = vision.capture_screen(region=(left, top, right, bottom))
        duration = __import__("time").perf_counter() - start
        return _response("success", payload={"path": path}, message="Retina capture successful.", tool_id="capture_host_retina", duration=duration)

    @mcp.tool()
    def send_somatic_input(keys: str) -> str:
        """Sends keyboard input to the host PC."""
        import asyncio
        allowed, msg = asyncio.run(_gate("send_somatic_input"))
        if not allowed:
            return _response("blocked", message=msg, tool_id="send_somatic_input")
        start = __import__("time").perf_counter()
        motor = services["motor"]
        res = motor.send_input(keys)
        duration = __import__("time").perf_counter() - start
        return _response("success", message=res, tool_id="send_somatic_input", duration=duration)

    @mcp.tool()
    def focus_host_window(window_name: str) -> str:
        """Switches focus to a specific window on the PC."""
        import asyncio
        allowed, msg = asyncio.run(_gate("focus_host_window"))
        if not allowed:
            return _response("blocked", message=msg, tool_id="focus_host_window")
        start = __import__("time").perf_counter()
        motor = services["motor"]
        res = motor.focus_window(window_name)
        duration = __import__("time").perf_counter() - start
        return _response("success", message=res, tool_id="focus_host_window", duration=duration)

    @mcp.tool()
    def inject_win32_pulse(window_name: str, message_type: str, w_param: int = 0, l_param: int = 0) -> str:
        """Direct Win32 Message Injection."""
        import asyncio
        allowed, msg = asyncio.run(_gate("inject_win32_pulse"))
        if not allowed:
            return _response("blocked", message=msg, tool_id="inject_win32_pulse")
        start = __import__("time").perf_counter()
        motor = services["motor"]
        res = motor.inject_message(window_name, message_type, w_param, l_param)
        duration = __import__("time").perf_counter() - start
        return _response("success", message=res, tool_id="inject_win32_pulse", duration=duration)

    @mcp.tool()
    def scan_semantic_desktop() -> str:
        """UIA Scan: Reads the internal structure of the desktop."""
        import asyncio
        allowed, msg = asyncio.run(_gate("scan_semantic_desktop"))
        if not allowed:
            return _response("blocked", message=msg, tool_id="scan_semantic_desktop")
        start = __import__("time").perf_counter()
        sentry = services["uia_sentry"]
        res = sentry.scan_ui_elements()
        duration = __import__("time").perf_counter() - start
        return _response("success", payload=res, message="Semantic UI scan complete.", tool_id="scan_semantic_desktop", duration=duration)
