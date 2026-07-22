"""
NexusAOS - State Manager
Version: 1.0.0
Description: Centralized SQLite-based state management with row-level locking.
Replaces legacy JSON state files to prevent race conditions in simultaneous swarms.
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class StateManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.db_path = base_dir / "core" / "monitoring" / "nexus_state.db"
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database with tables for Canvas and Lattice."""
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Neural Canvas Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS canvas_nodes (
                node_id TEXT PRIMARY KEY,
                content TEXT,
                author_id TEXT,
                timestamp REAL,
                signature TEXT,
                verified_by TEXT, -- JSON list
                status TEXT DEFAULT 'Unverified'
            )
        """)
        
        # Lattice Tasks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lattice_tasks (
                task_id TEXT PRIMARY KEY,
                from_role TEXT,
                to_role TEXT,
                directive TEXT,
                context TEXT, -- JSON
                status TEXT,
                started_at REAL,
                completed_at REAL,
                result TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    # --- Neural Canvas Operations ---

    def upsert_canvas_node(self, node_data: Dict) -> bool:
        """Writes or updates a node using LWW (Last-Writer-Wins) logic."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            # Check existing timestamp for LWW
            cursor.execute("SELECT timestamp FROM canvas_nodes WHERE node_id = ?", (node_data["node_id"],))
            row = cursor.fetchone()
            if row and row[0] >= node_data["timestamp"]:
                return False # Newer data exists
                
            cursor.execute("""
                INSERT OR REPLACE INTO canvas_nodes (node_id, content, author_id, timestamp, signature, verified_by, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                node_data["node_id"], 
                json.dumps(node_data["content"]), 
                node_data["author_id"], 
                node_data["timestamp"], 
                node_data["signature"],
                json.dumps(node_data.get("verified_by", [])),
                node_data.get("status", "Unverified")
            ))
            conn.commit()
            return True
        finally:
            conn.close()

    def get_canvas_snapshot(self) -> Dict:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM canvas_nodes")
        nodes = {}
        for row in cursor.fetchall():
            nodes[row["node_id"]] = {
                "content": json.loads(row["content"]),
                "author": row["author_id"],
                "timestamp": row["timestamp"],
                "signature": row["signature"],
                "verified_by": json.loads(row["verified_by"]),
                "status": row["status"]
            }
        conn.close()
        return {"nodes": nodes, "last_convergence": time.time()}

    # --- Lattice Operations ---

    def create_lattice_task(self, task_data: Dict):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lattice_tasks (task_id, from_role, to_role, directive, context, status, started_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            task_data["task_id"],
            task_data["from"],
            task_data["to"],
            task_data["directive"],
            json.dumps(task_data.get("context", {})),
            task_data["status"],
            task_data["started_at"]
        ))
        conn.commit()
        conn.close()

    def get_active_tasks(self) -> List[Dict]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lattice_tasks WHERE status = 'Firing'")
        tasks = [dict(row) for row in cursor.fetchall()]
        for t in tasks:
            t["context"] = json.loads(t["context"])
        conn.close()
        return tasks

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    mgr = StateManager(base)
    print(f"State Database initialized at {mgr.db_path}")
