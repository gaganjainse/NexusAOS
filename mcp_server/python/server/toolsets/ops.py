"""Operations domain registrar."""


def register_ops_tools(mcp, ctx, pipeline):
    from server.response import AOSResponse
    response = AOSResponse()

    @mcp.tool()
    def get_memory_map() -> str:
        action = "get_memory_map"
        return pipeline.run(
            tool_id=action,
            action=action,
            handler=lambda: response.build(status="success", payload={}, message="Memory map retrieved."),
        )
