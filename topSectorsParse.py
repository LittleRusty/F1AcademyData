import json
from collections import defaultdict
from operator import itemgetter
from pathlib import Path
from driver_info import DRIVERS
import Utils
import argparse


def parse_args():
    """Parses out command line arguments.  Currently just takes in path to JSONL file with session data.

    Returns:
        Parser Arguments: Array of optional parser arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate sector leaderboards from telemetry data."
    )
    parser.add_argument(
        "input_file", type=str, help="Path to the JSON Lines input file"
    )
    # TODO: Implment variable number of drivers
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Limit number of drivers in top sectors (default: 10)",
    )
    # TODO: Implement session argument and move away from file name parsing to determine session type
    parser.add_argument(
        "--session",
        type=str,
        choices=["FP1", "FP2", "Q", "R"],
        help="Filter by session type",
    )
    return parser.parse_args()


def parse_time(time_str):
    """_summary_

    Args:
        time_str (string): _description_

    Returns:
        _type_: _description_
    """
    if not time_str:
        return None
    try:
        if ":" in time_str:
            m, s = time_str.split(":")
            return float(m) * 60 + float(s)
        return float(time_str)
    except:
        return None


def load_jsonl(filepath):
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                items = json.loads(line)
                if isinstance(items, list):
                    entries.extend(items)
            except json.JSONDecodeError:
                continue
    return entries


def get_top_sector_times(entries, sector_key):
    best = {}
    for entry in entries:
        d = entry.get("driver_short_name")
        s = entry.get(sector_key)
        t = parse_time(s)
        if not d or t is None:
            continue
        if d not in best or t < best[d]["time"]:
            best[d] = {"driver": d, "display": s, "time": t}
    return sorted(best.values(), key=itemgetter("time"))[:10]


def get_top_combined_drivers(entries):
    # Union of top 10 drivers across all sectors
    top_s1 = get_top_sector_times(entries, "sector1_time")
    top_s2 = get_top_sector_times(entries, "sector2_time")
    top_s3 = get_top_sector_times(entries, "sector3_time")
    unique_drivers = {e["driver"] for e in top_s1 + top_s2 + top_s3}

    def get_best(driver, sector_key):
        times = [
            parse_time(e.get(sector_key))
            for e in entries
            if e.get("driver_short_name") == driver
            and parse_time(e.get(sector_key)) is not None
        ]
        return min(times) if times else None

    table_data = []
    for code in unique_drivers:
        d = DRIVERS.get(code, {})
        name = d.get("full_name", code).split()[-1]
        color = d.get("color", "#888")
        row = {
            "driver": code,
            "last_name": name,
            "color": color,
            "s1": get_best(code, "sector1_time"),
            "s2": get_best(code, "sector2_time"),
            "s3": get_best(code, "sector3_time"),
        }
        table_data.append(row)

    return sorted(
        table_data,
        key=lambda x: min(t for t in (x["s1"], x["s2"], x["s3"]) if t is not None),
    )[:10]


def get_best_sectors_by_driver(entries):
    best = defaultdict(
        lambda: {"sector1_time": None, "sector2_time": None, "sector3_time": None}
    )
    for entry in entries:
        code = entry.get("driver_short_name")
        for key in ("sector1_time", "sector2_time", "sector3_time"):
            val = parse_time(entry.get(key))
            if val is None:
                continue
            existing = best[code][key]
            if existing is None or val < parse_time(existing):
                best[code][key] = entry.get(key)
    return best


def generate_horizontal_sector_table(s1_top, s2_top, s3_top):
    html = ["<table>"]
    html.append(
        "<tr><th>Pos</th><th class='driver-col'>Driver S1</th><th>Time S1</th>"
        "<th class='driver-col'>Driver S2</th><th>Time S2</th>"
        "<th class='driver-col'>Driver S3</th><th>Time S3</th></tr>"
    )

    for i in range(10):
        row = []
        for sector_top in (s1_top, s2_top, s3_top):
            if i < len(sector_top):
                code = sector_top[i]["driver"]
                data = DRIVERS.get(code, {})
                name = data.get("full_name", code).split()[-1]
                color = data.get("color", "#999")
                time = sector_top[i]["display"]
                luminance = Utils.calculate_luminance(color)
                textColor = "black" if luminance > 128 else "white"
                row.append(
                    f"<td class='driver-cell' style='color: {textColor};background-color:{color}'>{name}</td><td class='time-cell'>{time}</td>"
                )
            else:
                row.append(
                    "<td class='driver-cell' style='background-color:#444'>-</td><td>-</td>"
                )

        html.append(f"<tr class='pos-cell'><td>{i+1}</td>{''.join(row)}</tr>")

    html.append("</table>")
    return "\n".join(html)


def generate_driver_sector_table(driver_data):
    lines = [
        "<table>",
        "<tr><th class='driver-col'>Driver</th><th>Sector 1</th><th>Sector 2</th><th>Sector 3</th></tr>",
    ]
    for code in sorted(driver_data):
        d = DRIVERS.get(code, {})
        name = d.get("full_name", code).split()[-1]
        color = d.get("color", "#777")
        cell = f"<span class='driver' style='background-color:{color}'>{name}</span>"
        s1 = driver_data[code]["sector1_time"] or "-"
        s2 = driver_data[code]["sector2_time"] or "-"
        s3 = driver_data[code]["sector3_time"] or "-"
        lines.append(
            f"<tr><td class='driver-col'>{cell}</td><td>{s1}</td><td>{s2}</td><td>{s3}</td></tr>"
        )
    lines.append("</table>")
    return "\n".join(lines)


def build_html(top_s1, top_s2, top_s3):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unified Sector Leaderboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h2>Free Practice Top 10 Sector Times</h2>
    {generate_horizontal_sector_table(top_s1, top_s2, top_s3)}
</body>
</html>"""


def main():
    args = parse_args()
    data = load_jsonl(args.input_file)
    combined_rows = get_top_combined_drivers(data)
    driver_best = get_best_sectors_by_driver(data)
    top_s1 = get_top_sector_times(data, "sector1_time")
    top_s2 = get_top_sector_times(data, "sector2_time")
    top_s3 = get_top_sector_times(data, "sector3_time")
    html = build_html(top_s1, top_s2, top_s3)
    Path("sector_leaderboard.html").write_text(html, encoding="utf-8")
    print("✅ Leaderboard saved to sector_leaderboard.html")


if __name__ == "__main__":
    main()
