# GitHub Stats Tracker Bot

An end-to-end data pipeline that tracks GitHub repository metrics over time, with a Discord bot for querying current stats and historical trend charts on demand.

The pipeline extracts repo metrics from the GitHub REST API, models them into a dimensional schema in SQLite, and serves them through Discord slash commands.

## Features

- **ETL pipeline**: extracts stars, forks, open issues, and watcher counts for a configurable list of repos
- **Dimensional model**: a `dim_repo` dimension table plus a periodic-snapshot fact table (`fact_repo_snapshot`), so history accumulates instead of being overwritten
- **Discord bot** with slash commands:
  - `/stats owner name`: latest snapshot for a repo
  - `/trend owner name`: star growth over time, rendered as a matplotlib chart
- **Idempotent setup**: tables are created with `CREATE TABLE IF NOT EXISTS`, and repos are upserted into the dimension table

## Architecture

```
GitHub REST API
      |
      v
  extract.py  ->  transform.py  ->  load.py  ->  SQLite (dim_repo, fact_repo_snapshot)
                                                        |
                                                        v
                                         queries.py -> charts.py -> bot.py -> Discord
```

| Stage | File | Responsibility |
|-------|------|----------------|
| Extract | `etl/extract.py` | Calls the GitHub API and returns raw JSON |
| Transform | `etl/transform.py` | Shapes raw JSON into dimension and fact records |
| Load | `etl/load.py` | Upserts the repo into `dim_repo`, inserts a new snapshot row |
| Orchestrate | `etl/pipeline.py` | Loops over tracked repos and runs extract, transform, load |
| Query | `bot/queries.py` | Reads data from SQLite into DataFrames |
| Chart | `bot/charts.py` | Generates trend charts with matplotlib |
| Bot | `bot/bot.py` | Registers slash commands and wires queries and charts together |

## Data Model

```
dim_repo
  repo_id (PK)
  owner
  name
  created_at
  language
  UNIQUE(owner, name)

fact_repo_snapshot
  snapshot_id (PK)
  repo_id (FK -> dim_repo)
  captured_at
  stars
  forks
  open_issues
  watchers
```

Each pipeline run inserts one new row per repo into `fact_repo_snapshot`, which builds the time series used by `/trend`.

## Project Structure

```
github-stats-tracker-bot/
├── bot/
│   ├── bot.py
│   ├── queries.py
│   └── charts.py
├── db/
│   ├── db_init.py
│   └── github_view_db.py
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- A Discord bot token (see below)

### 1. Clone and install

```bash
git clone https://github.com/ademabdi/github-stats-tracker-bot.git
cd github-stats-tracker-bot
pip install -r requirements.txt
```

### 2. Create a Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab and click **Reset Token** to generate a token.
3. Under **OAuth2 > URL Generator**, select the scopes `bot` and `applications.commands`, plus the permissions `Send Messages` and `Attach Files`.
4. Open the generated URL to invite the bot to your server.

### 3. Configure environment variables

Create a `.env` file in the project root (it is gitignored, so never commit it):

```
DISCORD_BOT_TOKEN=your_token_here
```

### 4. Choose repos to track

Edit the `REPOS_TO_TRACK` list in `etl/pipeline.py`:

```python
REPOS_TO_TRACK = [
    ("karpathy", "nanoGPT"),
    ("pytorch", "pytorch"),
    ("huggingface", "transformers"),
    ("pandas-dev", "pandas"),
]
```

### 5. Run the pipeline

From the project root:

```bash
python -m etl.pipeline
```

Run it repeatedly, or on a schedule (cron or Windows Task Scheduler), to build up snapshot history.

### 6. Run the bot

In a separate terminal:

```bash
python bot/bot.py
```

When you see `Logged in as ...`, the `/stats` and `/trend` commands will appear in your Discord server.

### Inspecting the database

```bash
python db/github_view_db.py
```

## Notes

- Unauthenticated GitHub API requests are limited to 60 per hour. For larger repo lists, add a personal access token to raise the limit to 5,000 per hour.
- `/trend` needs at least two snapshots for a repo before it can draw a line.
- `db/github_stats.db` is gitignored and is created automatically by the pipeline.

## Tech Stack

Python, SQLite, `requests`, `pandas`, `matplotlib`, `discord.py`, `python-dotenv`

## Roadmap

- Automatic repo discovery for a user or org via the GitHub API
- Authenticated API requests for higher rate limits
- Scheduled pipeline runs
- Additional commands (`/compare`, `/leaderboard`)
- Data quality checks and tests
