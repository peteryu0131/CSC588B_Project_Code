# CSC588B Divvy Final Project

This repository contains the final notebook and supporting outputs for the CSC588B Divvy bike-share spatial mobility project.

## Final Submission

Submit this notebook:

```text
notebooks/Divvy_Final_Project_Clean.ipynb
```

Use this meeting/defense guide when explaining the notebook:

```text
notebooks/Divvy_Final_Project_Clean_Notebook_Guide.md
```

Do not submit this older merged notebook:

```text
notebooks/Divvy_Final_Project_Merged_Notebook.ipynb
```

The clean notebook has been executed successfully. The merged notebook is kept only as legacy work and may contain old path errors or unfinished cells.

## Project Question

How do weekday and weekend Divvy end-station patterns differ in Chicago, and what nearby urban service environments are associated with high-volume weekday and weekend destinations?

The project treats an end station as a destination proxy. Nearby OpenStreetMap services describe the station environment; they do not prove individual rider intent or causality.

## Main Pipeline

```text
Divvy trips
-> cleaning and preprocessing
-> weekday/weekend temporal stratification
-> end-station aggregation
-> baseline duration/distance distributions
-> Top20 end-station overlap
-> normalized spatial heatmaps
-> coordinate-based OSM service profiles
-> Top100 main service-profile analysis
-> validation system
-> weather secondary check
-> discussion and limitations
```

## Key Results

| Result | Value / interpretation |
|---|---|
| Cleaned trip rows | 5,547,168 |
| Weekday share | 71.59% |
| Weekend share | 28.41% |
| Top20 weekday/weekend overlap | 55% |
| Main OSM profile set | Top100 weekday/weekend union, 250m radius |
| Top100 OSM covered return share | 63.63% |
| Weekend-oriented stable service | `tourism` |
| Weekday-oriented stable services | `food_drink`, `office`, `health` |
| Label shuffle p-value | 0.2657, so do not claim overall statistical significance |
| Station-demand randomization p-value | 0.0010, structured under station-total/global-share null |
| Station-service permutation p-value | 0.0010, real station-service pairing is structured |
| Weather rain-effect L1 | about 0.0089, secondary only |

Final claim: weekday and weekend high-volume Divvy destination patterns differ spatially and are associated with different nearby OSM service environments. The conclusion is exploratory and associative, not causal.

## Folder Structure

```text
data/
  raw/                         original raw data
  processed/                   generated cleaned trip-level data
  outputs/                     older/intermediate cached tables
  openmapdata/                 older OSM-related working files

figures/
  final_clean/                 final notebook figures
  *.png, *.html                older/intermediate figures

notebooks/
  Divvy_Final_Project_Clean.ipynb
  Divvy_Final_Project_Clean_Notebook_Guide.md
  other notebooks              legacy/proposal/development work

outputs/
  final_clean/                 final notebook tables
  osm_pois_chicago_services.csv local OSM cache needed by clean notebook
  other root files             older/intermediate outputs

src/
  pipeline scripts from earlier project stages

tests/
  focused unit tests for reusable pipeline utilities
```

## Important Final Outputs

Tables:

```text
outputs/final_clean/final_results_summary.csv
outputs/final_clean/validation_overview.csv
outputs/final_clean/final_validation_decision_summary.csv
outputs/final_clean/weekday_weekend_service_profile_comparison.csv
outputs/final_clean/bootstrap_service_category_stability.csv
outputs/final_clean/osm_coverage_bias_summary.csv
```

Figures:

```text
figures/final_clean/weekday_weekend_normalized_destination_heatmaps.png
figures/final_clean/weekend_minus_weekday_destination_difference_map.png
figures/final_clean/weekend_minus_weekday_service_difference.png
figures/final_clean/bootstrap_service_category_ci.png
figures/final_clean/topk_radius_l1_heatmap.png
```

## Running The Final Notebook

Use the Jupyter kernel:

```text
Python (CSC588B Project)
```

Command-line verification from the project root:

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks\Divvy_Final_Project_Clean.ipynb --ExecutePreprocessor.timeout=900 --ExecutePreprocessor.kernel_name=csc588b-project
```

The clean notebook reads the processed Divvy file and local cached OSM/weather inputs, then writes final outputs into:

```text
outputs/final_clean/
figures/final_clean/
```

## Checks

Run these from the project root:

```powershell
python -m unittest discover -s tests
python -m py_compile src\*.py
python -m json.tool notebooks\Divvy_Final_Project_Clean.ipynb > $null
```

For the final project, the most important check is that `Divvy_Final_Project_Clean.ipynb` executes with zero notebook error outputs.
