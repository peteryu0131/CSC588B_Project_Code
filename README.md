# CSC588B Divvy Bike-share Pipeline

Project topic:

`Weekday and Weekend Differences in Shared Mobility Patterns: A Bike-Share Case Study`

This project uses Python only. Do not use Excel for cleaning or analysis.

## Folder Guide

This project separates raw data, processed data, summary tables, figures, notebooks, and scripts.

```text
data/
  raw/
    2025_full_year_by_month/
      202501-divvy-tripdata.csv
      ...
      202512-divvy-tripdata.csv
    Weather Dataset Station Chicago Midway Airport IL US.csv

  processed/
    divvy_2025_cleaned.csv
    dwell_proxy_2025.csv

outputs/
  cleaning_summary.csv
  weekday_weekend_counts.csv
  monthly_counts_by_day_type.csv
  trip_summary_by_day_type.csv
  dwell_proxy_summary_by_day_type.csv
  daily_trip_weather_summary.csv

figures/
  heatmap_start_locations_weekday_weekend.png
  heatmap_start_locations_overall.png
  trip_length_boxplot.png
  trip_duration_boxplot.png
  monthly_trip_counts_by_day_type.png
  dwell_proxy_boxplot.png

src/
  01_combine_and_clean.py
  02_eda_trip_patterns.py
  03_dwell_proxy.py
  04_spatial_heatmaps.py
  05_optional_weather_merge.py

notebooks/
  proposal_summary.ipynb
```

## Raw Data

`data/raw/` contains only original, unprocessed datasets. Do not edit these files after downloading them.

### Divvy Monthly Trip Files

Location:

```text
data/raw/2025_full_year_by_month/
```

Expected files:

```text
202501-divvy-tripdata.csv
202502-divvy-tripdata.csv
...
202512-divvy-tripdata.csv
```

These files are the official monthly Chicago Divvy trip records. Each row is one trip. Important raw columns include:

- `ride_id`: unique trip ID
- `rideable_type`: bike type
- `started_at`, `ended_at`: trip start and end timestamps
- `start_station_name`, `start_station_id`: trip start station
- `end_station_name`, `end_station_id`: trip end station
- `start_lat`, `start_lng`: start coordinates
- `end_lat`, `end_lng`: end coordinates
- `member_casual`: rider type

### Weather Data

Location:

```text
data/raw/Weather Dataset Station Chicago Midway Airport IL US.csv
```

This is the NOAA daily weather file for Chicago Midway Airport. It is optional for the proposal and is mainly for final-project extension work. Important columns include:

- `DATE`: weather date
- `TMAX`: daily maximum temperature
- `TMIN`: daily minimum temperature
- `PRCP`: precipitation
- `SNOW`: snowfall
- `SNWD`: snow depth

The optional weather script can also read the same file from:

```text
data/raw/weather/Weather Dataset Station Chicago Midway Airport IL US.csv
```

## Run Order

Run these commands from the project root:

```powershell
python src/01_combine_and_clean.py
python src/02_eda_trip_patterns.py
python src/03_dwell_proxy.py
python src/04_spatial_heatmaps.py
python src/05_optional_weather_merge.py
```

The weather merge is optional and should be run after the core Divvy pipeline works.

After the pipeline runs, open the proposal notebook:

```text
notebooks/proposal_summary.ipynb
```

The notebook is for writing and presentation only. It reads `outputs/` and `figures/`; it does not replace the scripts in `src/`.

Use the Jupyter kernel named:

```text
Python (CSC588B Project)
```

This kernel points to the same miniconda Python environment used by the scripts.

## Processed Data

`data/processed/` contains script-generated cleaned datasets. These files can be deleted and regenerated from `data/raw/`.

### `data/processed/divvy_2025_cleaned.csv`

Created by:

```text
src/01_combine_and_clean.py
```

This is the main cleaned trip-level dataset. Each row is one valid 2025 Divvy trip after timestamp, coordinate, duration, and distance filters.

It keeps the original Divvy fields and adds:

- `source_month`: source monthly CSV, such as `2025-01`
- `trip_duration_minutes`: trip duration in minutes
- `trip_length_km`: straight-line start-to-end distance from the haversine formula
- `day_type`: `weekday` for Monday-Friday, `weekend` for Saturday-Sunday
- `date`: trip start date
- `month`: trip start month as a number
- `hour`: trip start hour
- `season`: `Winter`, `Spring`, `Summer`, or `Fall`

### `data/processed/dwell_proxy_2025.csv`

Created by:

```text
src/03_dwell_proxy.py
```

This file stores the station-level dwell time proxy. Each row represents an arrival event at a station and the next departure event from the same station.

Important columns:

- `station_id`, `station_name`: station used for the proxy calculation
- `arrival_time`: time when a trip ended at the station
- `departure_time`: next time a trip started from the same station
- `dwell_time_minutes`: time between arrival and next departure
- `day_type`: based on `arrival_time`
- `date`: arrival date

Important limitation: this is not bike-level dwell time because the public Divvy data does not include `bike_id`.

## Summary Tables

`outputs/` contains small CSV tables for reporting and proposal writing.

- `cleaning_summary.csv`: row counts after each cleaning step. Use this to explain data filtering.
- `weekday_weekend_counts.csv`: total weekday and weekend trip counts plus shares.
- `monthly_counts_by_day_type.csv`: monthly trip counts split by weekday/weekend. Use this to show full-year coverage.
- `trip_summary_by_day_type.csv`: count, mean, median, quartiles, min, and max for trip duration and trip length by day type.
- `dwell_proxy_summary_by_day_type.csv`: count, mean, median, q1, and q3 for station-level dwell proxy by day type.
- `daily_trip_weather_summary.csv`: optional daily Divvy summary merged with NOAA weather fields.

## Figures

`figures/` contains PNG files generated from the processed data.

- `heatmap_start_locations_weekday_weekend.png`: side-by-side weekday/weekend start-location density. This is the strongest spatial proposal figure.
- `heatmap_start_locations_overall.png`: overall start-location density.
- `trip_length_boxplot.png`: weekday/weekend straight-line trip length comparison.
- `trip_duration_boxplot.png`: weekday/weekend trip duration comparison.
- `monthly_trip_counts_by_day_type.png`: monthly trip counts by day type.
- `dwell_proxy_boxplot.png`: weekday/weekend station-level dwell time proxy comparison.

## Best Proposal Outputs

Use these first for the 2-page proposal:

- `figures/heatmap_start_locations_weekday_weekend.png`
- `figures/trip_length_boxplot.png`
- `figures/monthly_trip_counts_by_day_type.png`
- `outputs/trip_summary_by_day_type.csv`
- `outputs/cleaning_summary.csv`

The dwell proxy is useful, but describe it carefully:

`station-level dwell time proxy = time from an end event at a station to the next start event at the same station`

It is not bike-level dwell time because the public Divvy trip data does not include `bike_id`.

## Important Data Note

The cleaner intentionally accepts only full timestamps such as:

```text
2025-02-25 21:21:21.171
```

It rejects time-only values such as:

```text
23:54.5
```

This prevents pandas from accidentally parsing time-only strings as the current date. If `202501-divvy-tripdata.csv` contains time-only values, January rows will be removed by the timestamp filter. Replace that file with the original Divvy CSV if you need January included in weekday/weekend, monthly, and seasonal analysis.

The cleaner also keeps only rows where `started_at` is in 2025. This removes a small number of cross-year records, such as trips starting on `2024-12-31`, so the analysis stays aligned with the 2025 full-year scope.

## Checks

Run:

```powershell
python -m unittest discover -s tests
python -m py_compile src/*.py
```
