from datetime import datetime, timezone

def transform_repo_record(raw_json):
    dim_record = {
        "owner": raw_json["owner"]["login"],
        "name": raw_json["name"],
        "created_at": raw_json["created_at"],
        "language": raw_json["language"]
    }

    fact_record = {
        "repo_name": raw_json["full_name"],
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "stars": raw_json["stargazers_count"],
        "forks": raw_json["forks_count"],
        "open_issues": raw_json["open_issues_count"],
        "watchers": raw_json["watchers_count"]
    }


    return dim_record, fact_record