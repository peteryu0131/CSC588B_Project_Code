from pathlib import Path

import pandas as pd

from _pipeline_utils import ensure_project_folders, print_output_paths, project_root


WEATHER_FILENAME = "Weather Dataset Station Chicago Midway Airport IL US.csv"
EXPECTED_WEATHER_FIELDS = ["DATE", "TMAX", "TMIN", "PRCP", "SNOW", "SNWD"]


def require_cleaned_data(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Cleaned Divvy data not found. Run src/01_combine_and_clean.py first: {path}")


def find_weather_file(root: Path) -> Path | None:
    candidates = [
        root / WEATHER_FILENAME,
        root / "data" / "raw" / WEATHER_FILENAME,
        root / "data" / "raw" / "weather" / WEATHER_FILENAME,
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def normalize_weather_column(column: str) -> str:
    return column.strip().split(" ")[0].upper()


def read_weather_csv(path: Path) -> pd.DataFrame:
    # NOAA export used here has one station-name metadata line before the header.
    for skiprows in (1, 0):
        weather = pd.read_csv(path, skiprows=skiprows)
        renamed = {column: normalize_weather_column(column) for column in weather.columns}
        weather = weather.rename(columns=renamed)
        if "DATE" in weather.columns:
            return weather

    print("Weather CSV columns:")
    print(pd.read_csv(path, nrows=0).columns.tolist())
    raise ValueError("Could not find DATE in weather CSV.")


def prepare_weather(weather: pd.DataFrame) -> pd.DataFrame:
    missing = [field for field in EXPECTED_WEATHER_FIELDS if field not in weather.columns]
    if missing:
        print("Weather CSV is missing these expected fields:")
        print(missing)
        print("Available weather CSV columns:")
        print(weather.columns.tolist())

    weather = weather.copy()
    weather["date"] = pd.to_datetime(weather["DATE"], errors="coerce").dt.strftime("%Y-%m-%d")
    weather = weather.dropna(subset=["date"])

    numeric_fields = [field for field in EXPECTED_WEATHER_FIELDS if field != "DATE" and field in weather.columns]
    for field in numeric_fields:
        weather[field] = pd.to_numeric(weather[field], errors="coerce")

    return weather[["date", *numeric_fields]]


def create_daily_divvy_summary(cleaned_path: Path) -> pd.DataFrame:
    divvy = pd.read_csv(
        cleaned_path,
        usecols=["date", "trip_duration_minutes", "trip_length_km"],
    )
    return (
        divvy.groupby("date")
        .agg(
            daily_trip_count=("date", "size"),
            daily_median_duration=("trip_duration_minutes", "median"),
            daily_median_trip_length=("trip_length_km", "median"),
        )
        .reset_index()
    )


def main() -> None:
    root = project_root()
    ensure_project_folders(root)

    cleaned_path = root / "data" / "processed" / "divvy_2025_cleaned.csv"
    require_cleaned_data(cleaned_path)

    weather_path = find_weather_file(root)
    if weather_path is None:
        raise FileNotFoundError(
            f"Weather CSV not found at project root, data/raw/, or data/raw/weather/{WEATHER_FILENAME}"
        )

    weather = prepare_weather(read_weather_csv(weather_path))
    daily_divvy = create_daily_divvy_summary(cleaned_path)
    merged = daily_divvy.merge(weather, on="date", how="left")

    output_path = root / "outputs" / "daily_trip_weather_summary.csv"
    merged.to_csv(output_path, index=False)
    print_output_paths([output_path])


if __name__ == "__main__":
    main()
