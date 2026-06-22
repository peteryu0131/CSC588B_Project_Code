from pathlib import Path
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import requests
except ImportError as exc:
    raise ImportError("Please install requests: pip install requests") from exc

try:
    from sklearn.neighbors import BallTree
except ImportError as exc:
    raise ImportError("Please install scikit-learn: pip install scikit-learn") from exc


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
FIGURES = ROOT / "figures"

SAMPLE_PATH = OUTPUTS / "end_location_sample_for_osm.csv"
POI_CACHE_PATH = OUTPUTS / "osm_pois_chicago_services.csv"

CLASSIFIED_OUTPUT_PATH = OUTPUTS / "end_location_osm_service_classified.csv"
SUMMARY_OUTPUT_PATH = OUTPUTS / "osm_service_summary_by_day_type.csv"
COMPARISON_OUTPUT_PATH = OUTPUTS / "osm_service_weekend_weekday_comparison.csv"

RADIUS_METERS = 250
EARTH_RADIUS_METERS = 6_371_008.8

OUTPUTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


def make_bbox_from_sample(df, padding=0.015):
    south = df["end_lat"].quantile(0.005) - padding
    north = df["end_lat"].quantile(0.995) + padding
    west = df["end_lng"].quantile(0.005) - padding
    east = df["end_lng"].quantile(0.995) + padding

    return south, west, north, east


def build_overpass_query(south, west, north, east):
    bbox = f"{south},{west},{north},{east}"

    query = f"""
    [out:json][timeout:300];
    (
      node["amenity"~"restaurant|cafe|bar|pub|fast_food|school|university|college|library|hospital|clinic|doctors|dentist|pharmacy|bus_station"]({bbox});

      node["shop"]({bbox});

      node["tourism"]({bbox});

      node["leisure"~"park|fitness_centre|sports_centre|marina|stadium|pitch|playground|garden"]({bbox});

      node["office"]({bbox});

      node["public_transport"]({bbox});

      node["railway"~"station|subway_entrance|tram_stop|halt"]({bbox});

      node["highway"="bus_stop"]({bbox});
    );
    out body;
    """
    return query


def classify_service(tags):
    amenity = str(tags.get("amenity", "")).lower()
    shop = str(tags.get("shop", "")).lower()
    tourism = str(tags.get("tourism", "")).lower()
    leisure = str(tags.get("leisure", "")).lower()
    office = str(tags.get("office", "")).lower()
    public_transport = str(tags.get("public_transport", "")).lower()
    railway = str(tags.get("railway", "")).lower()
    highway = str(tags.get("highway", "")).lower()

    food_drink = {"restaurant", "cafe", "bar", "pub", "fast_food"}
    education = {"school", "university", "college", "library"}
    health = {"hospital", "clinic", "doctors", "dentist", "pharmacy"}
    transit_amenities = {"bus_station"}

    if shop:
        return "retail"

    if amenity in food_drink:
        return "food_drink"

    if amenity in education:
        return "education"

    if amenity in health:
        return "health"

    if amenity in transit_amenities:
        return "transit"

    if tourism:
        return "tourism"

    if leisure:
        return "recreation"

    if office:
        return "office"

    if public_transport or railway or highway == "bus_stop":
        return "transit"

    return "other_service"


