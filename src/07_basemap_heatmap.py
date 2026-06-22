from pathlib import Path

import pandas as pd
import folium
from folium.plugins import HeatMap


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "divvy_2025_cleaned.csv"
FIGURES = ROOT / "figures"

FIGURES.mkdir(exist_ok=True)


def load_start_locations():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing cleaned data file: {DATA_PATH}\n"
            "Run python src\\01_combine_and_clean.py first."
        )

    columns = pd.read_csv(DATA_PATH, nrows=5).columns.tolist()
    print("Available columns:")
    print(columns)

    required = ["day_type", "start_lat", "start_lng"]
    missing = [col for col in required if col not in columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = pd.read_csv(DATA_PATH, usecols=required)

    df = df[
        df["day_type"].isin(["weekday", "weekend"])
        & df["start_lat"].between(41.5, 42.2)
        & df["start_lng"].between(-88.0, -87.3)
    ].copy()

    df = df.dropna(subset=["start_lat", "start_lng"])

    return df


def sample_equal_groups(df, max_per_group=120_000):
    sampled = []

    for day_type in ["weekday", "weekend"]:
        group = df[df["day_type"] == day_type]
        n = min(len(group), max_per_group)
        sampled.append(group.sample(n=n, random_state=42))

    return pd.concat(sampled, ignore_index=True)


def create_basemap_heatmap(df):
    chicago_center = [41.8781, -87.6298]

    m = folium.Map(
        location=chicago_center,
        zoom_start=12,
        tiles="CartoDB positron",
        control_scale=True,
    )

    weekday = df[df["day_type"] == "weekday"]
    weekend = df[df["day_type"] == "weekend"]

    weekday_points = weekday[["start_lat", "start_lng"]].values.tolist()
    weekend_points = weekend[["start_lat", "start_lng"]].values.tolist()

    weekday_layer = folium.FeatureGroup(name="Weekday start-location heatmap", show=True)
    weekend_layer = folium.FeatureGroup(name="Weekend start-location heatmap", show=False)

    HeatMap(
        weekday_points,
        radius=9,
        blur=13,
        min_opacity=0.25,
    ).add_to(weekday_layer)

    HeatMap(
        weekend_points,
        radius=9,
        blur=13,
        min_opacity=0.25,
    ).add_to(weekend_layer)

    weekday_layer.add_to(m)
    weekend_layer.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    title_html = """
    <div style="
        position: fixed;
        top: 10px;
        left: 50px;
        z-index: 9999;
        background-color: white;
        padding: 10px;
        border: 1px solid gray;
        font-size: 16px;
        font-family: Arial;
    ">
    <b>Divvy 2025 Start-Location Heatmap with Basemap</b><br>
    Use the layer control to switch between weekday and weekend.
    </div>
    """

    m.get_root().html.add_child(folium.Element(title_html))

    output_path = FIGURES / "start_location_heatmap_with_basemap.html"
    m.save(output_path)

    print(f"Saved interactive basemap heatmap to: {output_path}")


def main():
    print("Loading start locations...")
    df = load_start_locations()
    print(f"Loaded rows: {len(df):,}")

    print("Sampling equal weekday and weekend groups...")
    sample = sample_equal_groups(df)
    print(sample["day_type"].value_counts())

    print("Creating basemap heatmap...")
    create_basemap_heatmap(sample)


if __name__ == "__main__":
    main()