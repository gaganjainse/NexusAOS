"""
SeshaAOS - Slack Receptor (Social R11)
Version: 1.0.0
Description: Slack API integration for messaging.
"""
import json

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
import urllib.request
import os
from pathlib import Path
from typing import Dict, Optional


class SlackReceptor:
    """Slack API client for sending messages."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.token = os.environ.get("SLACK_BOT_TOKEN")
        self.api_base = "https://slack.com/api"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "SeshaAOS-SlackReceptor/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated Slack API request."""
        url = f"{self.api_base}{endpoint}"
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.load(resp)
                if result.get("ok"):
                    return {"success": True, "data": result}
                return {"success": False, "error": result.get("error", "Unknown error")}
        except urllib.error.HTTPError as e:
            return {"success": False, "status": e.code, "error": e.read().decode()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_message(self, channel: str, text: str, blocks: list = None) -> Dict:
        """Send a message to a Slack channel."""
        if not self.token:
            return {"success": False, "error": "SLACK_BOT_TOKEN not set"}
        data = {"channel": channel, "text": text}
        if blocks:
            data["blocks"] = blocks
        return self._request("POST", "/chat.postMessage", data)

    def get_channels(self) -> Dict:
        """List channels the bot is in."""
        if not self.token:
            return {"success": False, "error": "SLACK_BOT_TOKEN not set"}
        return self._request("GET", "/conversations.list")
