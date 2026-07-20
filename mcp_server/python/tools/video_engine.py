"""
AOS Video Engine — video metadata extraction and frame analysis.
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

_tools_parent = Path(__file__).resolve().parent.parent
if str(_tools_parent) not in sys.path:
    sys.path.insert(0, str(_tools_parent))

from tools.vision_engine import VisionEngine


class VideoEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.cache_dir = base_dir / "core" / "monitoring" / "video_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.vision = VisionEngine(base_dir)

    def _resolve_path(self, video_path: str) -> Path:
        p = Path(video_path)
        if not p.is_absolute():
            p = self.base_dir / video_path
        return p.resolve()

    def analyze_video(self, video_path: str, max_frames: int = 5) -> Dict[str, Any]:
        """Extracts video metadata and analyzes sample frames."""
        path = self._resolve_path(video_path)
        if not path.exists():
            return {"error": f"Video not found: {video_path}"}

        result = {
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "format": path.suffix.lower(),
            "frames_analyzed": [],
        }

        try:
            import cv2
            cap = cv2.VideoCapture(str(path))
            result["fps"] = round(cap.get(cv2.CAP_PROP_FPS), 2)
            result["frame_count"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            result["width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            result["height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = result["frame_count"] / result["fps"] if result["fps"] > 0 else 0
            result["duration_seconds"] = round(duration, 2)

            # Sample frames evenly
            indices = [int(i * result["frame_count"] / max_frames) for i in range(max_frames)]
            for idx in indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    frame_path = self.cache_dir / f"{path.stem}_frame_{idx}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    frame_analysis = self.vision.analyze_image(str(frame_path))
                    result["frames_analyzed"].append({"frame_index": idx, "analysis": frame_analysis})

            cap.release()
            result["understanding"] = (
                f"Video {result['width']}x{result['height']}, {result['duration_seconds']}s, "
                f"{result['fps']}fps, {len(result['frames_analyzed'])} frames sampled."
            )
        except ImportError:
            result["understanding"] = (
                f"Video file ({result['format']}, {result['size_bytes']} bytes). "
                "Install opencv-python for frame extraction and analysis."
            )
        except Exception as e:
            result["error"] = str(e)

        cache_file = self.cache_dir / f"{path.stem}_video_analysis.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=str)

        return result

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    print(json.dumps(VideoEngine(base).analyze_video("nonexistent.mp4"), indent=2))