def download_osm_pois(endpoints):
    south, west, north, east = make_bbox_from_sample(endpoints)

    print("Full OSM query bounding box:")
    print(f"south={south:.5f}, west={west:.5f}, north={north:.5f}, east={east:.5f}")

    urls = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.openstreetmap.fr/api/interpreter",
        "https://overpass.osm.ch/api/interpreter",
    ]

    n_lat_tiles = 4
    n_lon_tiles = 4

    all_elements = []

    for i in range(n_lat_tiles):
        tile_south = south + (north - south) * i / n_lat_tiles
        tile_north = south + (north - south) * (i + 1) / n_lat_tiles

        for j in range(n_lon_tiles):
            tile_west = west + (east - west) * j / n_lon_tiles
            tile_east = west + (east - west) * (j + 1) / n_lon_tiles

            print(
                f"\nQuerying tile {i + 1},{j + 1}: "
                f"{tile_south:.5f}, {tile_west:.5f}, {tile_north:.5f}, {tile_east:.5f}"
            )

            query = build_overpass_query(tile_south, tile_west, tile_north, tile_east)

            tile_success = False
            last_error = None

            for url in urls:
                try:
                    print(f"Trying: {url}")
                    response = requests.post(url, data={"data": query}, timeout=180)
                    response.raise_for_status()

                    data = response.json()
                    elements = data.get("elements", [])

                    print(f"Downloaded elements from this tile: {len(elements):,}")

                    all_elements.extend(elements)
                    tile_success = True

                    time.sleep(1)
                    break

                except Exception as exc:
                    last_error = exc
                    print(f"Failed with {url}: {exc}")
                    time.sleep(3)

            if not tile_success:
                print(f"Skipping this tile because all servers failed. Last error: {last_error}")

    print(f"\nTotal downloaded OSM elements before cleaning: {len(all_elements):,}")

    rows = []

    for element in all_elements:
        tags = element.get("tags", {})

        if "lat" in element and "lon" in element:
            lat = element["lat"]
            lon = element["lon"]
        elif "center" in element:
            lat = element["center"].get("lat")
            lon = element["center"].get("lon")
        else:
            continue

        if lat is None or lon is None:
            continue

        rows.append(
            {
                "osm_type": element.get("type"),
                "osm_id": element.get("id"),
                "lat": lat,
                "lon": lon,
                "name": tags.get("name", ""),
                "amenity": tags.get("amenity", ""),
                "shop": tags.get("shop", ""),
                "tourism": tags.get("tourism", ""),
                "leisure": tags.get("leisure", ""),
                "office": tags.get("office", ""),
                "public_transport": tags.get("public_transport", ""),
                "railway": tags.get("railway", ""),
                "highway": tags.get("highway", ""),
                "service_category": classify_service(tags),
            }
        )

    pois = pd.DataFrame(rows)

    if pois.empty:
        raise ValueError(
            "No OSM POIs were returned. The Overpass servers may be busy. "
            "Try running the script again later."
        )

    pois = pois.drop_duplicates(subset=["osm_type", "osm_id"])

    pois.to_csv(POI_CACHE_PATH, index=False)

    print(f"\nSaved OSM POIs to: {POI_CACHE_PATH}")
    print("\nOSM service category counts:")
    print(pois["service_category"].value_counts())

    return pois


def load_or_download_pois(endpoints):
    if POI_CACHE_PATH.exists():
        print(f"Using cached OSM POIs: {POI_CACHE_PATH}")
        pois = pd.read_csv(POI_CACHE_PATH)
        print(pois["service_category"].value_counts())
        return pois

    return download_osm_pois(endpoints)


def assign_nearest_service(endpoints, pois, radius_meters=250):
    endpoints = endpoints.reset_index(drop=True).copy()
    pois = pois.dropna(subset=["lat", "lon", "service_category"]).reset_index(drop=True)

    poi_coords_rad = np.radians(pois[["lat", "lon"]].to_numpy(dtype=float))
    endpoint_coords_rad = np.radians(endpoints[["end_lat", "end_lng"]].to_numpy(dtype=float))

    tree = BallTree(poi_coords_rad, metric="haversine")

    distances_rad, indices = tree.query(endpoint_coords_rad, k=1)

    distances_m = distances_rad[:, 0] * EARTH_RADIUS_METERS
    nearest_indices = indices[:, 0]

    nearest_pois = pois.iloc[nearest_indices].reset_index(drop=True)

    endpoints["nearest_osm_distance_m"] = distances_m
    endpoints["nearest_service_category"] = nearest_pois["service_category"].to_numpy()
    endpoints["nearest_osm_name"] = nearest_pois["name"].fillna("").to_numpy()

    no_service_label = f"no_service_within_{radius_meters}m"

    too_far = endpoints["nearest_osm_distance_m"] > radius_meters
    endpoints.loc[too_far, "nearest_service_category"] = no_service_label
    endpoints.loc[too_far, "nearest_osm_name"] = ""

    return endpoints


