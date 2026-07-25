# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - Wisdom Feed (Proactive Reporting)
Version: 1.0.0
Description: Maintains a persistent Intelligence Briefing for the Sovereign.
Push channel for high-salience swarm findings and physiological alerts.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

class WisdomFeed:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.feed_path = base_dir / ".artifacts" / "WISDOM_FEED.artifact.md"
        self._ensure_feed_exists()

    def _ensure_feed_exists(self):
        if not self.feed_path.parent.exists():
            self.feed_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.feed_path.exists():
            header = (
                "# 🧠 Sovereign Wisdom Feed\n"
                "*Real-time Proactive Intelligence from the SeshaAOS Swarm*\n\n"
                "--- \n\n"
            )
            self.feed_path.write_text(header, encoding="utf-8")

    def push_briefing(self, title: str, content: str, salience: str = "MEDIUM"):
        """Pushes a high-salience update to the top of the feed."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        vibe_sigil = "🔥" if salience == "CRITICAL" else "⚡" if salience == "HIGH" else "🔹"
        
        entry = (
            f"## {vibe_sigil} {title} | {timestamp}\n"
            f"> **Salience:** {salience}\n\n"
            f"{content}\n\n"
            "---\n\n"
        )
        
        current_content = self.feed_path.read_text(encoding="utf-8")
        # Find the end of the header
        header_end = current_content.find("--- \n\n") + 6
        header = current_content[:header_end]
        rest = current_content[header_end:]
        
        # Keep only last 50 entries to manage file size
        updated_content = header + entry + rest
        self.feed_path.write_text(updated_content, encoding="utf-8")
        return f"Briefing pushed to {self.feed_path.name}"

    def report_anomaly(self, component: str, error: str):
        """Pushes a critical physiological anomaly to the feed."""
        return self.push_briefing(
            title=f"SOMA ALERT: {component}",
            content=f"**Anomaly Detected:** {error}",
            salience="CRITICAL"
        )

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    feed = WisdomFeed(base)
    print(feed.push_briefing("Neural Link Established", "The Wisdom Feed is now online and synchronized with your workspace."))

