"""AOS Browser Plugin — web perception and intelligence gathering."""

from pathlib import Path


class BrowserPlugin:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.name = "AOS Browser"
        self.id = "browser"

    def get_mcp_tools(self):
        return ["collect_intelligence", "browse_url"]
