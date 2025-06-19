import json
import matplotlib.pyplot as plt

plt.style.use("dark_background")
import pandas as pd
from pathlib import Path
from timple.timedelta import strftimedelta
from datetime import timedelta
from driver_info import DRIVERS  # Your own driver metadata dictionary

# This gives you the parent directory of the script you're running
base_dir = Path(__file__).resolve().parent

"""
This file is largely based off the qualifying delta file from fastf1.  Source: https://docs.fastf1.dev/gen_modules/examples_gallery/plot_qualifying_results.html#sphx-glr-gen-modules-examples-gallery-plot-qualifying-results-py
"""


def parse_time(ts):
    """Convert a lap time string to timedelta."""
    if not ts:
        return None
    try:
        if ":" in ts:
            m, s = ts.split(":")
            return timedelta(minutes=int(m), seconds=float(s))
        return timedelta(seconds=float(ts))
    except Exception:
        return None


def load_last_snapshot(filepath):
    """Load the final telemetry snapshot from a JSONL file."""
    with open(filepath, "rb") as f:
        f.seek(-2, 2)  # Move to just before EOF
        while f.read(1) != b"\n":
            f.seek(-2, 1)
        last_line = f.readline().decode("utf-8")

    return json.loads(last_line)


def extract_fastest_laps(latest_snapshot):
    """Extract best_lap from a single snapshot for all drivers."""
    laps = []
    for entry in latest_snapshot:
        code = entry.get("driver_short_name")
        lap_str = entry.get("best_lap")
        lap_time = parse_time(lap_str)
        if code and lap_time:
            laps.append({"code": code, "lap_time": lap_time, "display": lap_str})
    return laps


def plot_qualifying_deltas(fastest_laps):
    """Plot horizontal bar chart of lap time deltas."""
    df = pd.DataFrame(fastest_laps)
    df = df.sort_values("lap_time").reset_index(drop=True)

    pole_time = df.loc[0, "lap_time"]
    df["delta"] = df["lap_time"] - pole_time
    df["delta_str"] = df["delta"].apply(lambda td: f"+{td.total_seconds():.3f}")

    # Colors and labels
    df["color"] = df["code"].apply(lambda c: DRIVERS.get(c, {}).get("color", "#888"))
    df["label"] = df["code"]

    fig, ax = plt.subplots(figsize=(8, len(df) * 0.5 + 1))
    ax.barh(
        df.index, df["delta"].dt.total_seconds(), color=df["color"], edgecolor="grey"
    )
    # Add labels next to each bar
    for idx, row in df.iterrows():
        delta_sec = row["delta"].total_seconds()
        label = row["delta_str"]
        ax.text(
            delta_sec + 0.05,
            idx,
            label,
            va="center",
            ha="left",
            fontsize=10,
            color="white",
        )
    ax.set_yticks(df.index)
    ax.set_yticklabels(df["label"])
    ax.invert_yaxis()
    ax.set_xlabel("Delta to Pole (s)")
    ax.set_title(
        f"Qualifying Deltas (Pole: {df.loc[0, 'code']} - {df.loc[0, 'display']})"
    )
    # ax.grid(True, axis="x", linestyle="--", color="black", zorder=-1000)
    # Remove top and right borders (spines)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.show()


def main():
    filepath = base_dir.parent / "Montreal_2025" / "f1aData_qualifying_montreal.jsonl"
    snapshot = load_last_snapshot(filepath)
    laps = extract_fastest_laps(snapshot)
    plot_qualifying_deltas(laps)


if __name__ == "__main__":
    main()
