import calendar
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from _pipeline_utils import ensure_project_folders, print_output_paths, project_root, summary_by_group


DAY_TYPE_ORDER = ["weekday", "weekend"]


def require_cleaned_data(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Cleaned Divvy data not found. Run src/01_combine_and_clean.py first: {path}")


def ordered_day_types(df: pd.DataFrame) -> list[str]:
    return [day_type for day_type in DAY_TYPE_ORDER if day_type in set(df["day_type"].dropna())]


def save_weekday_weekend_counts(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    counts = df.groupby("day_type").size().reindex(DAY_TYPE_ORDER, fill_value=0).reset_index()
    counts.columns = ["day_type", "trip_count"]
    counts["share"] = counts["trip_count"] / counts["trip_count"].sum()
    counts.to_csv(output_path, index=False)
    return counts


def save_monthly_counts(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    monthly = df.groupby(["month", "day_type"]).size().reset_index(name="trip_count")
    monthly["month_name"] = monthly["month"].map(lambda value: calendar.month_abbr[int(value)])
    monthly = monthly[["month", "month_name", "day_type", "trip_count"]]
    monthly.to_csv(output_path, index=False)
    return monthly


def save_trip_summary(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    duration_summary = summary_by_group(df, "day_type", "trip_duration_minutes")
    duration_summary.insert(0, "metric", "trip_duration_minutes")

    length_summary = summary_by_group(df, "day_type", "trip_length_km")
    length_summary.insert(0, "metric", "trip_length_km")

    summary = pd.concat([duration_summary, length_summary], ignore_index=True)
    summary.to_csv(output_path, index=False)
    return summary


def plot_boxplot(df: pd.DataFrame, value_column: str, title: str, ylabel: str, output_path: Path) -> None:
    day_types = ordered_day_types(df)
    if not day_types:
        raise ValueError("No day_type values available for plotting.")

    plot_data = [df.loc[df["day_type"] == day_type, value_column].dropna() for day_type in day_types]
    upper_limit = df[value_column].quantile(0.99)
    if pd.isna(upper_limit) or upper_limit <= 0:
        upper_limit = df[value_column].max()

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    box = ax.boxplot(plot_data, tick_labels=day_types, showfliers=False, patch_artist=True)
    for patch, color in zip(box["boxes"], ["#4C78A8", "#F58518"]):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    ax.set_title(title)
    ax.set_xlabel("Day type")
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0, top=upper_limit * 1.08)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def plot_monthly_counts(monthly: pd.DataFrame, output_path: Path) -> None:
    pivot = monthly.pivot_table(
        index="month",
        columns="day_type",
        values="trip_count",
        aggfunc="sum",
        fill_value=0,
    ).reindex(range(1, 13), fill_value=0)

    x = range(len(pivot.index))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8.5, 4.4))

    weekday = pivot["weekday"] if "weekday" in pivot else [0] * len(pivot)
    weekend = pivot["weekend"] if "weekend" in pivot else [0] * len(pivot)
    ax.bar([value - width / 2 for value in x], weekday, width=width, label="Weekday", color="#4C78A8")
    ax.bar([value + width / 2 for value in x], weekend, width=width, label="Weekend", color="#F58518")

    ax.set_title("Monthly Trip Counts by Day Type")
    ax.set_xlabel("Month")
    ax.set_ylabel("Trip count")
    ax.set_xticks(list(x))
    ax.set_xticklabels([calendar.month_abbr[month] for month in pivot.index])
    ax.legend(frameon=False)
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
        usecols=["day_type", "month", "trip_duration_minutes", "trip_length_km"],
    )

    weekday_counts_path = root / "outputs" / "weekday_weekend_counts.csv"
    monthly_counts_path = root / "outputs" / "monthly_counts_by_day_type.csv"
    trip_summary_path = root / "outputs" / "trip_summary_by_day_type.csv"
    length_plot_path = root / "figures" / "trip_length_boxplot.png"
    duration_plot_path = root / "figures" / "trip_duration_boxplot.png"
    monthly_plot_path = root / "figures" / "monthly_trip_counts_by_day_type.png"

    save_weekday_weekend_counts(df, weekday_counts_path)
    monthly = save_monthly_counts(df, monthly_counts_path)
    save_trip_summary(df, trip_summary_path)
    plot_boxplot(
        df,
        "trip_length_km",
        "Trip Length by Day Type",
        "Straight-line trip length (km)",
        length_plot_path,
    )
    plot_boxplot(
        df,
        "trip_duration_minutes",
        "Trip Duration by Day Type",
        "Trip duration (minutes)",
        duration_plot_path,
    )
    plot_monthly_counts(monthly, monthly_plot_path)

    print_output_paths(
        [
            weekday_counts_path,
            monthly_counts_path,
            trip_summary_path,
            length_plot_path,
            duration_plot_path,
            monthly_plot_path,
        ]
    )


if __name__ == "__main__":
    main()