def create_summary(classified):
    summary = (
        classified.groupby(["day_type", "nearest_service_category"])
        .size()
        .reset_index(name="count")
    )

    summary["total_day_type"] = summary.groupby("day_type")["count"].transform("sum")
    summary["share"] = summary["count"] / summary["total_day_type"]
    summary["share_percent"] = summary["share"] * 100

    comparison = summary.pivot_table(
        index="nearest_service_category",
        columns="day_type",
        values="share",
        fill_value=0,
    ).reset_index()

    if "weekday" not in comparison.columns:
        comparison["weekday"] = 0

    if "weekend" not in comparison.columns:
        comparison["weekend"] = 0

    comparison["weekday_percent"] = comparison["weekday"] * 100
    comparison["weekend_percent"] = comparison["weekend"] * 100
    comparison["weekend_minus_weekday_percent"] = (
        comparison["weekend_percent"] - comparison["weekday_percent"]
    )

    comparison = comparison.sort_values(
        "weekend_minus_weekday_percent", ascending=False
    )

    return summary, comparison


def plot_service_shares(summary):
    plot_df = summary[
        ~summary["nearest_service_category"].str.startswith("no_service")
    ].copy()

    pivot = plot_df.pivot_table(
        index="nearest_service_category",
        columns="day_type",
        values="share_percent",
        fill_value=0,
    )

    if "weekday" in pivot.columns and "weekend" in pivot.columns:
        pivot = pivot[["weekday", "weekend"]]

    pivot = pivot.sort_values(by=pivot.columns.tolist(), ascending=False)

    ax = pivot.plot(kind="bar", figsize=(10, 5))

    ax.set_title("OSM service categories near Divvy trip end locations")
    ax.set_xlabel("Nearest OSM service category within 250 meters")
    ax.set_ylabel("Share of sampled end locations (%)")
    ax.legend(title="Day type")
    ax.grid(axis="y", alpha=0.3)

    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    output_path = FIGURES / "osm_service_share_by_day_type.png"
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.show()

    print(f"Saved figure: {output_path}")


def plot_weekend_minus_weekday(comparison):
    plot_df = comparison[
        ~comparison["nearest_service_category"].str.startswith("no_service")
    ].copy()

    plot_df = plot_df.sort_values("weekend_minus_weekday_percent")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        plot_df["nearest_service_category"],
        plot_df["weekend_minus_weekday_percent"],
    )

    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Weekend minus weekday difference in nearby OSM service categories")
    ax.set_xlabel("Weekend share minus weekday share, percentage points")
    ax.set_ylabel("Nearest OSM service category")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()

    output_path = FIGURES / "osm_service_weekend_minus_weekday.png"
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.show()

    print(f"Saved figure: {output_path}")


def main():
    if not SAMPLE_PATH.exists():
        raise FileNotFoundError(
            f"Missing sample file: {SAMPLE_PATH}\n"
            "Run python src\\08_prepare_end_location_sample.py first."
        )

    print("Loading sampled end locations...")
    endpoints = pd.read_csv(SAMPLE_PATH)

    print("Sample counts:")
    print(endpoints["day_type"].value_counts())

    print("Loading or downloading OSM POIs...")
    pois = load_or_download_pois(endpoints)

    print("Assigning nearest OSM service category...")
    classified = assign_nearest_service(endpoints, pois, radius_meters=RADIUS_METERS)

    classified.to_csv(CLASSIFIED_OUTPUT_PATH, index=False)
    print(f"Saved classified endpoints to: {CLASSIFIED_OUTPUT_PATH}")

    print("Creating summaries...")
    summary, comparison = create_summary(classified)

    summary.to_csv(SUMMARY_OUTPUT_PATH, index=False)
    comparison.to_csv(COMPARISON_OUTPUT_PATH, index=False)

    print(f"Saved summary to: {SUMMARY_OUTPUT_PATH}")
    print(f"Saved comparison to: {COMPARISON_OUTPUT_PATH}")

    print("\nService summary:")
    print(summary.sort_values(["day_type", "share_percent"], ascending=[True, False]))

    print("\nWeekend minus weekday comparison:")
    print(comparison)

    plot_service_shares(summary)
    plot_weekend_minus_weekday(comparison)


if __name__ == "__main__":
    main()