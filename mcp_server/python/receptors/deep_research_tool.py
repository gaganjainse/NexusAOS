"""
NexusAOS - Deep Research Tool (Nutrient Discovery)
Version: 1.0.0
Description: Scours the web and GitHub for architectural nutrients (LangGraph, Slurm, RDMA, etc.) to optimize the organism.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
from receptors.web_receptor import WebReceptor
from receptors.github_scanner import GitHubScanner

class DeepResearchTool:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.web = WebReceptor(base_dir)
        self.github = GitHubScanner(base_dir)
        self.research_path = base_dir / "archives" / "dna_core" / "learning" / "research_notes.json"

    def perform_deep_research(self, topic: str) -> Dict[str, Any]:
        """Performs a multi-layered scan of the web and source code for a specific architectural nutrient."""
        print(f"Deep Researching: {topic}...")
        
        # 1. Web Scan (Best Practices & Papers)
        web_results = self.web.search(f"{topic} architecture best practices research papers")
        
        # 2. GitHub Scan (Framework Nutrients)
        # If it's a known repo/organization, we scan it specifically
        repo_data = {}
        if "langgraph" in topic.lower():
            repo_data = self.github.scan_repo("langchain-ai/langgraph")
        elif "langchain" in topic.lower():
            repo_data = self.github.scan_repo("langchain-ai/langchain")
        
        research_entry = {
            "topic": topic,
            "timestamp": time.time(),
            "web_nutrients": web_results[:500], # Summary
            "github_nutrients": repo_data.get("structure", {}),
            "status": "INGESTED"
        }
        
        self._archive_research(research_entry)
        return research_entry

    def _archive_research(self, entry: Dict):
        if not self.research_path.parent.exists():
            self.research_path.parent.mkdir(parents=True, exist_ok=True)
            
        history = []
        if self.research_path.exists():
            try:
                history = json.loads(self.research_path.read_text(encoding="utf-8"))
            except: pass
            
        history.append(entry)
        self.research_path.write_text(json.dumps(history, indent=4), encoding="utf-8")

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    drt = DeepResearchTool(base)
    print(drt.perform_deep_research("LangGraph vs Slurm for Agent Swarms"))
