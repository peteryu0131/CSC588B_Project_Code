from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd

from _pipeline_utils import ensure_project_folders, print_output_paths, project_root


MAX_HEATMAP_ROWS = 300_000
HEATMAP_BINS = 220


def require_cleaned_data(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Cleaned Divvy data not found. Run src/01_combine_and_clean.py first: {path}")


def sample_for_heatmap(df: pd.DataFrame, max_rows: int = MAX_HEATMAP_ROWS) -> pd.DataFrame:
    day_types = [day_type for day_type in ["weekday", "weekend"] if day_type in set(df["day_type"])]
    if not day_types or len(df) <= max_rows:
        return df

    per_day_type = max_rows // len(day_types)
    samples = []
    for day_type in day_types:
        group = df.loc[df["day_type"] == day_type]
        samples.append(group.sample(n=min(len(group), per_day_type), random_state=42))
    return pd.concat(samples, ignore_index=True)


def coordinate_range(df: pd.DataFrame) -> list[list[float]]:
    lng_min, lng_max = df["start_lng"].quantile([0.005, 0.995])
    lat_min, lat_max = df["start_lat"].quantile([0.005, 0.995])

    if lng_min == lng_max:
        lng_min -= 0.01
        lng_max += 0.01
    if lat_min == lat_max:
        lat_min -= 0.01
        lat_max += 0.01

    return [[lng_min, lng_max], [lat_min, lat_max]]


def draw_heatmap(ax: plt.Axes, df: pd.DataFrame, title: str, plot_range: list[list[float]]) -> None:
    if df.empty:
        ax.text(0.5, 0.5, "No records available", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        return

    image = ax.hist2d(
        df["start_lng"],
        df["start_lat"],
        bins=HEATMAP_BINS,
        range=plot_range,
        cmap="viridis",
        norm=LogNorm(),
    )
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal", adjustable="box")
    return image


def plot_weekday_weekend_heatmap(df: pd.DataFrame, output_path: Path) -> None:
    plot_range = coordinate_range(df)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), sharex=True, sharey=True)
    weekday_image = draw_heatmap(
        axes[0],
        df.loc[df["day_type"] == "weekday"],
        "Weekday Start-location Density",
        plot_range,
    )
    weekend_image = draw_heatmap(
        axes[1],
        df.loc[df["day_type"] == "weekend"],
        "Weekend Start-location Density",
        plot_range,
    )
    image = weekday_image if weekday_image is not None else weekend_image
    if image is not None:
        fig.colorbar(image[3], ax=axes, shrink=0.86, label="Trip starts per bin")
    fig.suptitle("Weekday vs Weekend Divvy Start Locations", y=0.98)
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_overall_heatmap(df: pd.DataFrame, output_path: Path) -> None:
    plot_range = coordinate_range(df)
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    image = draw_heatmap(ax, df, "Overall Start-location Density", plot_range)
    if image is not None:
        fig.colorbar(image[3], ax=ax, shrink=0.86, label="Trip starts per bin")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def main() -> None:
    root = project_root()
    ensure_project_folders(root)

    cleaned_path = root / "data" / "processed" / "divvy_2025_cleaned.csv"
    require_cleaned_data(cleaned_path)

    df = pd.read_csv(cleaned_path, usecols=["day_type", "start_lat", "start_lng"])
    df = df.dropna(subset=["day_type", "start_lat", "start_lng"])
    df = sample_for_heatmap(df)

    side_by_side_path = root / "figures" / "heatmap_start_locations_weekday_weekend.png"
    overall_path = root / "figures" / "heatmap_start_locations_overall.png"

    plot_weekday_weekend_heatmap(df, side_by_side_path)
    plot_overall_heatmap(df, overall_path)

    print_output_paths([side_by_side_path, overall_path])


if __name__ == "__main__":
    main()
