# CSC588B Divvy Final Project Presentation Outline

Topic: How do weekday and weekend Divvy end-station patterns differ in Chicago, and what nearby urban service environments are associated with high-volume weekday and weekend destinations?

Source files checked: `Final_Project.pdf`, `notebooks/Divvy_Final_Project_Clean.ipynb`, `notebooks/Divvy_Final_Project_Merged_Notebook.ipynb`, `notebooks/Divvy_Final_Project_Clean_Notebook_Guide.md`, and final outputs under `outputs/final_clean/`.

Use the clean notebook as the presentation source. The merged notebook exists, but the clean notebook is the final executed version.

## Instructor Rubric Organization

| Rubric category | Slides |
|---|---|
| Problem & Solution | 1-2 |
| Data Pipeline | 3-5 |
| Experimental Setup | 6 |
| Results | 7-10 |
| Delivery & Q&A | 11-12 |

## Slide 1: Title and Research Question

**Main message / 主要信息:** This is a focused spatial mobility question, not only a weekday/weekend count comparison. / 这是一个明确的空间出行问题，不只是比较工作日和周末数量。

**Figure/table to use / 使用内容:** Research Question and Hypothesis markdown cell.

**Rubric fit / 对应评分:** Problem & Solution.

**Slide content / 幻灯片内容:**

- EN: Research question: how do weekday and weekend Divvy end-station patterns differ in Chicago?
- CN: 研究问题：芝加哥 Divvy 工作日和周末的还车站点模式有什么不同？
- EN: Service question: what nearby OSM service environments are associated with high-volume destinations?
- CN: 服务环境问题：这些高频目的地附近对应什么 OSM 城市服务环境？
- EN: Use “end station as destination proxy.”
- CN: 使用“还车站点作为目的地 proxy”。

## Slide 2: Why This Is a Spatial Mobility Problem

**Main message / 主要信息:** The project connects trip behavior, return locations, and nearby services. / 项目把 trip 行为、还车地点和附近服务环境连接起来。

**Figure/table to use / 使用内容:** Project overview pipeline text.

**Rubric fit / 对应评分:** Problem & Solution.

**Slide content / 幻灯片内容:**

- EN: Raw Divvy trips alone do not answer the service-access question.
- CN: 原始 Divvy trips 本身不能回答 service access 问题。
- EN: The key spatial unit is the end station.
- CN: 核心空间单位是还车站点。
- EN: The key temporal split is weekday versus weekend.
- CN: 核心时间分层是 weekday versus weekend。
- EN: OSM adds the nearby service environment layer.
- CN: OSM 加入站点附近服务环境这一层。

## Slide 3: Data Sources

**Main message / 主要信息:** The analysis uses Divvy trips, station coordinates, OSM POIs, and weather as a secondary check. / 分析使用 Divvy trips、站点坐标、OSM POIs，weather 只是辅助检查。

**Figure/table to use / 使用内容:** Data Sources markdown cell.

**Rubric fit / 对应评分:** Data Pipeline.

**Slide content / 幻灯片内容:**

- EN: Raw Divvy trip records provide dates, station fields, and coordinates; the cleaned analysis table includes duration and distance.
- CN: 原始 Divvy trip records 提供日期、站点字段和坐标；清洗后的分析表包含 duration 和 distance。
- EN: Station coordinates support mapping and OSM matching.
- CN: 站点坐标用于地图和 OSM 匹配。
- EN: OSM POIs describe nearby service environments.
- CN: OSM POIs 描述站点附近服务环境。
- EN: Weather is only a secondary robustness check.
- CN: Weather 只是 secondary robustness check。

## Slide 4: Cleaning and Spatial Filtering

**Main message / 主要信息:** Cleaning makes the data usable for time, station, and spatial analysis. / 清洗让数据可以用于时间、站点和空间分析。

**Figure/table to use / 使用内容:** Cleaning table from `outputs/cleaning_summary.csv`.

**Rubric fit / 对应评分:** Data Pipeline.

**Slide content / 幻灯片内容:**

- EN: Original rows: 5,552,994; final rows: 5,547,168.
- CN: 原始行数 5,552,994；最终行数 5,547,168。
- EN: Coordinate filter removed 5,535 rows.
- CN: 坐标过滤移除了 5,535 行。
- EN: Duration filter removed 238 rows.
- CN: Duration 过滤移除了 238 行。
- EN: Spatial filtering matters because incorrect coordinates would affect heatmaps and OSM matching.
- CN: 空间过滤很重要，因为错误坐标会影响 heatmap 和 OSM matching。

## Slide 5: Full Data Pipeline

**Main message / 主要信息:** The pipeline turns raw trips into a defendable station-level service profile. / Pipeline 把 raw trips 转成可解释、可 defend 的站点级服务 profile。

