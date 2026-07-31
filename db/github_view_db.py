import sqlite3
import pandas as pd

conn = sqlite3.connect("github_stats.db")

dim_df = pd.read_sql_query("SELECT * FROM dim_repo", conn)
fact_df = pd.read_sql_query("SELECT * FROM fact_repo_snapshot", conn)

print(dim_df)
print(fact_df)

conn.close()