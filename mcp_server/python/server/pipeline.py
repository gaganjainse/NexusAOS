# SeshaAOS Tool Execution Pipeline
# Version: 0.1.0
# Description: Unified execution path for tool calls.

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any, Callable, Awaitable, TypeVar

from .context import ServerContext

T = TypeVar("T")
Handler = Callable[[], Any]


@dataclass
class ToolCallContext:
    tool_id: str
    action: str
    agent_id: str = "Sovereign"
    duration: float = 0.0


class ToolExecutionPipeline:
    def __init__(self, ctx: ServerContext):
        self.ctx = ctx
        self.enabled = True

    def run(self, *, tool_id: str, action: str, handler: Handler, agent_id: str = "Sovereign", args: Optional[Dict[str, Any]] = None) -> str:
        start = time.perf_counter()
        result = self._execute(handler)
        duration = time.perf_counter() - start
        return result

    async def run_async(self, *, tool_id: str, action: str, handler: Callable[[], Awaitable[Any]], agent_id: str = "Sovereign", args: Optional[Dict[str, Any]] = None) -> str:
        start = time.perf_counter()
        result = await self._execute_async(handler)
        duration = time.perf_counter() - start
        return result

    def _execute(self, handler: Handler) -> str:
        return handler()

    async def _execute_async(self, handler: Callable[[], Awaitable[Any]]) -> str:
        return await handler()

