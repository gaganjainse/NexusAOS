"""
SeshaAOS - Excalidraw Receptor
Agent's visual cortex - reads/writes Excalidraw canvases programmatically.
Supports self-hosted Excalidraw and Excalidraw Plus API.
"""

import sys
import json
import time
import uuid
import os
import urllib.request
import urllib.parse

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import base64

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))


class ElementType(Enum):
    RECTANGLE = "rectangle"
    ELLIPSE = "ellipse"
    DIAMOND = "diamond"
    ARROW = "arrow"
    LINE = "line"
    TEXT = "text"
    FREEDRAW = "freedraw"
    IMAGE = "image"
    FRAME = "frame"
    SELECTION = "selection"


@dataclass
class ExcalidrawElement:
    """Structured Excalidraw canvas element - agent readable/writable."""
    type: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    x: float = 0
    y: float = 0
    width: float = 100
    height: float = 100
    angle: float = 0
    strokeColor: str = "#1e1e1e"
    backgroundColor: str = "transparent"
    fillStyle: str = "solid"
    strokeWidth: float = 2
    strokeStyle: str = "solid"
    roughness: float = 1
    opacity: int = 100
    groupIds: list[str] = field(default_factory=list)
    frameId: str | None = None
    roundness: float | None = None
    seed: int = field(default_factory=lambda: int(time.time() * 1000) % 1000000)
    version: int = 1
    versionNonce: int = field(default_factory=lambda: int(time.time() * 1000000) % 1000000)
    isDeleted: bool = False
    boundElements: list[Dict] | None = None
    updated: int = field(default_factory=lambda: int(time.time() * 1000))
    link: str | None = None
    locked: bool = False
    
    # Text-specific
    text: str = ""
    fontSize: float = 20
    fontFamily: int = 1
    textAlign: str = "center"
    verticalAlign: str = "middle"
    containerId: str | None = None
    originalText: str = ""
    lineHeight: float = 1.25
    
    # Arrow/Line specific
    startBinding: Dict | None = None
    endBinding: Dict | None = None
    startArrowhead: str | None = None
    endArrowhead: str = "arrow"
    
    # FreeDraw specific
    points: list[list[float]] | None = None
    pressures: list[float] | None = None
    simulatePressure: bool = False
    
    # Image specific
    fileId: str | None = None
    scale: list[float] | None = None
    crop: Dict | None = None
    
    # Frame specific
    name: str | None = None
    
    # Custom agent data
    customData: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to Excalidraw JSON format."""
        d = asdict(self)
        # Remove None values
        return {k: v for k, v in d.items() if v is not None}
    
    @classmethod
    def create_text(cls, x: float, y: float, text: str, agent_id: str, 
                    confidence: float = 0.8, reasoning_type: str = "insight") -> 'ExcalidrawElement':
        """Create a text element for agent reasoning."""
        return cls(
            type="text",
            x=x, y=y,
            text=text,
            fontSize=16,
            customData={
                "agent_id": agent_id,
                "timestamp": time.time(),
                "type": "reasoning",
                "confidence": confidence,
                "reasoning_type": reasoning_type
            }
        )
    
    @classmethod
    def create_arrow(cls, from_id: str, to_id: str, label: str = "", 
                     agent_id: str = "", connection_type: str = "supports") -> 'ExcalidrawElement':
        """Create an arrow connecting two elements (synaptic connection)."""
        return cls(
            type="arrow",
            x=0, y=0,
            startBinding={"elementId": from_id, "focus": 0.5},
            endBinding={"elementId": to_id, "focus": 0.5},
            text=label,
            endArrowhead="arrow",
            customData={
                "agent_id": agent_id,
                "timestamp": time.time(),
                "type": "connection",
                "connection_type": connection_type
            }
        )
    
    @classmethod
    def create_frame(cls, x: float, y: float, width: float, height: float, 
                     name: str, agent_id: str) -> 'ExcalidrawElement':
        """Create a frame (concept grouping)."""
        return cls(
            type="frame",
            x=x, y=y,
            width=width, height=height,
            name=name,
            customData={
                "agent_id": agent_id,
                "timestamp": time.time(),
                "type": "frame"
            }
        )


class ExcalidrawReceptor:
    """
    Agent's visual cortex - reads/writes Excalidraw canvases programmatically.
    Supports self-hosted Excalidraw and Excalidraw Plus API.
    """
    
    def __init__(self, base_dir: Path, api_url: str = None, api_key: str = None):
        self.base_dir = base_dir
        self.api_url = api_url or os.environ.get("EXCALIDRAW_API_URL", "http://localhost:3000/api")
        self.api_key = api_key or os.environ.get("EXCALIDRAW_API_KEY")
        self.is_cloud = bool(self.api_key)
        
        # Local file storage for self-hosted
        self.canvases_dir = base_dir / "core" / "monitoring" / "canvases"
        self.canvases_dir.mkdir(parents=True, exist_ok=True)
        
        # Scene cache
        self._scene_cache: dict[str, Dict] = {}
    
    # === Cloud API Methods ===
    
    def _cloud_request(self, method: str, endpoint: str, data: Dict | None = None) -> Dict:
        """Make authenticated request to Excalidraw Plus API."""
        if not self.is_cloud:
            raise RuntimeError("Cloud API not configured. Set EXCALIDRAW_API_KEY.")
        
        url = f"https://api.excalidraw.com/api/v1{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.read().decode()}"}
        except Exception as e:
            return {"error": str(e)}
    
    # === Local File Methods ===
    
    def _local_scene_path(self, scene_id: str) -> Path:
        return self.canvases_dir / f"{scene_id}.json"
    
    def _load_local_scene(self, scene_id: str) -> Dict:
        path = self._local_scene_path(scene_id)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        # Create new scene
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "Sesha-aos",
            "elements": [],
            "appState": {
                "gridSize": 20,
                "viewBackgroundColor": "#",
                "currentItemStrokeColor": "#1e1e1e",
                "currentItemBackgroundColor": "transparent",
                "currentItemFillStyle": "solid",
                "currentItemStrokeWidth": 2,
                "currentItemStrokeStyle": "solid",
                "currentItemRoughness": 1,
                "currentItemOpacity": 100,
                "currentItemFontFamily": 1,
                "currentItemFontSize": 20,
                "currentItemTextAlign": "center",
                "currentItemStartArrowhead": None,
                "currentItemEndArrowhead": "arrow",
                "scrollX": 0,
                "scrollY": 0,
                "zoom": {"value": 1}
            },
            "files": {}
        }
    
    def _save_local_scene(self, scene_id: str, scene: Dict):
        path = self._local_scene_path(scene_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(scene, f, indent=2)
    
    # === Public API ===
    
    def create_canvas(self, canvas_id: str = None, title: str = "Agent Canvas") -> str:
        """Create a new canvas."""
        canvas_id = canvas_id or f"canvas_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        if self.is_cloud:
            result = self._cloud_request("POST", "/scenes", {
                "name": title,
                "elements": [],
                "appState": {"gridSize": 20}
            })
            if "error" not in result:
                return result.get("id", canvas_id)
        else:
            scene = self._load_local_scene(canvas_id)
            scene["appState"]["name"] = title
            self._save_local_scene(canvas_id, scene)
        
        return canvas_id
    
    def get_canvas(self, canvas_id: str) -> Dict:
        """Get full canvas state."""
        if self.is_cloud:
            return self._cloud_request("GET", f"/scenes/{canvas_id}")
        else:
            return self._load_local_scene(canvas_id)
    
    def list_canvases(self) -> list[Dict]:
        """List all canvases."""
        if self.is_cloud:
            return self._cloud_request("GET", "/scenes")
        else:
            canvases = []
            for path in self.canvases_dir.glob("*.json"):
                with open(path, "r") as f:
                    scene = json.load(f)
                    canvases.append({
                        "id": path.stem,
                        "name": scene.get("appState", {}).get("name", path.stem),
                        "element_count": len(scene.get("elements", [])),
                        "updated": scene.get("appState", {}).get("updated", 0)
                    })
            return canvases
    
    def perceive_canvas(self, canvas_id: str, agent_id: str) -> list[Dict]:
        """
        Read canvas as structured data for agent reasoning.
        Returns interpreted elements with agent-relevant metadata.
        """
        scene = self.get_canvas(canvas_id)
        elements = scene.get("elements", [])
        
        interpreted = []
        for elem in elements:
            if elem.get("isDeleted"):
                continue
            
            interpreted_elem = {
                "id": elem.get("id"),
                "type": elem.get("type"),
                "position": {"x": elem.get("x", 0), "y": elem.get("y", 0)},
                "size": {"width": elem.get("width", 0), "height": elem.get("height", 0)},
                "content": elem.get("text", ""),
                "metadata": elem.get("customData", {}),
                "connections": []
            }
            
            # Find connections (arrows) to/from this element
            for other in elements:
                if other.get("type") == "arrow":
                    start = other.get("startBinding", {}).get("elementId")
                    end = other.get("endBinding", {}).get("elementId")
                    if start == elem.get("id"):
                        interpreted_elem["connections"].append({
                            "type": "outgoing",
                            "to": end,
                            "label": other.get("text", ""),
                            "connection_type": other.get("customData", {}).get("connection_type", "unknown")
                        })
                    elif end == elem.get("id"):
                        interpreted_elem["connections"].append({
                            "type": "incoming",
                            "from": start,
                            "label": other.get("text", ""),
                            "connection_type": other.get("customData", {}).get("connection_type", "unknown")
                        })
            
            interpreted.append(interpreted_elem)
        
        return interpreted
    
    def think_on_canvas(self, canvas_id: str, agent_id: str, 
                        x: float, y: float, content: str,
                        confidence: float = 0.8, reasoning_type: str = "insight") -> str:
        """Agent writes reasoning/thought as canvas element."""
        element = ExcalidrawElement.create_text(x, y, content, agent_id, confidence, "reasoning")
        
        if self.is_cloud:
            result = self._cloud_request("POST", f"/scenes/{canvas_id}/elements", element.to_dict())
            return result.get("id", element.id)
        else:
            scene = self._load_local_scene(canvas_id)
            scene["elements"].append(element.to_dict())
            scene["appState"]["updated"] = int(time.time() * 1000)
            self._save_local_scene(canvas_id, scene)
            return element.id
    
    def draw_connection(self, canvas_id: str, from_id: str, to_id: str, 
                        label: str = "", agent_id: str = "", 
                        connection_type: str = "supports") -> str:
        """Draw synaptic connection between concepts."""
        element = ExcalidrawElement.create_arrow(from_id, to_id, label, agent_id, connection_type)
        
        if self.is_cloud:
            result = self._cloud_request("POST", f"/scenes/{canvas_id}/elements", element.to_dict())
            return result.get("id", element.id)
        else:
            scene = self._load_local_scene(canvas_id)
            scene["elements"].append(element.to_dict())
            scene["appState"]["updated"] = int(time.time() * 1000)
            self._save_local_scene(canvas_id, scene)
            return element.id
    
    def create_concept_frame(self, canvas_id: str, x: float, y: float, 
                             width: float, height: float, name: str, agent_id: str) -> str:
        """Create a frame to group related concepts."""
        element = ExcalidrawElement.create_frame(x, y, width, height, name, agent_id)
        
        if self.is_cloud:
            result = self._cloud_request("POST", f"/scenes/{canvas_id}/elements", element.to_dict())
            return result.get("id", element.id)
        else:
            scene = self._load_local_scene(canvas_id)
            scene["elements"].append(element.to_dict())
            self._save_local_scene(canvas_id, scene)
            return element.id
    
    def search_canvas(self, canvas_id: str, query: str) -> list[Dict]:
        """Semantic search on canvas content."""
        scene = self.get_canvas(canvas_id)
        elements = scene.get("elements", [])
        
        results = []
        query_lower = query.lower()
        for elem in elements:
            if elem.get("isDeleted"):
                continue
            text = elem.get("text", "").lower()
            name = elem.get("name", "").lower()
            custom = json.dumps(elem.get("customData", {})).lower()
            
            if query_lower in text or query_lower in name or query_lower in custom:
                results.append({
                    "id": elem.get("id"),
                    "type": elem.get("type"),
                    "content": elem.get("text", "") or elem.get("name", ""),
                    "position": {"x": elem.get("x"), "y": elem.get("y")},
                    "metadata": elem.get("customData", {})
                })
        
        return results
    
    def export_canvas(self, canvas_id: str, fmt: str = "json") -> str | bytes:
        """Export canvas in various formats."""
        scene = self.get_canvas(canvas_id)
        
        if fmt == "json":
            return json.dumps(scene, indent=2)
        elif fmt == "markdown":
            return self._scene_to_markdown(scene)
        elif fmt == "png":
            # Would require headless browser - placeholder
            return b"PNG export requires headless browser"
        else:
            raise ValueError(f"Unsupported format: {fmt}")
    
    def _scene_to_markdown(self, scene: Dict) -> str:
        """Convert canvas to structured markdown for documentation."""
        elements = scene.get("elements", [])
        
        md = [f"# Canvas: {scene.get('appState', {}).get('name', 'Untitled')}\n"]
        
        # Group by frames
        frames = [e for e in elements if e.get("type") == "frame"]
        frameless = [e for e in elements if e.get("type") != "frame" and not e.get("frameId")]
        
        for frame in frames:
            md.append(f"\n## {frame.get('name', 'Frame')}\n")
            frame_elements = [e for e in frameless if e.get("frameId") == frame.get("id")]
            for elem in frame_elements:
                if elem.get("type") == "text" and elem.get("text"):
                    md.append(f"- {elem['text']}")
                elif elem.get("type") in ["rectangle", "ellipse", "diamond"]:
                    md.append(f"- [{elem.get('type')}] at ({elem.get('x')}, {elem.get('y')})")
        
        # Frameless elements
        if frameless:
            md.append("\n## Unframed\n")
            for elem in frameless:
                if elem.get("type") == "text" and elem.get("text"):
                    md.append(f"- {elem['text']}")
        
        return "\n".join(md)


# === MCP Tool Wrappers ===

def create_excalidraw_tools(base_dir: Path):
    """Create MCP tool wrappers for Excalidraw receptor."""
    receptor = ExcalidrawReceptor(base_dir)
    
    tools = {}
    
    def perceive_canvas(canvas_id: str, agent_id: str) -> str:
        """Read canvas as structured data for agent reasoning."""
        result = receptor.perceive_canvas(canvas_id, agent_id)
        return json.dumps(result, indent=2)
    
    def think_on_canvas(canvas_id: str, agent_id: str, x: float, y: float, 
                        content: str, confidence: float = 0.8, 
                        reasoning_type: str = "insight") -> str:
        """Agent writes reasoning/thought as canvas element."""
        element_id = receptor.think_on_canvas(canvas_id, agent_id, x, y, content, confidence, reasoning_type)
        return json.dumps({"element_id": element_id, "status": "created"})
    
    def draw_connection(canvas_id: str, from_id: str, to_id: str,
                        label: str = "", agent_id: str = "",
                        connection_type: str = "supports") -> str:
        """Draw synaptic connection between concepts."""
        element_id = receptor.draw_connection(canvas_id, from_id, to_id, label, agent_id, connection_type)
        return json.dumps({"element_id": element_id, "status": "connected"})
    
    def create_frame(canvas_id: str, x: float, y: float, width: float, 
                     height: float, name: str, agent_id: str) -> str:
        """Create a frame to group related concepts."""
        element_id = receptor.create_concept_frame(canvas_id, x, y, width, height, name, agent_id)
        return json.dumps({"element_id": element_id, "status": "framed"})
    
    def search_canvas(canvas_id: str, query: str) -> str:
        """Semantic search on canvas content."""
        results = receptor.search_canvas(canvas_id, query)
        return json.dumps(results, indent=2)
    
    def export_canvas(canvas_id: str, format: str = "json") -> str:
        """Export canvas in various formats."""
        result = receptor.export_canvas(canvas_id, format)
        if isinstance(result, bytes):
            return f"Binary {format} export ({len(result)} bytes)"
        return result
    
    def list_canvases() -> str:
        """List all available canvases."""
        canvases = receptor.list_canvases()
        return json.dumps(canvases, indent=2)
    
    def create_canvas(canvas_id: str = None, title: str = "Agent Canvas") -> str:
        """Create a new canvas."""
        cid = receptor.create_canvas(canvas_id, title)
        return json.dumps({"canvas_id": cid, "status": "created"})
    
    # Return tool functions with metadata
    return {
        "perceive_canvas": perceive_canvas,
        "think_on_canvas": think_on_canvas,
        "draw_connection": draw_connection,
        "create_frame": create_frame,
        "search_canvas": search_canvas,
        "export_canvas": export_canvas,
        "list_canvases": list_canvases,
        "create_canvas": create_canvas
    }


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    receptor = ExcalidrawReceptor(base)
    
    # Demo
    canvas_id = receptor.create_canvas("demo-canvas", "Research Canvas")
    print(f"Created canvas: {canvas_id}")
    
    # Agent thinks
    elem_id = receptor.think_on_canvas(canvas_id, "research-lead", 100, 100, 
                                       "Key insight: Attention is O(n²)", 0.95, "insight")
    print(f"Thought recorded: {elem_id}")
    
    # Another thought
    elem_id2 = receptor.think_on_canvas(canvas_id, "research-lead", 100, 200,
                                        "Linear attention reduces to O(n)", 0.9, "hypothesis")
    
    # Connect them
    conn_id = receptor.draw_connection(canvas_id, elem_id, elem_id2, 
                                       "enables", "research-lead", "enables")
    print(f"Connection drawn: {conn_id}")
    
    # Frame them
    frame_id = receptor.create_concept_frame(canvas_id, 50, 50, 400, 300,
                                             "Attention Research", "research-lead")
    print(f"Frame created: {frame_id}")
    
    # Export
    md = receptor.export_canvas(canvas_id, "markdown")
    print(f"\nMarkdown export:\n{md}")
