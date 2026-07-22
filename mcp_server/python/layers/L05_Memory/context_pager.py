"""
NexusAOS - Context Pager (Cognitive Memory Management)
Version: 1.0.0
Description: Swaps agent 'Thoughts' in and out of the context window to maximize reasoning efficiency.
Biological analog: Context Paging / Working Memory Shifting.
"""

import json
import time

from typing import Dict, List, Any, Optional

from pathlib import Path
import sys
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class ContextPager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.page_dir = base_dir / "active_core" / "monitoring_active" / "context_pages"
        self.page_dir.mkdir(parents=True, exist_ok=True)
        self.active_pages: Dict[str, Dict] = {}
        self.max_resident_pages = 5
        self.token_limit_baseline = 100000 # 100k fallback

    def trigger_autonomic_paging(self, current_context_chars: int, model_limit: int = None):
        """Neural 13.0: Token Sentry 2.0 - Prevents context overflow."""
        limit = model_limit or self.token_limit_baseline
        estimated_tokens = current_context_chars / 4.0
        
        if estimated_tokens > (limit * 0.75):
            # 75% saturation - Trigger Synaptic Compression
            from layers.L05_Memory.memory_synth import MemorySynth
            ms = MemorySynth(self.base_dir)
            wisdom_node = ms.summarize_long_context()
            
            # Page out the summarized wisdom to AMG
            self.page_out("long_context_summary", wisdom_node)
            return True, "Synaptic Compression Triggered. Old context offloaded to AMG."
            
        return False, "Context levels optimal."

    def page_out(self, agent_id: str, context_data: Any):
        """Swaps an agent's context out to 'Disk' (Long-term memory)."""
        page_path = self.page_dir / f"{agent_id}.page"
        page_content = {
            "agent_id": agent_id,
            "timestamp": time.time(),
            "data": context_data
        }
        page_path.write_text(json.dumps(page_content), encoding="utf-8")
        
        if agent_id in self.active_pages:
            del self.active_pages[agent_id]
            
        return f"Page-Out: Agent {agent_id} context swapped to persistent storage."

    def page_in(self, agent_id: str) -> Optional[Any]:
        """Swaps an agent's context back into 'Active Memory'."""
        page_path = self.page_dir / f"{agent_id}.page"
        if not page_path.exists():
            return None
            
        # LRU-style eviction if too many active pages
        if len(self.active_pages) >= self.max_resident_pages:
            oldest_agent = min(self.active_pages, key=lambda k: self.active_pages[k]["last_access"])
            self.page_out(oldest_agent, self.active_pages[oldest_agent]["data"])

        content = json.loads(page_path.read_text(encoding="utf-8"))
        self.active_pages[agent_id] = {
            "data": content["data"],
            "last_access": time.time()
        }
        return content["data"]

    def get_memory_map(self) -> Dict[str, str]:
        return {
            "resident": list(self.active_pages.keys()),
            "paged": [p.stem for p in self.page_dir.glob("*.page")]
        }

if __name__ == "__main__":
    from pathlib import Path
    base = Path(__file__).resolve().parent.parent.parent
    pager = ContextPager(base)
    pager.page_out("Agent_Alpha", {"task": "market_research", "progress": 0.5})
    print("Memory Map:", pager.get_memory_map())
    print("Page-In:", pager.page_in("Agent_Alpha"))
