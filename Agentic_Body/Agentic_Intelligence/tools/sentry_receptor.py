"""
SeshaAOS - Sentry Receptor (Introspection R11)
Version: 1.0.0
Description: Sentry API integration for error monitoring.
"""

import sys
import json
import urllib.request
import os
from pathlib import Path
from typing import Dict, List, Optional, Type

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))


class SentryReceptor:
    """Sentry API client for fetching errors/issues."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.token = os.environ.get("SENTRY_AUTH_TOKEN")
        self.org = os.environ.get("SENTRY_ORG")
        self.api_base = "https://sentry.io/api/0"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "SeshaAOS-SentryReceptor/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _request(self, method: str, endpoint: str, params: Dict | None = None) -> Dict:
        """Make authenticated Sentry API request."""
        url = f"{self.api_base}{endpoint}"
        if params:
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"
        req = urllib.request.Request(url, method=method, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {"success": True, "data": json.load(resp)}
        except urllib.error.HTTPError as e:
            return {"success": False, "status": e.code, "error": e.read().decode()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_project_issues(self, project: str, limit: int = 10) -> Dict:
        """Get recent issues for a project."""
        if not self.token or not self.org:
            return {"success": False, "error": "SENTRY_AUTH_TOKEN and SENTRY_ORG required"}
        return self._request("GET", f"/projects/{self.org}/{project}/issues/", {"limit": limit})

    def get_issue_details(self, project: str, issue_id: str) -> Dict:
        """Get details for a specific issue."""
        if not self.token or not self.org:
            return {"success": False, "error": "SENTRY_AUTH_TOKEN and SENTRY_ORG required"}
        return self._request("GET", f"/projects/{self.org}/{project}/issues/{issue_id}/")

    def list_projects(self) -> Dict:
        """List projects in organization."""
        if not self.token or not self.org:
            return {"success": False, "error": "SENTRY_AUTH_TOKEN and SENTRY_ORG required"}
        return self._request("GET", f"/organizations/{self.org}/projects/")
