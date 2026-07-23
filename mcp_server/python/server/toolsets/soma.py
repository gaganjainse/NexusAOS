"""Soma domain registrar."""


def register_soma_tools(mcp, ctx, pipeline):
    from layers.L02_Agent.sleep_engine import SleepEngine
    from server.response import AOSResponse
    response = AOSResponse()
    sleep_engine = SleepEngine(ctx.base_dir)

    @mcp.tool()
    def trigger_sleep_cycle() -> str:
        action = "trigger_sleep_cycle"
        return pipeline.run(
            tool_id=action,
            action=action,
            handler=lambda: response.build(status="success", payload={}, message="Sleep cycle simulated."),
        )
