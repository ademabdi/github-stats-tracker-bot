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

def get_latest_snapshot(owner,name):
    df = get_latest_snapshots()
    df_snapshot = df[(df["owner"] == owner) & (df["name"] == name)]
    return df_snapshot

def get_repo_history(owner,name):
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT f.captured_at, f.stars, f.forks, f.open_issues
        FROM fact_repo_snapshot f
        JOIN dim_repo d ON f.repo_id = d.repo_id
        WHERE d.owner = ? AND d.name = ?
        ORDER BY f.captured_at ASC
    """
    df = pd.read_sql_query(query, conn, params=(owner, name))
    conn.close()
    return df



