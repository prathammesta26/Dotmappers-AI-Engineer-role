import sqlite3
import pandas as pd
from pathlib import Path

# Anchors the paths to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "support_tickets.db"
CSV_FILE = BASE_DIR / "support_tickets.csv"

def init_db():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Cannot find CSV at {CSV_FILE}")
    df = pd.read_csv(CSV_FILE)
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("tickets", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def run_query(sql_query: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows, None
    except Exception as e:
        conn.close()
        return None, str(e)