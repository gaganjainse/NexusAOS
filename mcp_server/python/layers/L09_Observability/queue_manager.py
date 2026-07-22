"""
NexusAOS - Queue Manager (The Cognitive Buffer)
Version: 1.0.0
Description: Decides the best time to execute deferred directives based on Soma physiology and Mind state.
"""

import time
import sys
from pathlib import Path
from typing import Dict, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from layers.L05_Memory.state_manager import StateManager
from layers.L02_Agent.metabolism_engine import MetabolismEngine
from layers.L02_Agent.endocrine_engine import EndocrineEngine
from layers.L10_Intelligence.thought_agent import ThoughtAgent

class QueueManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_mgr = StateManager(base_dir)
        self.metabolism = MetabolismEngine(base_dir)
        self.endocrine = EndocrineEngine(base_dir)
        self.thought = ThoughtAgent(base_dir)

    def defer_directive(self, text: str, priority: Optional[int] = None) -> str:
        """Buffers a directive into the Deferred queue with automated prioritization."""
        
        # Automatically decide optimal priority if not provided
        if priority is None:
            priority = self.thought.prioritize_intent(text)
            assigned_msg = f" (Autonomic Priority Assigned: {priority})"
        else:
            assigned_msg = f" (Sovereign Priority: {priority})"

        directive_id = f"def_{int(time.time())}"
        data = {
            "id": directive_id,
            "text": text,
            "priority": priority,
            "submitted_at": time.time(),
            "reasoning": f"Initial buffering with priority {priority}."
        }
        self.state_mgr.queue_directive(data)
        return f"Directive [{directive_id}] buffered in Cognitive Buffer.{assigned_msg}"

    def process_buffer(self) -> List[str]:
        """
        Analyzes the deferred queue and promotes directives to 'Pending' (Orchestrator pick-up)
        if biological and mental conditions are optimal.
        """
        deferred = self.state_mgr.get_queued_directives("Deferred")
        if not deferred:
            return []

        # Get current vitals
        phys = self.metabolism._report()
        vibe = self.endocrine.get_state().get("vibe", "Stable")
        energy = phys["energy"]

        promoted = []
        for d in deferred:
            should_promote = False
            reasoning = ""

            # Decision Logic: When is it 'Best'?
            if d["priority"] >= 9:
                should_promote = True
                reasoning = "High priority bypass. Immediate execution required."
            elif energy > 70 and vibe in ("Stable", "Euphoric"):
                should_promote = True
                reasoning = f"Optimal conditions: Energy ({energy:.1f}%) high, Vibe ({vibe}) stable."
            elif energy > 40 and d["priority"] >= 5:
                should_promote = True
                reasoning = f"Sufficient conditions: Energy ({energy:.1f}%) enough for medium priority."
            else:
                reasoning = f"Deferred: Waiting for higher energy or better system vibe. Current Energy: {energy:.1f}%"

            if should_promote:
                self.state_mgr.update_queue_status(d["directive_id"], "Pending", reasoning)
                promoted.append(f"Promoted [{d['directive_id']}]: {reasoning}")
            else:
                self.state_mgr.update_queue_status(d["directive_id"], "Deferred", reasoning)

        return promoted

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    qm = QueueManager(base)
    print(qm.defer_directive("Check system integrity", priority=5))
    print(qm.process_buffer())
