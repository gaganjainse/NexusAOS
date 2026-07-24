"""SeshaAOS MCP entrypoint.

This thin bootstrap replaces the previous monolithic registry entrypoint.
It assembles shared services and delegates tool registration to domain
registrars under the ``server/toolsets`` package.
"""
from mcp.server.fastmcp import FastMCP

from server.bootstrap import setup
from server.context import ServerContext, ServiceContainer
from server.pipeline import ToolExecutionPipeline
from server.toolsets import TOOLSET_REGISTRARS


def create_server(base_dir=None):
    base_dir = setup(base_dir)
    mcp = FastMCP("SeshaAOS - Golden Master Registry")
    ctx = ServerContext(base_dir=base_dir, services=ServiceContainer())
    pipeline = ToolExecutionPipeline(ctx)
    for registrar in TOOLSET_REGISTRARS:
        registrar(mcp, ctx, pipeline)
    return pipeline, mcp


def main():
    pipeline, mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()

