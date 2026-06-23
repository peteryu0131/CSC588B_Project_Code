# Divvy Final Project Clean Notebook Meeting Guide

这个文件是开会讲 `Divvy_Final_Project_Clean.ipynb` 用的中英对照版。它不是逐 cell 说明，而是按会议/答辩逻辑整理：先讲主线，再讲结果，最后讲 validation 和限制。

**Final submission / 最终提交**

| Item | What to do |
|---|---|
| Final notebook | Submit `notebooks/Divvy_Final_Project_Clean.ipynb` |
| Do not submit | `notebooks/Divvy_Final_Project_Merged_Notebook.ipynb` |
| Reason | Clean notebook 已完整执行；merged notebook 有旧路径和未完整执行风险 |

## 1. Core Story

**EN**

This project is not just a weekday/weekend trip-count comparison. It builds a spatial mobility pipeline to study whether high-volume Divvy return destinations differ between weekdays and weekends, and whether those destination stations are associated with different nearby OSM service environments.

**CN**

这个 project 不是简单比较 weekday/weekend trip count。它做的是一个 spatial mobility pipeline：先看工作日和周末的高频还车目的地是否不同，再看这些目的地附近的 OSM 城市服务环境是否不同。

**One-sentence version / 一句话版本**

EN: Weekday and weekend high-volume Divvy return destinations differ spatially; weekend-weighted destinations are more tourism-oriented, while weekday-weighted destinations are more food_drink/office-oriented, but the result must be framed as exploratory association rather than causal proof or overall statistical significance.

CN: Divvy 工作日和周末高频还车目的地在空间上不同；周末更偏 tourism，工作日更偏 food_drink/office；但结论必须说成 exploratory association，不是因果证明，也不是整体显著性证明。

## 2. Research Question And Claim Boundary

**Research question / 研究问题**

> How do weekday and weekend Divvy end-station patterns differ in Chicago, and what nearby urban service environments are associated with high-volume weekday and weekend destinations?

中文：

> 芝加哥 Divvy 工作日和周末的高频还车站点模式有什么不同？这些高频还车目的地附近对应什么样的城市服务环境？

**Claim boundary / 结论边界**

| Safe claim | Unsafe claim |
|---|---|
| End station is a destination proxy | End station proves the rider's final activity |
| OSM services describe nearby environment | OSM services caused rider behavior |
| Results are exploratory associations | Results are causal proof |
| Some category directions are stable | Overall profile difference is statistically significant |
| Weather is a secondary check | Weather explains the main pattern |

**中文重点**

- End station 只是 destination proxy，不是骑车人的最终活动地点。
- OSM POIs 说明站点周边环境，不证明 rider intent。
- 这是 exploratory spatial association，不是 prediction model，所以不要讲 accuracy。
- 不要说 “proved causal relationship” 或 “overall statistically significant”。

## 3. Pipeline

**Pipeline / 主流程**

```text
Divvy trips
-> cleaning and preprocessing
-> weekday/weekend temporal stratification
-> end-station aggregation
-> baseline duration/distance distributions
-> Top20 station overlap
-> normalized spatial heatmaps
-> coordinate-based OSM service profiles
-> Top100 main service-profile analysis
-> validation system
-> weather secondary check
-> discussion and limitations
```

**Why this meets the project requirement / 为什么这符合要求**

| Requirement | Where it appears |
|---|---|
| Specific spatial question | weekday/weekend end-station patterns + nearby OSM environments |
| Data pipeline | cleaning, filtering, temporal stratification, aggregation |
| Spatial processing | coordinate-based station-to-OSM matching |
| Results | overlap, heatmaps, OSM service profiles |
| Validation | shuffle, randomization, permutation, bootstrap, sensitivity, coverage |
| Discussion | limitations and careful final claims |

## 4. Data And Cleaning

**Data sources / 数据来源**

| Data | Purpose |
|---|---|
| Divvy trips | trip time, duration, distance, end station, coordinates |
| OSM POI cache | nearby service environment around stations |
| Weather data | secondary rainy/dry and cold/mild check |

**Cleaning result / 清洗结果**

| Stage | Rows |
|---|---:|
| Original rows | 5,552,994 |
| Final rows | 5,547,168 |

