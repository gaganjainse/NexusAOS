"""
SeshaAOS - GitHub Receptor (Lineage R8)
Version: 1.0.0
Description: GitHub API integration for issue creation, PR management, repo ops.
"""
import json

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
import urllib.request
import os
from pathlib import Path
from typing import Dict, Optional


class GitHubReceptor:
    """GitHub API client for creating issues, PRs, etc."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.token = os.environ.get("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "SeshaAOS-GitHubReceptor/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated GitHub API request."""
        url = f"{self.api_base}{endpoint}"
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {"success": True, "status": resp.status, "data": json.load(resp)}
        except urllib.error.HTTPError as e:
            return {"success": False, "status": e.code, "error": e.read().decode()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_issue(self, repo: str, title: str, body: str, labels: list = None) -> Dict:
        """Create a GitHub issue."""
        if not self.token:
            return {"success": False, "error": "GITHUB_TOKEN not set"}
        data = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        return self._request("POST", f"/repos/{repo}/issues", data)

    def create_pr(self, repo: str, title: str, head: str, base: str, body: str = "") -> Dict:
        """Create a pull request."""
        if not self.token:
            return {"success": False, "error": "GITHUB_TOKEN not set"}
        data = {"title": title, "head": head, "base": base, "body": body}
        return self._request("POST", f"/repos/{repo}/pulls", data)

    def get_repo(self, repo: str) -> Dict:
        """Get repository info."""
        return self._request("GET", f"/repos/{repo}")
