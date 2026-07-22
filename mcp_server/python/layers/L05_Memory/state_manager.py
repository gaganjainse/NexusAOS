"""
NexusAOS - State Manager
Version: 1.0.0
Description: Centralized SQLite-based state management with row-level locking.
Replaces legacy JSON state files to prevent race conditions in simultaneous swarms.
"""

import sqlite3
import json
import time

from typing import Dict, Any, List, Optional

from pathlib import Path
import sys
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

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

        # Universal Domain Graph (UDG) Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS domain_graph (
                node_id TEXT PRIMARY KEY,
                zone TEXT,
                belief_content TEXT, -- HSML Belief Structure
                latent_vibe BLOB,   -- Vector embedding
                variational_free_energy REAL,
                provenance_sigil TEXT, -- !, ?, ◊, ~
                last_sync REAL
            )
        """)

        # Directive Queue Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS directive_queue (
                directive_id TEXT PRIMARY KEY,
                text TEXT,
                priority INTEGER,
                status TEXT,
                submitted_at REAL,
                completed_at REAL,
                reasoning TEXT,
                outcome TEXT
            )
        """)

        # Synaptic Signals Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS synaptic_signals (
                signal_type TEXT PRIMARY KEY,
                payload TEXT, -- JSON
                emitted_at REAL,
                ttl_seconds INTEGER,
                evidentiality TEXT,
                active INTEGER DEFAULT 1
            )
        """)

        # Signal History Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signal_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_type TEXT,
                payload TEXT,
                timestamp REAL,
                ttl_seconds INTEGER,
                evidentiality TEXT
            )
        """)

        # Immune Registry Table (Antigens & Antibodies)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS immune_registry (
                antigen_id TEXT PRIMARY KEY,
                type TEXT,
                details TEXT,
                detected_at REAL,
                neutralized INTEGER DEFAULT 0,
                antibody_id TEXT
            )
        """)

        # Motor Execution Log Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS motor_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                action TEXT,
                target TEXT,
                success INTEGER,
                result TEXT
            )
        """)

        # Routing Weights Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS routing_weights (
                signal_type TEXT PRIMARY KEY,
                to_role TEXT,
                priority INTEGER,
                action TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0
            )
        """)
        
        # Kùzu Pipeline Triggers (Simulated)
        # In Neural 6.0, these are compiled into the DB engine for sub-5us detection
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS db_native_reflexes (
                trigger_pattern TEXT PRIMARY KEY,
                reflex_action TEXT,
                priority INTEGER
            )
        """)
        
        conn.commit()

        # Hive Locks Table (L13 Collision Prevention)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hive_locks (
                lock_id TEXT PRIMARY KEY,
                holder_node TEXT,
                acquired_at REAL,
                expires_at REAL
            )
        """)

        # Context Caches Table (Neural 13.0)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_caches (
                cache_key TEXT PRIMARY KEY,
                cache_id TEXT,
                expires_at REAL,
                content_hash TEXT
            )
        """)
        conn.commit()

        # Migrations
        try:
            cursor.execute("ALTER TABLE directive_queue ADD COLUMN outcome TEXT")
        except Exception: pass
        try:
            cursor.execute("ALTER TABLE directive_queue ADD COLUMN completed_at REAL")
        except Exception: pass
        conn.commit()
        conn.close()

    def detect_native_reflex(self, event_data: str) -> Optional[str]:
        """Neural 6.0: Simulated DB-native reasoning trigger."""
        conn = self._get_connection()
        cursor = conn.cursor()
        # Find reflexes matching the current event pattern
        cursor.execute("SELECT reflex_action FROM db_native_reflexes WHERE ? LIKE '%' || trigger_pattern || '%'", (event_data,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

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

    # --- Directive Queue Operations ---

    def queue_directive(self, data: Dict):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO directive_queue (directive_id, text, priority, status, submitted_at, reasoning)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["id"],
            data["text"],
            data["priority"],
            data.get("status", "pending"),
            data["submitted_at"],
            data.get("reasoning", "")
        ))
        conn.commit()
        conn.close()

    def get_queued_directives(self, status: str = "pending") -> List[Dict]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM directive_queue WHERE status = ?", (status,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def update_directive_status(self, directive_id: str, status: str, outcome: str = "", completed_at: Optional[float] = None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE directive_queue SET status = ?, outcome = ?, completed_at = ? WHERE directive_id = ?
        """, (status, outcome, completed_at or time.time(), directive_id))
        conn.commit()
        conn.close()

    # --- Signal Operations ---

    def upsert_signal(self, signal_type: str, payload: Dict, ttl_seconds: int, evidentiality: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO synaptic_signals (signal_type, payload, emitted_at, ttl_seconds, evidentiality, active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (signal_type, json.dumps(payload), time.time(), ttl_seconds, evidentiality))
        conn.commit()
        conn.close()

    def get_active_signals(self) -> Dict[str, Dict]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = time.time()
        cursor.execute("SELECT * FROM synaptic_signals WHERE active = 1")
        rows = cursor.fetchall()
        active = {}
        to_deactivate = []
        for row in rows:
            if now - row["emitted_at"] > row["ttl_seconds"]:
                to_deactivate.append(row["signal_type"])
            else:
                active[row["signal_type"]] = {
                    "payload": json.loads(row["payload"]),
                    "emitted_at": row["emitted_at"],
                    "ttl_seconds": row["ttl_seconds"],
                    "evidentiality": row["evidentiality"]
                }
        
        if to_deactivate:
            placeholders = ', '.join(['?'] * len(to_deactivate))
            cursor.execute(f"UPDATE synaptic_signals SET active = 0 WHERE signal_type IN ({placeholders})", to_deactivate)
            conn.commit()
            
        conn.close()
        return active

    def log_signal_history(self, signal_type: str, payload: Dict, ttl_seconds: int, evidentiality: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO signal_history (signal_type, payload, timestamp, ttl_seconds, evidentiality)
            VALUES (?, ?, ?, ?, ?)
        """, (signal_type, json.dumps(payload), time.time(), ttl_seconds, evidentiality))
        conn.commit()
        conn.close()

    # --- Motor Operations ---

    def log_motor_action(self, action: str, target: str, success: bool, result: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO motor_log (timestamp, action, target, success, result)
            VALUES (?, ?, ?, ?, ?)
        """, (time.time(), action, target, 1 if success else 0, result))
        conn.commit()
        conn.close()

    def get_motor_log(self, limit: int = 100) -> List[Dict]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motor_log ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    # --- Routing Weights Operations ---

    def get_routing_weights(self) -> Dict[str, Dict]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routing_weights")
        rows = cursor.fetchall()
        weights = {}
        for row in rows:
            weights[row["signal_type"]] = {
                "to": row["to_role"],
                "priority": row["priority"],
                "action": row["action"],
                "success_count": row["success_count"],
                "failure_count": row["failure_count"]
            }
        conn.close()
        return weights

    def update_routing_stats(self, signal_type: str, success: bool):
        conn = self._get_connection()
        cursor = conn.cursor()
        field = "success_count" if success else "failure_count"
        cursor.execute(f"UPDATE routing_weights SET {field} = {field} + 1 WHERE signal_type = ?", (signal_type,))
        conn.commit()
        conn.close()

    def initialize_routing_weights(self, default_routing: Dict):
        conn = self._get_connection()
        cursor = conn.cursor()
        for sig, data in default_routing.items():
            cursor.execute("""
                INSERT OR IGNORE INTO routing_weights (signal_type, to_role, priority, action)
                VALUES (?, ?, ?, ?)
            """, (sig, data["to"], data["priority"], data["action"]))
        conn.commit()
        conn.close()

    # --- Immune Operations ---

    def upsert_antigen(self, antigen_id: str, antigen_type: str, details: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO immune_registry (antigen_id, type, details, detected_at)
            VALUES (?, ?, ?, ?)
        """, (antigen_id, antigen_type, details, time.time()))
        conn.commit()
        conn.close()

    def get_immune_registry(self) -> List[Dict]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM immune_registry")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    # --- Hive Lock Operations ---

    def acquire_hive_lock(self, lock_id: str, node_id: str, ttl_seconds: int = 60) -> bool:
        """Attempts to acquire a global hive lock."""
        conn = self._get_connection()
        cursor = conn.cursor()
        now = time.time()
        
        # Cleanup expired locks
        cursor.execute("DELETE FROM hive_locks WHERE expires_at < ?", (now,))
        
        try:
            cursor.execute("""
                INSERT INTO hive_locks (lock_id, holder_node, acquired_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (lock_id, node_id, now, now + ttl_seconds))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def release_hive_lock(self, lock_id: str, node_id: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hive_locks WHERE lock_id = ? AND holder_node = ?", (lock_id, node_id))
        conn.commit()
        conn.close()

    # --- Context Cache Operations ---

    def upsert_context_cache(self, cache_key: str, cache_id: str, ttl_seconds: int, content_hash: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO context_caches (cache_key, cache_id, expires_at, content_hash)
            VALUES (?, ?, ?, ?)
        """, (cache_key, cache_id, time.time() + ttl_seconds, content_hash))
        conn.commit()
        conn.close()

    def get_valid_cache_id(self, cache_key: str, current_hash: str) -> Optional[str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute("""
            SELECT cache_id FROM context_caches 
            WHERE cache_key = ? AND content_hash = ? AND expires_at > ?
        """, (cache_key, current_hash, now))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def prune_lattice_tasks(self, task_ids: List[str]) -> int:
        """Permanently removes specific tasks from the lattice (Synaptic Pruning)."""
        if not task_ids:
            return 0
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(task_ids))
        cursor.execute(f"DELETE FROM lattice_tasks WHERE task_id IN ({placeholders})", task_ids)
        count = cursor.rowcount
        conn.commit()
        conn.close()
        return count

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    mgr = StateManager(base)
    print(f"State Database initialized at {mgr.db_path}")