**Day-type volume / weekday 和 weekend 总量**

| Day type | Trip count | Share |
|---|---:|---:|
| Weekday | 3,970,986 | 71.59% |
| Weekend | 1,576,182 | 28.41% |

**Meeting point / 开会重点**

EN: Weekday trips are much more common, so raw weekday/weekend heatmaps are not directly comparable.

CN: 工作日 trip 总量明显更多，所以不能直接比较 raw heatmap。后面要用 normalized station share。

## 5. Baseline Findings

### 5.1 Duration And Distance

| Metric | Weekday mean | Weekend mean | Interpretation |
|---|---:|---:|---|
| Trip duration | 13.47 min | 17.15 min | Weekend trips are longer |
| Trip length | 2.18 km | 2.27 km | Weekend trips are slightly longer |

**Interpretation / 解释**

EN: Duration and distance confirm weekday/weekend behavior differs, but they do not explain what kinds of destinations riders return bikes to.

CN: Duration 和 distance 说明 weekday/weekend trip 行为不同，但不能解释目的地城市功能。所以后面要做 end-station 和 OSM service profile。

### 5.2 Top20 Station Overlap

| Metric | Value |
|---|---:|
| Weekday Top20 stations | 20 |
| Weekend Top20 stations | 20 |
| Union stations | 29 |
| Overlap stations | 11 |
| Overlap percentage | 55% |

**Interpretation / 解释**

EN: Only 11 stations overlap between weekday and weekend Top20 lists. High-volume weekday and weekend destinations are not identical.

CN: weekday Top20 和 weekend Top20 只有 11 个站重合，overlap 是 55%。这支持继续分析空间差异和附近服务环境。

## 6. Spatial Heatmaps

**Why normalized heatmaps / 为什么 normalize**

```text
weekday_station_share = weekday_return_count / total_weekday_returns
weekend_station_share = weekend_return_count / total_weekend_returns
difference = weekend_station_share - weekday_station_share
```

EN: This compares relative station importance within each day type instead of raw trip volume.

CN: 这样比较的是 station 在各自 day type 里的相对重要性，不是 raw volume。

**Heatmap result / Heatmap 结果**

| Weekend-oriented | Weekday-oriented |
|---|---|
| Navy Pier | Clinton St & Washington Blvd |
| DuSable Lake Shore Dr & Monroe St | Canal St & Madison St |
| Theater on the Lake | Clinton St & Jackson Blvd |
| Michigan Ave & Oak St | Franklin St & Monroe St |

**Meeting wording / 开会话术**

EN: The normalized heatmaps show lakefront/tourism stations are relatively weekend-oriented, while downtown commute stations are relatively weekday-oriented. The heatmaps answer where the pattern differs; OSM profiles answer what kinds of services are near those stations.

CN: Normalized heatmaps 显示 lakefront/tourism 站点更偏 weekend，downtown commute 站点更偏 weekday。Heatmap 回答 where，OSM profile 回答这些地方附近是什么服务环境。

## 7. OSM Service Profiling

**Service categories / 服务类别**

| Category | Meaning |
|---|---|
| `education` | school, university, library |
| `food_drink` | restaurant, cafe, bar, pub, fast food |
| `health` | hospital, clinic, doctors, pharmacy |
| `office` | office-related OSM tags |
| `recreation` | park, garden, fitness, sports, marina, playground |
| `retail` | shops |
| `tourism` | tourism-related OSM tags |
| `transit` | public transport, rail, subway, bus |
| `other_amenity` | mixed amenities: parking, bench, toilets, bank, vending machine |

**`other_amenity` decision / `other_amenity` 怎么处理**

EN: `other_amenity` is kept in raw outputs but excluded from the main interpreted profile because it is too heterogeneous.

CN: `other_amenity` 保留在 raw output 里，但不进入主解释性 profile，因为它太杂，不能清楚代表一种 destination function。

**Destination-Service Profiling formula / 方法公式**

```text
S_i = normalized OSM service vector for station i
w_i,weekday = weekday_return_count_i / sum(weekday_return_count)
w_i,weekend = weekend_return_count_i / sum(weekend_return_count)

P_weekday = sum_i w_i,weekday * S_i
P_weekend = sum_i w_i,weekend * S_i
D = P_weekend - P_weekday
```

