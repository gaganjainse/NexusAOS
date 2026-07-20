"""
AOS Plugin Registry — native integration of Plugins, MCPs, Skills, Subagents, Rules, Commands, Hooks.
Version: 1.0.0
"""

import importlib
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE = Path(__file__).resolve().parent.parent  # project root


class PluginRegistry:
    """Discovers and loads AOS platform extensions."""

    LAYER_TYPES = ("plugins", "mcps", "skills", "subagents", "rules", "commands", "hooks")

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or BASE
        self.manifest_path = self.base_dir / "plugins" / "manifest.json"
        self.cursor_dir = self.base_dir / ".cursor"

    def _read_manifest(self) -> Dict[str, Any]:
        if not self.manifest_path.exists():
            return {"plugins": [], "version": "1.0.0"}
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_layers(self) -> Dict[str, List[str]]:
        manifest = self._read_manifest()
        result = {layer: [] for layer in self.LAYER_TYPES}
        for plugin in manifest.get("plugins", []):
            for layer in self.LAYER_TYPES:
                items = plugin.get(layer, [])
                result[layer].extend(items)
        # Cursor-native paths
        if self.cursor_dir.exists():
            for layer in ("rules", "skills", "commands", "hooks"):
                layer_dir = self.cursor_dir / layer
                if layer_dir.exists():
                    result[layer].extend([str(p.relative_to(self.base_dir)) for p in layer_dir.rglob("*") if p.is_file()])
            hooks_file = self.cursor_dir / "hooks.json"
            if hooks_file.exists():
                result["hooks"].append(str(hooks_file.relative_to(self.base_dir)))
            mcp_file = self.cursor_dir / "mcp.json"
            if mcp_file.exists():
                result["mcps"].append(str(mcp_file.relative_to(self.base_dir)))
            cursor_manifest = self.cursor_dir / "manifest.json"
            if cursor_manifest.exists():
                try:
                    with open(cursor_manifest, "r", encoding="utf-8") as f:
                        cursor_data = json.load(f)
                    for key in ("skills", "rules", "commands", "hooks", "subagents"):
                        if key in cursor_data:
                            result[key].extend(cursor_data[key])
                except Exception:
                    pass
        return result

    def load_plugin(self, module_path: str):
        """Loads a plugin module by dotted path relative to plugins/."""
        full = self.base_dir / "plugins" / module_path.replace(".", "/")
        if full.suffix != ".py":
            full = Path(str(full) + ".py")
        spec_name = f"aos_plugin_{full.stem}"
        if str(self.base_dir / "plugins") not in sys.path:
            sys.path.insert(0, str(self.base_dir / "plugins"))
        mod = importlib.import_module(module_path.replace("/", ".").removesuffix(".py"))
        return mod

    def get_status(self) -> Dict[str, Any]:
        layers = self.list_layers()
        return {
            "manifest": str(self.manifest_path),
            "cursor_bridge": self.cursor_dir.exists(),
            "layers": {k: len(v) for k, v in layers.items()},
            "items": layers,
        }

if __name__ == "__main__":
    import json as _json
    print(_json.dumps(PluginRegistry().get_status(), indent=2))
