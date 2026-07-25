import sys
import os
import sqlite3
from pathlib import Path
from typing import Dict, Optional

try:
    import psycopg2
except ImportError:
    psycopg2 = None

"""
import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
"""


class DatabaseReceptor:
    """SQL query executor (SQLite for local, PostgreSQL via env)."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.pg_dsn = os.environ.get("DATABASE_URL")  # postgresql://user:pass@host/db
        self.sqlite_path = base_dir / "core" / "exports" / "Sesha_aos.db"

    def _get_sqlite_conn(self):
        return sqlite3.connect(self.sqlite_path)

    def query(self, sql: str, params: tuple = None, use_pg: bool = False) -> Dict:
        """Execute a SELECT query."""
        if use_pg and self.pg_dsn:
            try:
                import psycopg2
                conn = psycopg2.connect(self.pg_dsn)
            except ImportError:
                return {"success": False, "error": "psycopg2 not installed"}
        else:
            conn = self._get_sqlite_conn()

        try:
            cur = conn.cursor()
            cur.execute(sql, params or ())
            if cur.description:
                columns = [d[0] for d in cur.description]
                rows = [dict(zip(columns, row)) for row in cur.fetchall()]
                return {"success": True, "columns": columns, "rows": rows, "rowcount": len(rows)}
            return {"success": True, "rowcount": cur.rowcount}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def execute(self, sql: str, params: tuple = None, use_pg: bool = False) -> Dict:
        """Execute INSERT/UPDATE/DELETE."""
        if use_pg and self.pg_dsn:
            try:
                conn = psycopg2.connect(self.pg_dsn)
            except ImportError:
                return {"success": False, "error": "psycopg2 not installed"}
        else:
            conn = self._get_sqlite_conn()

        try:
            cur = conn.cursor()
            cur.execute(sql, params or ())
            conn.commit()
            return {"success": True, "rowcount": cur.rowcount}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