Positive `D` = weekend-oriented service. Negative `D` = weekday-oriented service.

`D` 为正说明偏 weekend；`D` 为负说明偏 weekday。

**OSM coverage / OSM 覆盖**

| Analysis set | Union stations | Stations with OSM profile | Covered return share |
|---|---:|---:|---:|
| Top20 union | 29 | 24 | 85.27% |
| Top50 union | 72 | 45 | 68.56% |
| Top100 union | 129 | 75 | 63.63% |

**Why Top100 / 为什么主分析用 Top100**

EN: Top20 is easier to visualize, but Top100 is less dependent on a tiny station set. The tradeoff is lower OSM coverage, so coverage becomes a limitation.

CN: Top20 好画图、好解释，但样本小。Top100 更稳定，不容易被少数站点控制；代价是 OSM coverage 只有 63.63%，所以必须作为 limitation。

## 8. Main OSM Results

**Main setting / 主设置**

```text
Top100 weekday/weekend union
250m radius
excluding other_amenity
covered stations only
```

**Main result table / 主结果表**

| Service | Weekday | Weekend | Weekend - weekday | Direction |
|---|---:|---:|---:|---|
| `tourism` | 0.0772 | 0.1128 | +0.0355 | Weekend-oriented |
| `transit` | 0.3432 | 0.3680 | +0.0248 | Weekend-oriented, less stable |
| `retail` | 0.1729 | 0.1741 | +0.0011 | Very small |
| `education` | 0.0053 | 0.0046 | -0.0008 | Very small |
| `recreation` | 0.0093 | 0.0082 | -0.0011 | Very small, not weekend claim |
| `health` | 0.0168 | 0.0142 | -0.0026 | Weekday-oriented, small |
| `office` | 0.0449 | 0.0314 | -0.0135 | Weekday-oriented |
| `food_drink` | 0.3304 | 0.2868 | -0.0436 | Weekday-oriented |

**Strong results / 强结果**

- EN: `tourism` is the strongest weekend-oriented stable category.
- CN: `tourism` 是最强、最稳定的 weekend-oriented 类别。
- EN: `food_drink` is the strongest weekday-oriented category.
- CN: `food_drink` 是最强 weekday-oriented 类别。
- EN: `office` is weekday-oriented and stable, but smaller.
- CN: `office` 也是 weekday-oriented 且稳定，但效果小一些。

**Careful results / 谨慎结果**

- EN: `transit` is weekend-oriented descriptively, but bootstrap CI crosses zero.
- CN: `transit` 描述上偏 weekend，但 bootstrap CI 跨 0，所以不能作为强结论。
- EN: `recreation` is not a main weekend result in the Top100 profile.
- CN: `recreation` 在 Top100 主分析里不是 weekend 方向，不要作为主结论。

## 9. Validation: What Is Strong And What Is Weak

### 9.1 Validation Summary

| Test | Result | What it supports | What it does not support |
|---|---|---|---|
| Top20 overlap | 55% overlap | High-volume stations differ spatially | Does not explain service environment |
| Normalized heatmaps | lakefront/tourism weekend; downtown commute weekday | Spatial pattern differs | Does not prove rider intent |
| Label shuffle | p = 0.2657 | Descriptive difference only | No overall significance under this null |
| Station-demand randomization | p = 0.0010 | Real allocation is structured beyond station totals + global share | Does not prove OSM explains behavior |
| Station-service permutation | p = 0.0010 | Real station-service pairing is structured | Not causal proof |
| Bootstrap CI/FDR | tourism stable weekend; food_drink, office, health stable weekday | Category directions are partly stable | Does not make every category significant |
| Top-K sensitivity | Top20/50/100 keep tourism vs food_drink | Core direction stable across Top-K | Effect size can change |
| Radius sensitivity | 250m/500m tourism; 100m transit | Scale matters | No single radius is universal truth |
| OSM coverage | Top100 covered return share = 63.63% | Limitation is measured | Missing coverage remains |
| Weather | max L1 = 0.0089 | Weather effect is small | Weather is not main story |

### 9.2 Good Parts

**EN**

