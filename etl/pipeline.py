import time
import os
from etl.extract import extract_from_github
from etl.load import load_repo_data
from etl.transform import transform_repo_record
from db.db_init import create_tables

REPOS_TO_TRACK = [
    ("karpathy", "nanoGPT"),
    ("pytorch", "pytorch"),
    ("huggingface", "transformers"),
    ("pandas-dev", "pandas"),
]


def run_pipeline():
    create_tables()

    for owner, repo in REPOS_TO_TRACK:
        print(f"Processing from {owner}/{repo}")

        raw_json = extract_from_github(owner, repo)
        if raw_json is None:
            print(f"No data to track from {owner}/{repo}")
            continue

        dim_record, fact_record = transform_repo_record(raw_json)
        load_repo_data(dim_record, fact_record)

        print(f"Loaded snapshot: {fact_record['stars']} stars")

        time.sleep(1)


if __name__ == "__main__":
    run_pipeline()