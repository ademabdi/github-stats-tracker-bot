import sqlite3
import os

def create_tables():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "db", "github_stats.db")

    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_repo (
            repo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT,
            language TEXT,
            UNIQUE(owner, name)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fact_repo_snapshot (
            snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_id INTEGER NOT NULL,
            captured_at TEXT NOT NULL,
            stars INTEGER,
            forks INTEGER,
            open_issues INTEGER,
            watchers INTEGER,
            FOREIGN KEY (repo_id) REFERENCES dim_repo(repo_id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Tables created at {DB_PATH}")

if __name__ == "__main__":
    create_tables()