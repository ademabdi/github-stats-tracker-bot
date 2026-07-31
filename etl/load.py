import sqlite3
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# up from etl/ to project root
DB_PATH = os.path.join(BASE_DIR, "db", "github_stats.db")

def load_repo_data(dim_record, fact_record, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Upsert into dim_repo (insert if not exists)
    cur.execute("""
        INSERT INTO dim_repo (owner, name, created_at, language)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(owner, name) DO NOTHING
    """, (dim_record["owner"], dim_record["name"], dim_record["created_at"], dim_record["language"]))

    # Look up repo_id
    cur.execute("SELECT repo_id FROM dim_repo WHERE owner = ? AND name = ?",
                (dim_record["owner"], dim_record["name"]))
    repo_id = cur.fetchone()[0]

    # Always insert new snapshot row
    cur.execute("""
        INSERT INTO fact_repo_snapshot (repo_id, captured_at, stars, forks, open_issues, watchers)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (repo_id, fact_record["captured_at"], fact_record["stars"],
          fact_record["forks"], fact_record["open_issues"], fact_record["watchers"]))

    conn.commit()
    conn.close()