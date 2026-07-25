# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
# TRANSPARENCY: simulated/file-based — Specialization framework referenced (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA.
"""
SeshaAOS - Deep Research Tool (Nutrient Discovery)
Version: 1.0.0
Description: Scours the web and GitHub for architectural nutrients (LangGraph, Slurm, RDMA, etc.) to optimize the organism.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

from layers.L06_Tool.github_scanner import GitHubScanner
from layers.L06_Tool.web_receptor import WebReceptor

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class DeepResearchTool:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.web = WebReceptor(base_dir)
        self.github = GitHubScanner(base_dir)
        self.research_path = base_dir / "archives" / "dna_core" / "learning" / "research_notes.json"

    def perform_deep_research(self, topic: str) -> Dict[str, Any]:
        """Performs a multi-layered scan of the web and source code for a specific architectural nutrient."""
        # 0. Check Semantic Nutrient Cache (Bone Marrow)
        if self.research_path.exists():
            try:
                history = json.loads(self.research_path.read_text(encoding="utf-8"))
                for entry in history:
                    if entry.get("topic") == topic:
                        # Cache hit: Check age
                        if time.time() - entry.get("timestamp", 0) < 86400: # 24h cache
                            print(f"Nutrient Cache Hit: {topic}. Returning from Bone Marrow.")
                            return entry
            except: pass

        print(f"Deep Researching: {topic}...")
        
        # 1. Web Scan (Best Practices & Papers)
        web_results = self.web.search_web(f"{topic} architecture best practices research papers")
        
        # 2. GitHub Scan (Framework Nutrients)
        # Dynamic repository discovery
        search_query = f"{topic} architecture"
        found_repos = self.github.search_repos(search_query, max_results=3)
        
        all_repo_data = []
        for repo in found_repos:
            repo_info = self.github.scan_repo(repo)
            all_repo_data.append({
                "repo": repo.full_name,
                "patterns": repo_info.patterns
            })
        
        # 3. DNA Synthesis (Learning Artifact)
        research_entry = {
            "topic": topic,
            "timestamp": time.time(),
            "web_summary": web_results.get("results", [])[:3],
            "github_patterns": all_repo_data,
            "learning_dna": self._synthesize_dna(topic, web_results, all_repo_data),
            "status": "INGESTED"
        }
        
        self._archive_research(research_entry)
        return research_entry

    def _synthesize_dna(self, topic: str, web: dict, github: list) -> dict:
        """Synthesizes raw data into actionable DNA instructions."""
        dna = {
            "origin": topic,
            "protocols": [],
            "skills": []
        }
        
        # Extract keywords from web results
        for res in web.get("results", []):
            if "architecture" in res.get("title", "").lower():
                dna["protocols"].append(f"ADOPT:{res['title']}")
                
        # Extract patterns from github
        for repo in github:
            patterns = repo.get("patterns", {})
            if patterns.get("architecture"):
                for p, v in patterns["architecture"].items():
                    if v: dna["skills"].append(f"PATTERN:{p.upper()}")
                    
        return dna

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