1. Top20 overlap is only 55%, so weekday/weekend high-volume destinations differ.
2. Heatmaps show a clear spatial split: lakefront/tourism weekend, downtown/commute weekday.
3. Main Top100 profile gives a clear direction: weekend tourism, weekday food_drink and office.
4. Station-demand randomization p = 0.0010 rules out a simple station-total + global-share allocation explanation.
5. Station-service permutation p = 0.0010 shows real station-service pairing is more structured than random assignment.
6. Bootstrap supports stable directions for `tourism`, `food_drink`, `office`, and `health`.
7. Top-K sensitivity keeps the core tourism vs food_drink direction across Top20, Top50, and Top100.

**CN**

1. Top20 overlap 只有 55%，说明 weekday/weekend 高频目的地不同。
2. Heatmaps 空间差异清楚：lakefront/tourism 偏 weekend，downtown/commute 偏 weekday。
3. Top100 主结果方向清楚：weekend = tourism，weekday = food_drink 和 office。
4. Station-demand randomization p = 0.0010，排除了简单 station total + global share 随机分配解释。
5. Station-service permutation p = 0.0010，说明真实 station-service pairing 比随机分配更有结构。
6. Bootstrap 支持 `tourism`、`food_drink`、`office`、`health` 的方向稳定。
7. Top-K sensitivity 中 Top20/50/100 都保持 tourism vs food_drink 核心方向。

### 9.3 Weak Or Limited Parts

**EN**

1. Label shuffle p = 0.2657, so do not claim overall statistical significance.
2. Transit is descriptive only because its bootstrap CI crosses zero.
3. Recreation should not be presented as the main weekend result.
4. Top100 OSM coverage is 63.63%, so missing coverage can bias the profile.
5. OSM services do not prove rider intent or exact destination.
6. Weather effect is small and stays secondary.
7. Radius and normalization choices affect some categories.

**CN**

1. Label shuffle p = 0.2657，所以不能 claim overall statistical significance。
2. Transit 只能描述性提，因为 bootstrap CI 跨 0。
3. Recreation 不要作为主要 weekend 结论。
4. Top100 OSM coverage 是 63.63%，missing coverage 可能影响 profile。
5. OSM services 不能证明 rider intent 或具体目的地。
6. Weather effect 很小，只能 secondary。
7. Radius 和 normalization 会影响部分类别。

## 10. Key Validation Details

**Label shuffle**

| Metric | Value |
|---|---:|
| Real difference score | 0.1231 |
| Shuffle mean | 0.1015 |
| Shuffle 95th percentile | 0.1783 |
| p-value | 0.2657 |

Meaning: no overall statistical significance under this null.

含义：在这个 null 下不能说整体显著。

**Station-demand randomization**

| Metric | Value |
|---|---:|
| Real difference score | 0.1231 |
| Randomization mean | 0.0010 |
| Randomization 95th percentile | 0.0018 |
| p-value | 0.0010 |
| Global weekday share | 0.7356 |

Meaning: station totals plus global weekday share do not explain the observed profile difference. This does not prove OSM services explain rider behavior.

含义：station total + global weekday share 不能解释观察到的 profile difference。但这不证明 OSM services 解释 rider behavior。

**Station-service permutation**

| Metric | Value |
|---|---:|
| Real difference score | 0.1231 |
| Permutation mean | 0.0366 |
| Permutation 95th percentile | 0.0642 |
| p-value | 0.0010 |

Meaning: real station-service pairing is more structured than random service-vector assignment.

含义：真实 station-service pairing 比随机 service-vector assignment 更有结构。

**Bootstrap category stability**

| Category | Observed diff | CI low | CI high | Final interpretation |
|---|---:|---:|---:|---|
| `tourism` | +0.0355 | +0.0133 | +0.0566 | Stable weekend |
| `food_drink` | -0.0436 | -0.0640 | -0.0210 | Stable weekday |
| `office` | -0.0135 | -0.0179 | -0.0091 | Stable weekday |
| `health` | -0.0026 | -0.0043 | -0.0005 | Stable weekday, small |
| `transit` | +0.0248 | -0.0021 | +0.0487 | Descriptive only |

Final stable directions: weekend = `tourism`; weekday = `food_drink`, `office`, `health`.

最终稳定方向：weekend = `tourism`；weekday = `food_drink`、`office`、`health`。

