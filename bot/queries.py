#extract data from sqlite db

import os
import time 
import sqlite3
import pandas as pd


BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "github_stats.db")

def get_latest_snapshots():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT d.owner, d.name, s.captured_at, s.stars, s.forks, s.open_issues, s.watchers
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY repo_id ORDER BY captured_at DESC) AS rn
            FROM fact_repo_snapshot
        ) s
        JOIN dim_repo d ON s.repo_id = d.repo_id
        WHERE s.rn = 1
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df