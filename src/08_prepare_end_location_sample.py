from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "divvy_2025_cleaned.csv"
OUTPUTS = ROOT / "outputs"

OUTPUTS.mkdir(exist_ok=True)


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing cleaned data file: {DATA_PATH}\n"
            "Run python src\\01_combine_and_clean.py first."
        )

    columns = pd.read_csv(DATA_PATH, nrows=5).columns.tolist()
    print("Available columns:")
    print(columns)

    required = ["day_type", "end_lat", "end_lng"]
    missing = [col for col in required if col not in columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = pd.read_csv(DATA_PATH, usecols=required)

    df = df[
        df["day_type"].isin(["weekday", "weekend"])
        & df["end_lat"].between(41.5, 42.2)
        & df["end_lng"].between(-88.0, -87.3)
    ].copy()

    df = df.dropna(subset=["end_lat", "end_lng"])

    print("Rows after filtering:")
    print(len(df))

    sample_parts = []

    for day_type in ["weekday", "weekend"]:
        group = df[df["day_type"] == day_type]
        n = min(len(group), 100_000)

        sample = group.sample(n=n, random_state=42)
        sample_parts.append(sample)

        print(f"{day_type}: sampled {n:,} end locations")

    sampled_df = pd.concat(sample_parts, ignore_index=True)

    output_path = OUTPUTS / "end_location_sample_for_osm.csv"
    sampled_df.to_csv(output_path, index=False)

    print(f"Saved sample to: {output_path}")
    print(sampled_df.head())


if __name__ == "__main__":
    main()