**Figure/table to use / 使用内容:** Pipeline text from the clean notebook or guide.

**Rubric fit / 对应评分:** Data Pipeline.

**Slide content / 幻灯片内容:**

- EN: Clean trips and assign weekday/weekend labels.
- CN: 清洗 trips，并标记 weekday/weekend。
- EN: Aggregate trips by return station.
- CN: 按还车站点聚合 trips。
- EN: Normalize station shares so weekday volume does not dominate.
- CN: Normalize station share，避免 weekday 总量更大造成误导。
- EN: Match stations to nearby OSM service categories.
- CN: 把站点匹配到附近 OSM service categories。

## Slide 6: Experimental Setup and Destination-Service Profiling Formula

**Main message / 主要信息:** The method compares weighted nearby service profiles, not raw counts. / 方法比较的是加权服务环境 profile，不是 raw count。

**Figure/table to use / 使用内容:** Destination-Service Profiling Framework formula.

**Rubric fit / 对应评分:** Experimental Setup.

**Slide content / 幻灯片内容:**

- EN: Variables: day type, end station, return count, station share, OSM service vector.
- CN: 变量包括 day type、end station、return count、station share、OSM service vector。
- EN: Main setting: Top100 union, 250m radius, excluding `other_amenity`, covered stations only.
- CN: 主设置：Top100 union、250m radius、排除 `other_amenity`、只用 covered stations。
- EN: Formula: profile = sum of station share times station service vector.
- CN: 公式：profile = station share 和 station service vector 的加权和。
- EN: 250m is a modeling choice, and sensitivity checks show scale matters.
- CN: 250m 是 modeling choice，sensitivity checks 显示 scale matters。

## Slide 7: Baseline Results

**Main message / 主要信息:** Trip-only weekday/weekend differences exist, but they do not explain nearby service environments. / Trip-only 分析能说明 weekday/weekend 不同，但不能解释附近服务环境。

**Figure/table to use / 使用内容:** Baseline duration/distance table and Top20 overlap table.

**Rubric fit / 对应评分:** Results.

**Result structure / 结果页结构:**

1. EN: The figure is designed to show whether weekday and weekend trips differ before OSM services are added.
   CN: 这张图/表用于展示加入 OSM 前，weekday 和 weekend trip 是否已经不同。
2. EN: Weekend mean duration is 17.15 min versus 13.47 min on weekdays; weekend mean distance is 2.27 km versus 2.18 km.
   CN: Weekend 平均 duration 是 17.15 min，weekday 是 13.47 min；weekend 平均 distance 是 2.27 km，weekday 是 2.18 km。
3. EN: Top20 overlap is 11 stations, or 55%.
   CN: Top20 overlap 是 11 个站，也就是 55%。
4. EN: This supports deeper end-location analysis, but it does not explain service access.
   CN: 这支持继续分析 end-location，但不能解释 service access。

## Slide 8: Normalized Spatial Heatmaps

**Main message / 主要信息:** Normalized maps show where weekday and weekend destination patterns differ. / Normalized maps 显示 weekday 和 weekend 目的地模式在哪里不同。

**Figure/table to use / 使用内容:** `figures/final_clean/weekday_weekend_normalized_destination_heatmaps.png` and `figures/final_clean/weekend_minus_weekday_destination_difference_map.png`.

**Rubric fit / 对应评分:** Results.

**Result structure / 结果页结构:**

1. EN: The figure is designed to show spatial differences after correcting for larger weekday volume.
   CN: 这张图用于在修正 weekday 总量更大后，看空间差异。
2. EN: Weekend-oriented stations appear around lakefront and tourism areas; weekday-oriented stations appear around downtown commute areas.
   CN: Weekend-oriented 站点更多在 lakefront/tourism 区域；weekday-oriented 站点更多在 downtown commute 区域。
3. EN: This supports the research question by showing where the end-station pattern differs.
   CN: 它通过说明差异在哪里来支持研究问题。
4. EN: It does not prove rider intent or final activity.
   CN: 它不能证明 rider intent 或最终活动。

## Slide 9: Main OSM Service Profile Result

**Main message / 主要信息:** Weekend-weighted destinations are more tourism-associated, while weekday-weighted destinations are more food_drink and office-associated. / Weekend 加权目的地更偏 tourism，weekday 加权目的地更偏 food_drink 和 office。

**Figure/table to use / 使用内容:** `figures/final_clean/weekend_minus_weekday_service_difference.png` and `outputs/final_clean/weekday_weekend_service_profile_comparison.csv`.

**Rubric fit / 对应评分:** Results.

**Result structure / 结果页结构:**

1. EN: The figure is designed to show whether weekday and weekend destination stations have different nearby OSM service profiles.
   CN: 这张图用于展示 weekday 和 weekend 目的地站点附近 OSM service profile 是否不同。