## 11. Weather Secondary Check

| Day type | Rain-effect L1 |
|---|---:|
| Weekday | 0.0089 |
| Weekend | 0.0085 |

**Meeting point / 开会重点**

EN: The weather effect is small compared with the main weekday/weekend destination-service difference. It is a secondary robustness check, not the main story.

CN: Weather effect 相比主 weekday/weekend destination-service difference 很小，所以它只是 secondary robustness check，不是主线。

## 12. Discussion And Limitations

| Limitation | Why it matters |
|---|---|
| End station proxy | Riders may walk after returning bikes |
| OSM nearby services | Describes station environment, not exact rider activity |
| Top100 coverage | Covered return share is 63.63%, not full coverage |
| 250m radius | A modeling choice; sensitivity shows scale matters |
| High-volume subset | Focuses on Top100 union, not all stations |
| Label shuffle | p = 0.2657, so no overall significance under that null |
| Weather labels | Daily-level weather is coarse and effect is small |

**How to say it / 怎么讲**

EN: These limitations do not invalidate the project. They define the correct claim: a cautious, exploratory spatial association.

CN: 这些限制不是说 project 失败，而是定义正确结论范围：谨慎的 exploratory spatial association。

## 13. Feedback Integration

这个 section 对应 rubric 里的 Feedback Integration。Notebook 里需要保留它，因为老师明确给了 10%。

| Feedback / rubric issue | How the notebook responds |
|---|---|
| Project cannot be only weekday/weekend descriptive comparison | Reframed as destination-service profiling using OSM service environments |
| Pipeline must be clear | Added explicit filtering, temporal stratification, aggregation, and saved outputs |
| Results need spatial evidence | Added normalized heatmaps and weekend-minus-weekday difference map |
| OSM matching should be defensible | Uses station coordinates and radius-based local OSM POI matching |
| Categories must be interpretable | Defines service categories and excludes heterogeneous `other_amenity` from main claims |
| Top20-only analysis is fragile | Uses Top100 as the main profile and checks Top20/50/100 sensitivity |
| Validation should be stronger | Adds label shuffle, station-demand randomization, station-service permutation, bootstrap, influence, coverage, and sensitivity checks |
| Conclusion should be careful | States label shuffle is not significant and frames result as exploratory association, not causality |

**开会怎么讲**

EN: We integrated feedback by moving from simple weekday/weekend summaries to a full destination-service profiling pipeline with spatial heatmaps, coordinate-based OSM matching, stronger validation, and more careful claims.

CN: 我们把反馈整合进 final notebook：从简单 weekday/weekend summary 扩展成 destination-service profiling pipeline，加了 spatial heatmaps、基于坐标的 OSM matching、更完整的 validation，并且把结论写得更谨慎。

## 14. Meeting Talk Track

Use this order if you need to present quickly.

开会可以直接按这个顺序讲。

1. **Goal / 目标**  
   EN: We study weekday/weekend high-volume return destinations and their nearby service environments.  
   CN: 我们研究 weekday/weekend 高频还车目的地，以及这些地方附近的服务环境。

2. **Pipeline / 流程**  
   EN: Clean trips, label weekday/weekend, aggregate end stations, map normalized spatial differences, build OSM profiles, validate.  
   CN: 清洗 trips、标记 weekday/weekend、聚合 end stations、做 normalized heatmaps、构建 OSM profiles、做 validation。

3. **Baseline / 基线**  
   EN: Weekend trips are longer, but the key baseline is Top20 overlap = 55%.  
   CN: Weekend trips 更长，但关键 baseline 是 Top20 overlap = 55%。

4. **Spatial result / 空间结果**  
   EN: Lakefront/tourism stations are more weekend-oriented; downtown commute stations are more weekday-oriented.  
   CN: Lakefront/tourism 更偏 weekend；downtown commute 更偏 weekday。

5. **OSM result / OSM 结果**  
   EN: Weekend-weighted destinations are more associated with tourism; weekday-weighted destinations are more associated with food_drink and office.  
   CN: 周末加权目的地更偏 tourism；工作日加权目的地更偏 food_drink 和 office。

