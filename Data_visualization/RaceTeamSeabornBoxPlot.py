"""Team Pace Comparison
=============================================
Rank team's race pace from the fastest to the slowest.
This code is largely inspired by the team race comparison from FastF1. Source: https://docs.fastf1.dev/gen_modules/examples_gallery/plot_team_pace_ranking.html#sphx-glr-gen-modules-examples-gallery-plot-team-pace-ranking-py
"""

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

from driver_info import DRIVERS, TEAMS  # Make sure this exists and is importable

base_dir = Path(__file__).resolve().parent


def parse_time(s):
    """Convert a lap time string into float seconds, or return None if invalid."""
    if not s:
        return None
    try:
        if ":" in s:
            m, rest = s.split(":")
            return float(m) * 60 + float(rest)
        return float(s)
    except Exception:
        return None


def load_unique_laps(filepath):
    """Load all race laps, removing repeated consecutive entries per driver."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        try:
            row = json.loads(line)
            if isinstance(row, list):
                entries.extend(row)
        except json.JSONDecodeError:
            continue

    cleaned = []
    last_seen = {}
    for entry in entries:
        code = entry.get("driver_short_name")
        lap_str = entry.get("latest_lap_time")
        if not code or not lap_str:
            continue
        if last_seen.get(code) != lap_str:
            last_seen[code] = lap_str
            cleaned.append(entry)
    return cleaned


def build_dataframe(entries):
    """Build a dataframe of driver/team/laptime from cleaned entries."""
    rows = []
    for e in entries:
        code = e.get("driver_short_name")
        lap_str = e.get("latest_lap_time")
        lap_time = parse_time(lap_str)
        if not code or lap_time is None:
            continue
        team = DRIVERS.get(code, {}).get("team", "Unknown")
        rows.append({"Driver": code, "Team": team, "LapTime (s)": lap_time})
    return pd.DataFrame(rows)


def plot_team_pace(df, title="Team Race Pace - Race 2 (Median Lap Time)"):
    """Plot a dark-mode seaborn boxplot of team pace from the lap dataframe."""
    sns.set_theme(style="darkgrid")
    plt.style.use("dark_background")

    # Team ranking by median pace
    team_order = df.groupby("Team")["LapTime (s)"].median().sort_values().index

    team_palette = {
        team: TEAMS.get(team, {}).get("color", "#999") for team in team_order
    }

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.boxplot(
        data=df,
        x="Team",
        y="LapTime (s)",
        hue="Team",
        order=team_order,
        palette=team_palette,
        dodge=False,
        whiskerprops={"color": "white"},
        boxprops={"edgecolor": "white"},
        medianprops={"color": "grey"},
        capprops={"color": "white"},
    )

    # Clean up axes
    ax.set_title(title, fontsize=14)
    ax.set(xlabel=None)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    # Set custom y-axis limits with a little padding
    min_time = df["LapTime (s)"].min()
    max_time = df["LapTime (s)"].max()
    ax.set_ylim(97, 106)  # Add padding for clarity
    plt.tight_layout()
    plt.show()


def main():
    path = (
        base_dir.parent / "Montreal_2025" / "f1aData_Race2_montreal_2025.jsonl"
    )  # Adjust as needed
    entries = load_unique_laps(path)
    df = build_dataframe(entries)
    if df.empty:
        print("No valid lap times found.")
    else:
        plot_team_pace(df)


if __name__ == "__main__":
    main()
