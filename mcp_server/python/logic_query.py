import sqlite3
import json
import sys
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "core", "exports", "nexus_aos.db")

def query_db(sql: str):
    """Executes a SQL query against the Logic Graph and returns results as JSON."""
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Return as dicts
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        results = [dict(row) for row in rows]
        print(json.dumps(results, indent=2))
        conn.close()
    except Exception as e:
        print(f"SQL Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python logic_query.py \"SELECT ...\"")
    else:
        query_db(sys.argv[1])