6. **Validation good news / 好的 validation**  
   EN: Station-demand randomization and station-service permutation both have p = 0.0010; bootstrap supports stable service directions.  
   CN: Station-demand randomization 和 station-service permutation 都是 p = 0.0010；bootstrap 支持部分 service 方向稳定。

7. **Validation caution / 谨慎点**  
   EN: Label shuffle p = 0.2657, so no overall statistical significance claim.  
   CN: Label shuffle p = 0.2657，所以不能 claim overall statistical significance。

8. **Final claim / 最终说法**  
   EN: The result is exploratory, structured, and partly stable, but not causal.  
   CN: 结果是 exploratory、structured、partly stable，但不是 causality。

## 15. Q&A Defense Lines

**Q: Is this just visualization?**  
EN: No. Visualization is only one part. The notebook includes cleaning, temporal stratification, aggregation, coordinate-based OSM profiling, and validation.  
CN: 不是。Visualization 只是其中一部分；notebook 包含 cleaning、时间分层、聚合、坐标 OSM profiling 和 validation。

**Q: Did you prove weekend riders go to tourist places?**  
EN: No. We show weekend-weighted return stations are more associated with nearby tourism services. That is not individual intent proof.  
CN: 没有。我们只是显示周末加权还车站点附近更偏 tourism services，不证明个人目的。

**Q: Why exclude `other_amenity`?**  
EN: It is too broad and mixes unrelated amenities. It is useful for raw context but not for interpretation.  
CN: 它太杂，混合了很多无关 amenity；可以做 raw context，但不适合作主解释。

**Q: What is the strongest result?**  
EN: Weekend tourism versus weekday food_drink and office.  
CN: 最强结果是 weekend tourism vs weekday food_drink/office。

**Q: What is the weakest part?**  
EN: Label shuffle is not significant, and OSM coverage is incomplete.  
CN: 最弱的是 label shuffle 不显著，以及 OSM coverage 不完整。

**Q: Does station-demand randomization prove OSM explains behavior?**  
EN: No. It rejects a simple demand-allocation null; it does not prove causality.  
CN: 不证明。它只是排除一个简单 demand-allocation null，不证明因果。

**Q: Why is weather secondary?**  
EN: Rain-effect L1 is only about 0.0089, so the weather signal is small.  
CN: Rain-effect L1 只有约 0.0089，所以 weather signal 很小。

## 16. Safe Wording

**Say this / 可以说**

- EN: The results suggest an exploratory spatial association.
- CN: 结果显示探索性空间关联。
- EN: Weekend-weighted destinations are more associated with tourism in the covered Top100 station set.
- CN: 有覆盖的 Top100 站点中，周末加权目的地更偏 tourism。
- EN: Weekday-weighted destinations are more associated with food_drink and office.
- CN: 工作日加权目的地更偏 food_drink 和 office。
- EN: Validation is mixed but defendable.
- CN: Validation 不是完美，但可以 defend。

**Do not say this / 不要说**

- EN: We proved overall statistical significance.
- CN: 我们证明了整体显著。
- EN: OSM services caused riding behavior.
- CN: OSM services 导致骑行行为。
- EN: Riders definitely went to tourist places.
- CN: 骑车人一定去了景点。
- EN: Weather explains the main pattern.
- CN: Weather 解释主结果。
- EN: Recreation is the main weekend result.
- CN: Recreation 是主要 weekend 结果。

## 17. Files To Mention

**Final notebook**

- `notebooks/Divvy_Final_Project_Clean.ipynb`

**Key outputs**

- `outputs/final_clean/final_results_summary.csv`
- `outputs/final_clean/validation_overview.csv`
- `outputs/final_clean/final_validation_decision_summary.csv`
- `outputs/final_clean/weekday_weekend_service_profile_comparison.csv`
- `outputs/final_clean/bootstrap_service_category_stability.csv`
- `outputs/final_clean/osm_coverage_bias_summary.csv`

**Key figures**

- `figures/final_clean/weekday_weekend_normalized_destination_heatmaps.png`
- `figures/final_clean/weekend_minus_weekday_destination_difference_map.png`
- `figures/final_clean/weekend_minus_weekday_service_difference.png`
- `figures/final_clean/bootstrap_service_category_ci.png`
- `figures/final_clean/topk_radius_l1_heatmap.png`
