"""
SeshaAOS - Google Cloud Receptor (L06)
Version: 13.0.0
Description: High-priority interface for Google Vertex AI and Gemini APIs.
Implements Priority Headers and Global Failover to minimize RESOURCE_EXHAUSTED errors.
"""

import hashlib
import json
import random
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

from layers.L05_Memory.state_manager import StateManager

# Ensure root is in path
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class GoogleCloudReceptor:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_mgr = StateManager(base_dir)
        self.default_endpoint = "us-central1-aiplatform.googleapis.com"
        self.priority_endpoint = "global-vertexai.googleapis.com"
        self.use_priority_lane = True

    def get_context_cache(self, content: str) -> Optional[str]:
        """Neural 13.0: Checks for an existing valid context cache on Google's servers."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        cache_key = "Sesha_system_context"
        
        cache_id = self.state_mgr.get_valid_cache_id(cache_key, content_hash)
        if cache_id:
            print(f"Context Cache Hit: {cache_id}. Bypassing 90% of token ingestion.")
            return cache_id
        return None

    def register_new_cache(self, content: str, cache_id: str, ttl_seconds: int = 3600):
        """Neural 13.0: Registers a newly created cache from Vertex AI."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        self.state_mgr.upsert_context_cache("Sesha_system_context", cache_id, ttl_seconds, content_hash)
        print(f"Context Cache Created & Registered: {cache_id}")

    def get_priority_headers(self) -> Dict[str, str]:
        """Returns headers to force Google to prioritize our request."""
        headers = {
            "Content-Type": "application/json",
            "X-Vertex-AI-LLM-Shared-Request-Type": "priority" if self.use_priority_lane else "standard"
        }
        return headers

    def resolve_endpoint(self, error_count: int = 0) -> str:
        """Fails over to global endpoint if regional congestion is detected."""
        if error_count > 0:
            return self.priority_endpoint
        return self.default_endpoint

    def handle_resource_exhaustion(self, attempt: int) -> float:
        """Calculates jittered exponential backoff for 429/503 errors."""
        # Biological Backoff: 1s, 2s, 4s, 8s + jitter
        base_wait = 2 ** attempt
        jitter = random.uniform(0, 1)
        wait_time = base_wait + jitter
        
        print(f"RESOURCE_EXHAUSTED: Entering Hibernation Reflex. Waiting {wait_time:.2f}s (Attempt #{attempt})")
        return wait_time

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    gcr = GoogleCloudReceptor(base)
    print("Priority Headers:", gcr.get_priority_headers())
    print("Resolved Endpoint (Healthy):", gcr.resolve_endpoint())
    print("Resolved Endpoint (Congested):", gcr.resolve_endpoint(1))

