# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
# TRANSPARENCY: simulated/file-based — Specialization framework referenced (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA.
"""
SeshaAOS - Geo Receptor (Spatial R12)
Version: 1.0.0
Description: Geographic lookup via OpenStreetMap Nominatim (free, no API key needed).
"""
import json

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Optional


class GeoReceptor:
    """Geocoding via OpenStreetMap Nominatim (free tier)."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.api_base = "https://nominatim.openstreetmap.org"
        self.headers = {
            "User-Agent": "SeshaAOS-GeoReceptor/1.0 (contact@example.com)",
            "Accept": "application/json"
        }

    def _request(self, endpoint: str, params: Dict) -> Dict:
        """Make request to Nominatim."""
        url = f"{self.api_base}{endpoint}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {"success": True, "data": json.load(resp)}
        except urllib.error.HTTPError as e:
            return {"success": False, "status": e.code, "error": e.read().decode()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def geocode(self, place: str, limit: int = 5) -> Dict:
        """Search for a place by name."""
        return self._request("/search", {"q": place, "format": "json", "limit": limit})

    def reverse_geocode(self, lat: float, lon: float) -> Dict:
        """Reverse geocode coordinates to address."""
        return self._request("/reverse", {"lat": lat, "lon": lon, "format": "json"})
