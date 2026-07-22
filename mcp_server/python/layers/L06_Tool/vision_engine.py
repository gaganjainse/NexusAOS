"""
AOS Vision Engine — image analysis, metadata extraction, and structured understanding.
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))


class VisionEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.cache_dir = base_dir / "core" / "monitoring" / "vision_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, image_path: str) -> Path:
        p = Path(image_path)
        if not p.is_absolute():
            p = self.base_dir / image_path
        return p.resolve()

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Extracts image metadata and performs basic visual analysis."""
        path = self._resolve_path(image_path)
        if not path.exists():
            return {"error": f"Image not found: {image_path}"}

        result = {
            "path": str(path.relative_to(self.base_dir)) if path.is_relative_to(self.base_dir) else str(path),
            "size_bytes": path.stat().st_size,
            "format": path.suffix.lower(),
        }

        try:
            from PIL import Image
            with Image.open(path) as img:
                result["width"] = img.width
                result["height"] = img.height
                result["mode"] = img.mode
                result["aspect_ratio"] = round(img.width / img.height, 3) if img.height else 0

                # Dominant color sampling (center pixel + corners)
                pixels = []
                for x, y in [(0, 0), (img.width - 1, 0), (0, img.height - 1), (img.width // 2, img.height // 2)]:
                    try:
                        pixels.append(img.getpixel((min(x, img.width - 1), min(y, img.height - 1))))
                    except Exception:
                        pass
                if pixels and isinstance(pixels[0], tuple):
                    avg = tuple(int(sum(c[i] for c in pixels) / len(pixels)) for i in range(len(pixels[0])))
                    result["dominant_color_rgb"] = avg
                    result["brightness"] = round(sum(avg[:3]) / 3 / 255 * 100, 1)

                # Basic classification heuristic
                if result.get("brightness", 50) < 20:
                    result["visual_class"] = "dark_scene"
                elif result.get("brightness", 50) > 80:
                    result["visual_class"] = "bright_scene"
                else:
                    result["visual_class"] = "balanced_scene"

                if img.width > img.height * 1.5:
                    result["layout"] = "landscape_wide"
                elif img.height > img.width * 1.5:
                    result["layout"] = "portrait_tall"
                else:
                    result["layout"] = "square_balanced"

                result["understanding"] = (
                    f"{result['visual_class']} image, {result['width']}x{result['height']} "
                    f"{result['mode']}, layout={result['layout']}, brightness={result.get('brightness', '?')}%"
                )

        except ImportError:
            result["understanding"] = f"Image file ({result['format']}, {result['size_bytes']} bytes). Install Pillow for deep analysis."
        except Exception as e:
            result["error"] = str(e)

        cache_file = self.cache_dir / f"{path.stem}_analysis.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result

    def extract_image_data(self, image_path: str) -> str:
        return json.dumps(self.analyze_image(image_path), indent=2)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = VisionEngine(base)
    print(json.dumps(engine.analyze_image("core/monitoring/physiology.json"), indent=2))
