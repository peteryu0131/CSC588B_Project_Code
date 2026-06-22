from pathlib import Path
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "divvy_2025_cleaned.csv"
OUTPUTS = ROOT / "outputs"
FIGURES = ROOT / "figures"

OUTPUTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


def haversine_km(lat1, lon1, lat2, lon2):
    radius_km = 6371.0088

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))

    return radius_km * c


def find_column(columns, candidates):
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def load_distribution_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing cleaned data file: {DATA_PATH}\n"
            "Run python src\\01_combine_and_clean.py first."
        )

    all_columns = pd.read_csv(DATA_PATH, nrows=5).columns.tolist()
    print("Available columns:")
    print(all_columns)

    duration_col = find_column(
        all_columns,
        [
            "duration_min",
            "trip_duration_min",
            "duration_minutes",
            "trip_duration_minutes",
        ],
    )

    distance_col = find_column(
        all_columns,
        [
            "distance_km",
            "trip_distance_km",
            "straight_line_distance_km",
            "trip_length_km",
            "trip_length_km_haversine",
        ],
    )

    needed_columns = ["day_type"]

    if duration_col is not None:
        needed_columns.append(duration_col)
    else:
        needed_columns.extend(["started_at", "ended_at"])

    if distance_col is not None:
        needed_columns.append(distance_col)
    else:
        needed_columns.extend(["start_lat", "start_lng", "end_lat", "end_lng"])

    needed_columns = [col for col in needed_columns if col in all_columns]

    df = pd.read_csv(DATA_PATH, usecols=needed_columns)
    df = df[df["day_type"].isin(["weekday", "weekend"])].copy()

    if duration_col is not None:
        df["duration_min_for_analysis"] = df[duration_col]
    else:
        df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
        df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")
        df["duration_min_for_analysis"] = (
            df["ended_at"] - df["started_at"]
        ).dt.total_seconds() / 60

    if distance_col is not None:
        df["distance_km_for_analysis"] = df[distance_col]
    else:
        df["distance_km_for_analysis"] = haversine_km(
            df["start_lat"],
            df["start_lng"],
            df["end_lat"],
            df["end_lng"],
        )

    df = df[
        (df["duration_min_for_analysis"] > 0)
        & (df["distance_km_for_analysis"] > 0)
        & np.isfinite(df["duration_min_for_analysis"])
        & np.isfinite(df["distance_km_for_analysis"])
    ].copy()

    return df


def sample_by_day_type(df, max_per_group=200_000):
    return (
        df.groupby("day_type", group_keys=False)
        .apply(lambda x: x.sample(min(len(x), max_per_group), random_state=42))
        .reset_index(drop=True)
    )


def fit_lognormal(values):
    values = np.asarray(values)
    values = values[np.isfinite(values) & (values > 0)]

    log_values = np.log(values)
    mu = log_values.mean()
    sigma = log_values.std(ddof=1)

    return {
        "lognormal_mu": mu,
        "lognormal_sigma": sigma,
        "lognormal_median": math.exp(mu),
    }


def fit_powerlaw_tail(values, xmin_quantile=0.90):
    values = np.asarray(values)
    values = values[np.isfinite(values) & (values > 0)]

    xmin = np.quantile(values, xmin_quantile)
    tail = values[values >= xmin]

    alpha = 1 + len(tail) / np.sum(np.log(tail / xmin))

    return {
        "powerlaw_xmin_q90": xmin,
        "powerlaw_alpha_tail": alpha,
        "powerlaw_tail_n": len(tail),
    }


def make_summary_table(df):
    rows = []

    for day_type in ["weekday", "weekend"]:
        group = df[df["day_type"] == day_type]

        for variable, column in [
            ("trip_duration_min", "duration_min_for_analysis"),
            ("straight_line_distance_km", "distance_km_for_analysis"),
        ]:
            values = group[column].dropna()
            values = values[values > 0]

            row = {
                "day_type": day_type,
                "variable": variable,
                "count": len(values),
                "mean": values.mean(),
                "median": values.median(),
                "q1": values.quantile(0.25),
                "q3": values.quantile(0.75),
                "skew": values.skew(),
            }

            row.update(fit_lognormal(values))
            row.update(fit_powerlaw_tail(values))

            rows.append(row)

    summary = pd.DataFrame(rows)
    return summary


def plot_log_histogram(df, column, title, xlabel, output_filename):
    fig, ax = plt.subplots(figsize=(8, 5))

    for day_type in ["weekday", "weekend"]:
        values = df.loc[df["day_type"] == day_type, column].dropna()
        values = values[values > 0]

        lower = values.quantile(0.001)
        upper = values.quantile(0.999)

        bins = np.logspace(np.log10(lower), np.log10(upper), 80)

        ax.hist(
            values,
            bins=bins,
            density=True,
            alpha=0.45,
            label=day_type,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Density")
    ax.legend()
    fig.tight_layout()

    output_path = FIGURES / output_filename
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.show()
    print(f"Saved {output_path}")


def plot_ccdf(df, column, title, xlabel, output_filename):
    fig, ax = plt.subplots(figsize=(8, 5))

    for day_type in ["weekday", "weekend"]:
        values = df.loc[df["day_type"] == day_type, column].dropna()
        values = np.sort(values[values > 0])

        ccdf = 1.0 - np.arange(1, len(values) + 1) / len(values)

        ax.plot(values, ccdf, label=day_type)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("P(X ≥ x)")
    ax.legend()
    fig.tight_layout()

    output_path = FIGURES / output_filename
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.show()
    print(f"Saved {output_path}")


def main():
    print("Loading cleaned Divvy data...")
    df = load_distribution_data()
    print(f"Rows available for distribution analysis: {len(df):,}")

    print("Sampling data for plots...")
    sample = sample_by_day_type(df)

    print("Creating distribution fit summary...")
    summary = make_summary_table(df)

    summary_path = OUTPUTS / "distribution_fit_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"Saved {summary_path}")

    print(summary)

    plot_log_histogram(
        sample,
        "duration_min_for_analysis",
        "Trip Duration Distribution by Day Type",
        "Trip duration, minutes, log scale",
        "trip_duration_distribution_loglog.png",
    )

    plot_log_histogram(
        sample,
        "distance_km_for_analysis",
        "Straight-line Distance Distribution by Day Type",
        "Straight-line distance, km, log scale",
        "trip_distance_distribution_loglog.png",
    )

    plot_ccdf(
        sample,
        "duration_min_for_analysis",
        "CCDF of Trip Duration by Day Type",
        "Trip duration, minutes, log scale",
        "trip_duration_ccdf.png",
    )

    plot_ccdf(
        sample,
        "distance_km_for_analysis",
        "CCDF of Straight-line Distance by Day Type",
        "Straight-line distance, km, log scale",
        "trip_distance_ccdf.png",
    )


if __name__ == "__main__":
    main()