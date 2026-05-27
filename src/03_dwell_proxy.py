from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _pipeline_utils import ensure_project_folders, print_output_paths, project_root, summary_by_group


MAX_DWELL_MINUTES = 1440


def require_cleaned_data(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Cleaned Divvy data not found. Run src/01_combine_and_clean.py first: {path}")


def valid_station_mask(series: pd.Series) -> pd.Series:
    station_id = series.astype("string").str.strip()
    return station_id.notna() & station_id.ne("")


def build_station_events(df: pd.DataFrame) -> pd.DataFrame:
    arrivals = df.loc[valid_station_mask(df["end_station_id"])].copy()
    arrivals = arrivals.rename(
        columns={
            "end_station_id": "station_id",
            "end_station_name": "station_name",
            "ended_at": "event_time",
        }
    )
    arrivals = arrivals[["station_id", "station_name", "event_time"]]
    arrivals["event_type"] = "arrival"
    arrivals["event_order"] = 0

    departures = df.loc[valid_station_mask(df["start_station_id"])].copy()
    departures = departures.rename(
        columns={
            "start_station_id": "station_id",
            "start_station_name": "station_name",
            "started_at": "event_time",
        }
    )
    departures = departures[["station_id", "station_name", "event_time"]]
    departures["event_type"] = "departure"
    departures["event_order"] = 1

    events = pd.concat([arrivals, departures], ignore_index=True)
    events["station_id"] = events["station_id"].astype("string").str.strip()
    events["event_time"] = pd.to_datetime(events["event_time"], errors="coerce")
    events = events.dropna(subset=["station_id", "event_time"])
    return events


def calculate_dwell_proxy(events: pd.DataFrame) -> pd.DataFrame:
    # This is station-level idle/availability time, not bike-level dwell time.
    # The public Divvy trip files do not include bike_id.
    if events.empty:
        return pd.DataFrame(
            columns=[
                "station_id",
                "station_name",
                "arrival_time",
                "departure_time",
                "dwell_time_minutes",
                "day_type",
                "date",
            ]
        )

    events = events.sort_values(["station_id", "event_time", "event_order"]).reset_index(drop=True)
    departure_time = events["event_time"].where(events["event_type"].eq("departure"))
    events["next_departure_time"] = departure_time.groupby(events["station_id"]).bfill()

    dwell = events.loc[events["event_type"].eq("arrival")].copy()
    dwell = dwell.rename(columns={"event_time": "arrival_time"})
    dwell["departure_time"] = dwell["next_departure_time"]
    dwell = dwell.dropna(subset=["departure_time"])
    dwell["dwell_time_minutes"] = (
        dwell["departure_time"] - dwell["arrival_time"]
    ).dt.total_seconds() / 60.0
    dwell = dwell.loc[
        dwell["dwell_time_minutes"].gt(0) & dwell["dwell_time_minutes"].le(MAX_DWELL_MINUTES)
    ].copy()

    dwell["day_type"] = np.where(dwell["arrival_time"].dt.dayofweek < 5, "weekday", "weekend")
    dwell["date"] = dwell["arrival_time"].dt.date.astype(str)
    return dwell[
        [
            "station_id",
            "station_name",
            "arrival_time",
            "departure_time",
            "dwell_time_minutes",
            "day_type",
            "date",
        ]
    ]


def write_dwell_summary(dwell: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    if dwell.empty:
        summary = pd.DataFrame(columns=["day_type", "count", "mean", "median", "q1", "q3"])
    else:
        summary = summary_by_group(dwell, "day_type", "dwell_time_minutes")
        summary = summary[["day_type", "count", "mean", "median", "q1", "q3"]]
    summary.to_csv(output_path, index=False)
    return summary


def plot_dwell_boxplot(dwell: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    if dwell.empty:
        ax.text(0.5, 0.5, "No dwell proxy records available", ha="center", va="center")
        ax.set_axis_off()
    else:
        day_types = [day_type for day_type in ["weekday", "weekend"] if day_type in set(dwell["day_type"])]
        plot_data = [dwell.loc[dwell["day_type"] == day_type, "dwell_time_minutes"] for day_type in day_types]
        upper_limit = dwell["dwell_time_minutes"].quantile(0.99)
        box = ax.boxplot(plot_data, tick_labels=day_types, showfliers=False, patch_artist=True)
        for patch, color in zip(box["boxes"], ["#4C78A8", "#F58518"]):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
        ax.set_title("Station-level Dwell Time Proxy by Day Type")
        ax.set_xlabel("Day type based on arrival time")
        ax.set_ylabel("Dwell time proxy (minutes)")
        ax.set_ylim(bottom=0, top=upper_limit * 1.08)
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def main() -> None:
    root = project_root()
    ensure_project_folders(root)

    cleaned_path = root / "data" / "processed" / "divvy_2025_cleaned.csv"
    require_cleaned_data(cleaned_path)

    df = pd.read_csv(
        cleaned_path,
        usecols=[
            "started_at",
            "ended_at",
            "start_station_id",
            "start_station_name",
            "end_station_id",
            "end_station_name",
        ],
    )

    events = build_station_events(df)
    dwell = calculate_dwell_proxy(events)

    dwell_path = root / "data" / "processed" / "dwell_proxy_2025.csv"
    summary_path = root / "outputs" / "dwell_proxy_summary_by_day_type.csv"
    plot_path = root / "figures" / "dwell_proxy_boxplot.png"

    dwell.to_csv(dwell_path, index=False)
    write_dwell_summary(dwell, summary_path)
    plot_dwell_boxplot(dwell, plot_path)

    print_output_paths([dwell_path, summary_path, plot_path])


if __name__ == "__main__":
    main()
