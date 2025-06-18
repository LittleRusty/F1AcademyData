import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors


def parse_lap_time(lap_str):
    try:
        minutes, seconds = lap_str.split(":")
        return float(minutes) * 60 + float(seconds)
    except Exception:
        return None


def format_mmss(x, _):
    minutes = int(x // 60)
    seconds = x % 60
    return f"{minutes}:{seconds:06.3f}"


def format_hover(index, lap_times):
    total_sec = lap_times[int(index)]
    minutes = int(total_sec // 60)
    seconds = total_sec % 60
    return f"Lap {int(index)+1}\nTime: {minutes}:{seconds:06.3f}"


def plot_driver_laps(data, driver_short_name):
    seen_laps = set()
    lap_times = []

    for entry in data:
        if entry.get("driver_short_name") != driver_short_name:
            continue

        sector_key = (
            entry.get("sector1_time"),
            entry.get("sector2_time"),
            entry.get("sector3_time"),
        )
        if not all(sector_key) or "" in sector_key or sector_key in seen_laps:
            continue

        seen_laps.add(sector_key)

        lap_str = entry.get("latest_lap_time")
        if not lap_str:
            continue

        lap_time = parse_lap_time(lap_str)
        if lap_time is not None:
            lap_times.append(lap_time)

    if not lap_times:
        print(f"No valid lap times found for {driver_short_name}")
        return

    lap_indices = list(range(1, len(lap_times) + 1))

    # Plot as scatter
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(lap_indices, lap_times, c="dodgerblue", s=60)

    # Format Y-axis as mm:ss.xxx
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_mmss))
    plt.xlabel("Lap Count")
    plt.ylabel("Latest Lap Time")
    plt.title(f"Lap Time Trend for {driver_short_name}")
    plt.xticks(lap_indices)
    plt.grid(False)
    plt.tight_layout()

    # Enable hover
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.snap = True

    @cursor.connect("add")
    def on_add(sel):
        sel.annotation.set_text(format_hover(sel.index, lap_times))

    plt.show()


if __name__ == "__main__":
    with open("Montreal_2025/f1aData_FP1_2.jsonl", "r", encoding="utf-8") as f:
        lines = f.readlines()

    all_entries = []
    for line in lines:
        try:
            parsed = json.loads(line)
            if isinstance(parsed, list):
                all_entries.extend(parsed)
        except json.JSONDecodeError:
            continue

    plot_driver_laps(all_entries, driver_short_name="CHA")
