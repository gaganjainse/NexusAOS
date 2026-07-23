"""Host-side domain registrar."""


def register_host_tools(mcp, ctx, pipeline):
    from server.response import AOSResponse
    response = AOSResponse()

    @mcp.tool()
    def scan_semantic_desktop() -> str:
        action = "scan_semantic_desktop"
        return pipeline.run(
            tool_id=action,
            action=action,
            handler=lambda: response.build(status="success", payload={}, message="Semantic desktop scan simulated."),
        )
