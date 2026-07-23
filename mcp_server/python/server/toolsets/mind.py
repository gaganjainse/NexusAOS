"""Mind domain registrar."""


def register_mind_tools(mcp, ctx, pipeline):
    from server.response import AOSResponse
    response = AOSResponse()

    @mcp.tool()
    def queue_directive(text: str, priority: int = 5) -> str:
        action = "queue_directive"
        return pipeline.run(
            tool_id=action,
            action=action,
            handler=lambda: response.build(status="success", payload={"text": text, "priority": priority}, message="Directive queued."),
        )
