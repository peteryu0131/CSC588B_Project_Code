from pathlib import Path

import pandas as pd

from _pipeline_utils import (
    REQUIRED_DIVVY_COLUMNS,
    add_calendar_fields,
    ensure_project_folders,
    find_divvy_monthly_files,
    filter_started_year,
    haversine_km,
    parse_full_timestamp,
    print_output_paths,
    project_root,
    valid_coordinate_mask,
    validate_required_columns,
)


CHUNKSIZE = 250_000
ANALYSIS_YEAR = 2025
MAX_DURATION_MINUTES = 1440
MAX_TRIP_LENGTH_KM = 50


def source_month_from_file(csv_path: Path) -> str:
    raw_month = csv_path.name[:6]
    return f"{raw_month[:4]}-{raw_month[4:]}"


def clean_chunk(chunk: pd.DataFrame, source_month: str) -> tuple[pd.DataFrame, dict[str, int]]:
    counts = {
        "original rows": len(chunk),
        "rows after timestamp filter": 0,
        "rows after 2025 started_at filter": 0,
        "rows after coordinate filter": 0,
        "rows after duration filter": 0,
        "rows after distance filter": 0,
        "final rows": 0,
    }

    chunk = chunk.copy()
    chunk["source_month"] = source_month
    chunk["started_at"] = parse_full_timestamp(chunk["started_at"])
    chunk["ended_at"] = parse_full_timestamp(chunk["ended_at"])
    chunk = chunk.dropna(subset=["started_at", "ended_at"])
    counts["rows after timestamp filter"] = len(chunk)

    chunk = filter_started_year(chunk, ANALYSIS_YEAR)
    counts["rows after 2025 started_at filter"] = len(chunk)

    coordinate_columns = ["start_lat", "start_lng", "end_lat", "end_lng"]
    for column in coordinate_columns:
        chunk[column] = pd.to_numeric(chunk[column], errors="coerce")
    chunk = chunk.dropna(subset=coordinate_columns)
    chunk = chunk.loc[valid_coordinate_mask(chunk)].copy()
    counts["rows after coordinate filter"] = len(chunk)

    duration = chunk["ended_at"] - chunk["started_at"]
    chunk["trip_duration_minutes"] = duration.dt.total_seconds() / 60.0
    duration_mask = chunk["trip_duration_minutes"].gt(0) & chunk["trip_duration_minutes"].le(
        MAX_DURATION_MINUTES
    )
    chunk = chunk.loc[duration_mask].copy()
    counts["rows after duration filter"] = len(chunk)

    chunk["trip_length_km"] = haversine_km(
        chunk["start_lat"],
        chunk["start_lng"],
        chunk["end_lat"],
        chunk["end_lng"],
    )
    distance_mask = chunk["trip_length_km"].ge(0) & chunk["trip_length_km"].le(MAX_TRIP_LENGTH_KM)
    chunk = chunk.loc[distance_mask].copy()
    counts["rows after distance filter"] = len(chunk)

    chunk = add_calendar_fields(chunk)
    counts["final rows"] = len(chunk)
    return chunk, counts


def add_counts(total_counts: dict[str, int], chunk_counts: dict[str, int]) -> None:
    for key, value in chunk_counts.items():
        total_counts[key] = total_counts.get(key, 0) + value


def write_cleaned_data(monthly_files: list[Path], cleaned_path: Path) -> dict[str, int]:
    total_counts = {
        "original rows": 0,
        "rows after timestamp filter": 0,
        "rows after 2025 started_at filter": 0,
        "rows after coordinate filter": 0,
        "rows after duration filter": 0,
        "rows after distance filter": 0,
        "final rows": 0,
    }
    first_write = True

    if cleaned_path.exists():
        cleaned_path.unlink()

    for csv_path in monthly_files:
        validate_required_columns(csv_path, REQUIRED_DIVVY_COLUMNS)
        source_month = source_month_from_file(csv_path)
        print(f"Reading {csv_path.name}")
        reader = pd.read_csv(
            csv_path,
            usecols=REQUIRED_DIVVY_COLUMNS,
            chunksize=CHUNKSIZE,
            low_memory=False,
        )
        for chunk in reader:
            cleaned_chunk, chunk_counts = clean_chunk(chunk, source_month)
            add_counts(total_counts, chunk_counts)
            cleaned_chunk.to_csv(
                cleaned_path,
                mode="w" if first_write else "a",
                header=first_write,
                index=False,
            )
            first_write = False

    if first_write:
        pd.DataFrame(columns=REQUIRED_DIVVY_COLUMNS).to_csv(cleaned_path, index=False)

    return total_counts


def write_cleaning_summary(total_counts: dict[str, int], summary_path: Path) -> pd.DataFrame:
    rows = []
    previous_rows = None
    for stage, row_count in total_counts.items():
        removed = 0 if previous_rows is None else previous_rows - row_count
        rows.append(
            {
                "stage": stage,
                "rows": row_count,
                "removed_since_previous_stage": removed,
            }
        )
        previous_rows = row_count

    summary = pd.DataFrame(rows)
    summary.to_csv(summary_path, index=False)
    return summary


def main() -> None:
    root = project_root()
    ensure_project_folders(root)

    monthly_files = find_divvy_monthly_files(root)
    if not monthly_files:
        raise FileNotFoundError(
            "No 2025 monthly Divvy CSV files found in 2025_full_year_by_month/ "
            "or data/raw/2025_full_year_by_month/."
        )

    cleaned_path = root / "data" / "processed" / "divvy_2025_cleaned.csv"
    summary_path = root / "outputs" / "cleaning_summary.csv"

    total_counts = write_cleaned_data(monthly_files, cleaned_path)
    write_cleaning_summary(total_counts, summary_path)

    print_output_paths([cleaned_path, summary_path])


if __name__ == "__main__":
    main()
