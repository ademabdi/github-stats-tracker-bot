import os
import matplotlib.pyplot as plt
import pandas as pd

CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_charts")
os.makedirs(CHART_DIR, exist_ok=True)


def generate_star_trend_chart(df, owner, name):
    df = df.copy()
    df["captured_at"] = pd.to_datetime(df["captured_at"])

    plt.figure(figsize=(8, 4))
    plt.plot(df["captured_at"], df["stars"], marker="o")
    plt.title(f"{owner}/{name} — Star Growth")
    plt.xlabel("Date")
    plt.ylabel("Stars")
    plt.xticks(rotation=30)
    plt.tight_layout()

    chart_path = os.path.join(CHART_DIR, f"{owner}_{name}_trend.png")
    plt.savefig(chart_path)
    plt.close()

    return chart_path