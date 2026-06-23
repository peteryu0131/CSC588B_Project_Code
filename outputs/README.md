# Outputs

Use `outputs/final_clean/` for final project tables.

Important final tables:

```text
final_clean/final_results_summary.csv
final_clean/validation_overview.csv
final_clean/final_validation_decision_summary.csv
final_clean/weekday_weekend_service_profile_comparison.csv
final_clean/bootstrap_service_category_stability.csv
final_clean/osm_coverage_bias_summary.csv
```

Root-level files in this folder are older/intermediate outputs or caches from earlier project stages. Do not delete these dependency caches if you need to rerun the clean notebook:

```text
osm_pois_chicago_services.csv
cleaning_summary.csv
weekday_weekend_counts.csv
trip_summary_by_day_type.csv
distribution_fit_summary.csv
daily_trip_weather_summary.csv
weather_labels_2025.csv
```

For final submission and presentation, prefer files under `outputs/final_clean/`.