2. EN: Tourism difference is +0.0355, weekend-oriented. Food_drink is -0.0436 and office is -0.0135, weekday-oriented.
   CN: Tourism difference 是 +0.0355，偏 weekend；food_drink 是 -0.0436，office 是 -0.0135，偏 weekday。
3. EN: Transit is +0.0248, but descriptive only because the bootstrap CI crosses zero.
   CN: Transit 是 +0.0248，但因为 bootstrap CI 跨 0，只能描述性提。
4. EN: This does not prove riders definitely went to tourist places.
   CN: 这不能证明 riders 一定去了旅游地点。

## Slide 10: Validation

**Main message / 主要信息:** Validation is mixed but transparent: no overall significance claim, but structured evidence supports the main exploratory pattern. / Validation 是 mixed but transparent：不能说整体显著，但结构性证据支持主 exploratory pattern。

**Figure/table to use / 使用内容:** `figures/final_clean/shuffle_test_plot.png`, `figures/final_clean/station_demand_randomization_plot.png`, `figures/final_clean/station_service_permutation_plot.png`, `figures/final_clean/bootstrap_service_category_ci.png`, and `figures/final_clean/topk_radius_l1_heatmap.png`.

**Rubric fit / 对应评分:** Results and Delivery & Q&A.

**Result structure / 结果页结构:**

1. EN: The figures are designed to test whether the pattern is random, stable, or too dependent on one setting.
   CN: 这些图用于检查 pattern 是不是随机、是否稳定、是否太依赖某一个设置。
2. EN: Label shuffle p = 0.2657, so do not claim overall statistical significance.
   CN: Label shuffle p = 0.2657，所以不能 claim overall statistical significance。
3. EN: Station-demand randomization p = 0.0010 and station-service permutation p = 0.0010.
   CN: Station-demand randomization p = 0.0010，station-service permutation p = 0.0010。
4. EN: Sensitivity checks show scale matters, so 250m is a modeling choice.
   CN: Sensitivity checks 显示 scale matters，所以 250m 是 modeling choice。

## Slide 11: Limitations

**Main message / 主要信息:** The limitations define the safe claim. / Limitation 决定我们能安全说什么。

**Figure/table to use / 使用内容:** Discussion and Limitations markdown cell and `outputs/final_clean/osm_coverage_bias_summary.csv`.

**Rubric fit / 对应评分:** Delivery & Q&A.

**Result structure / 结果页结构:**

1. EN: The slide is designed to show what the project cannot prove.
   CN: 这一页用于说明项目不能证明什么。
2. EN: End station is a destination proxy, not exact rider activity.
   CN: End station 是 destination proxy，不是 rider 的精确活动地点。
3. EN: OSM coverage is incomplete; Top100 covered return share is 63.63%.
   CN: OSM coverage 不完整；Top100 covered return share 是 63.63%。
4. EN: Weather is not the main result; rain-effect L1 is about 0.0089.
   CN: Weather 不是主结果；rain-effect L1 大约是 0.0089。

## Slide 12: Final Claim and Q&A

**Main message / 主要信息:** The final claim is careful: exploratory spatial association, not causal proof. / 最终结论要谨慎：exploratory spatial association，不是 causal proof。

**Figure/table to use / 使用内容:** Conclusion markdown cell and final validation decision summary.

**Rubric fit / 对应评分:** Delivery & Q&A.

**Slide content / 幻灯片内容:**

- EN: Weekday and weekend high-volume Divvy return destinations differ spatially.
- CN: Divvy 工作日和周末高频还车目的地在空间上不同。
- EN: Weekend-weighted destinations are more tourism-associated.
- CN: Weekend 加权目的地更偏 tourism。
- EN: Weekday-weighted destinations are more food_drink and office-associated.
- CN: Weekday 加权目的地更偏 food_drink 和 office。
- EN: This is an exploratory spatial association, not causal proof.
- CN: 这是 exploratory spatial association，不是 causal proof。

## Rubric Checklist

| Instructor requirement | Covered? | Slides |
|---|---|---|
| Problem & Solution | Yes | 1, 2 |
| Data Pipeline | Yes | 3, 4, 5 |
| Spatial outlier handling | Yes | 4 |
| Filtering, temporal stratification, aggregation | Yes | 4, 5, 6 |
| Experimental Setup | Yes | 6 |
| Variables, algorithms, baseline comparisons | Yes | 6, 7 |
| Results | Yes | 7, 8, 9, 10 |
| Each result slide says what the figure shows | Yes | 7, 8, 9, 10, 11 |
| Validation and sensitivity checks | Yes | 10 |
| Limitations | Yes | 11 |
| Delivery & Q&A | Yes | 12 and `presentation_qa_bilingual.md` |
