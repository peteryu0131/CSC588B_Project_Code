from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_DIVVY_COLUMNS = [
    "ride_id",
    "rideable_type",
    "started_at",
    "ended_at",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
    "start_lat",
    "start_lng",
    "end_lat",
    "end_lng",
    "member_casual",
]

OUTPUT_DIRS = [
    "data/raw",
    "data/processed",
    "outputs",
    "figures",
    "src",
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_project_folders(root: Path) -> None:
    for relative_path in OUTPUT_DIRS:
        (root / relative_path).mkdir(parents=True, exist_ok=True)


def find_divvy_monthly_files(root: Path) -> list[Path]:
    candidates = [
        root / "2025_full_year_by_month",
        root / "data" / "raw" / "2025_full_year_by_month",
    ]
    for source_dir in candidates:
        files = sorted(source_dir.glob("2025*-divvy-tripdata.csv"))
        if files:
            return files
    return []


def validate_required_columns(csv_path: Path, required_columns: list[str]) -> None:
    columns = pd.read_csv(csv_path, nrows=0).columns.tolist()
    missing = [column for column in required_columns if column not in columns]
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"{csv_path} is missing required columns: {missing_text}")


def parse_full_timestamp(values: pd.Series) -> pd.Series:
    text_values = values.astype("string").str.strip()
    full_timestamp_mask = text_values.str.match(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", na=False)
    return pd.to_datetime(text_values.where(full_timestamp_mask), errors="coerce")


def haversine_km(
    start_lat: pd.Series,
    start_lng: pd.Series,
    end_lat: pd.Series,
    end_lng: pd.Series,
) -> pd.Series:
    radius_km = 6371.0088
    lat1 = np.radians(start_lat.astype(float))
    lon1 = np.radians(start_lng.astype(float))
    lat2 = np.radians(end_lat.astype(float))
    lon2 = np.radians(end_lng.astype(float))

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return radius_km * c


def valid_coordinate_mask(df: pd.DataFrame) -> pd.Series:
    return (
        df["start_lat"].between(-90, 90)
        & df["end_lat"].between(-90, 90)
        & df["start_lng"].between(-180, 180)
        & df["end_lng"].between(-180, 180)
        & ~((df["start_lat"] == 0) & (df["start_lng"] == 0))
        & ~((df["end_lat"] == 0) & (df["end_lng"] == 0))
    )


def filter_started_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    return df.loc[df["started_at"].dt.year.eq(year)].copy()


def add_calendar_fields(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["date"] = result["started_at"].dt.date.astype(str)
    result["month"] = result["started_at"].dt.month
    result["hour"] = result["started_at"].dt.hour
    result["day_type"] = np.where(result["started_at"].dt.dayofweek < 5, "weekday", "weekend")
    result["season"] = result["month"].map(month_to_season)
    return result


def month_to_season(month: int) -> str:
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Fall"


def summary_by_group(df: pd.DataFrame, group_column: str, value_column: str) -> pd.DataFrame:
    grouped = df.groupby(group_column, observed=True)[value_column]
    summary = grouped.agg(
        count="count",
        mean="mean",
        median="median",
        min="min",
        max="max",
    )
    summary["q1"] = grouped.quantile(0.25)
    summary["q3"] = grouped.quantile(0.75)
    summary = summary.reset_index()
    return summary[[group_column, "count", "mean", "median", "q1", "q3", "min", "max"]]


def print_output_paths(paths: list[Path]) -> None:
    print("Output files:")
    for path in paths:
        print(f"- {path}")
