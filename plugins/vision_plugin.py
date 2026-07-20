"""AOS Vision Plugin — image and video perception."""

from pathlib import Path


class VisionPlugin:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.name = "AOS Vision"
        self.id = "vision"

    def get_mcp_tools(self):
        return ["analyze_image", "analyze_video", "extract_image_data"]
