# Divvy Final Project Clean Notebook Meeting Guide

这个文件是开会讲 `Divvy_Final_Project_Clean.ipynb` 用的中英对照版。它不是逐 cell 说明，而是按会议/答辩逻辑整理：先讲主线，再讲结果，最后讲 validation 和限制。

**Final submission / 最终提交**

| Item | What to do |
|---|---|
| Final notebook | Submit `notebooks/Divvy_Final_Project_Clean.ipynb` |
| Do not submit | `notebooks/Divvy_Final_Project_Merged_Notebook.ipynb` |
| Reason | Clean notebook 已完整执行；merged notebook 有旧路径和未完整执行风险 |

## A. Read This First / 先读懂

这个 guide 的使用原则：先让组员听懂“我们在问什么、为什么这样做、结果说明什么”，再看公式、p-value 和细节。

**Project in plain words / 用最直白的话讲**

| Step | EN | CN |
|---|---|---|
| 1 | We look at where people return Divvy bikes on weekdays and weekends. | 我们先看工作日和周末大家把 Divvy 车还到哪里。 |
| 2 | We do not know each rider's final activity, so the return station is only a destination proxy. | 我们不知道骑车人下车后具体去哪，所以还车站只是目的地 proxy。 |
| 3 | We compare station importance within weekday and within weekend, not raw trip counts. | 我们比较每个站在 weekday/weekend 内部的重要性，不直接比原始数量。 |
| 4 | We use OSM POIs to describe what services are near those stations. | 我们用 OSM POIs 描述站点附近有什么城市服务。 |
| 5 | The main result is weekend = more tourism-associated, weekday = more food_drink/office-associated. | 主结果是 weekend 更偏 tourism，weekday 更偏 food_drink/office。 |
| 6 | The result is exploratory association, not proof of rider intent or causality. | 结论是探索性关联，不是证明 rider intent 或因果。 |

**How to read every section / 每一节怎么读**

| Section type | First question to ask | Good explanation style |
|---|---|---|
| Data | What data do we use, and why is it usable? | 先讲数据角色，再讲清洗数字。 |
| Method | What problem does this method solve? | 先讲为什么需要这个方法，再讲公式。 |
| Result | What changed between weekday and weekend? | 先讲方向，再讲具体数字。 |
| Validation | Why should we believe this result? | 先讲 test 问题，再讲 p-value。 |
| Limitation | What can we not claim? | 先讲边界，避免过度结论。 |

**The safest full-project sentence / 最安全总句**

EN: We find that weekday and weekend high-volume Divvy return destinations differ spatially and are associated with different nearby service environments, but this is an exploratory association, not a causal claim.

CN: 我们发现 Divvy 工作日和周末高频还车目的地在空间上不同，并且附近服务环境也不同；但这只是 exploratory association，不是因果证明。

## 0. Teacher Requirements From `Final_Project.pdf`

这一节是给组员统一口径用的。老师的要求不是“把图放出来讲一遍”，而是要求我们证明自己能完成一个完整的 spatial mobility research project：

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| The teacher wants a complete research story, not isolated charts. | 老师要的是一个完整研究故事，不是几张孤立的图。 |
| We need a clear problem, a defensible method, clear results, and honest limitations. | 我们需要清楚的问题、站得住的方法、明确的结果和诚实的限制。 |
| During presentation, every chart must answer: why did we make it, what does it show, and what does it not prove? | 演讲时每张图都要回答：为什么做、显示了什么、不能证明什么。 |
| The safest strategy is to explain first, then show numbers. | 最安全策略是先解释，再给数字。 |

```text
specific solvable spatial problem
-> mathematically/algorithmically defensible pipeline
-> spatial data preprocessing
-> movement / mobility pattern modeling
-> algorithm or heuristic evaluation
-> clear results
-> live defense and Q&A
```

**老师最看重的主线 / What the instructor is grading**

| Teacher wording | What it means for our project | How we answer it |
|---|---|---|
| Process unstructured spatial data | Divvy trips and OSM POIs are messy spatial data, not ready-made answers | Clean trips, filter invalid records, use end-station coordinates, match nearby OSM services |
| Extract meaningful behavioral phenotypes or system demands | We need describe a meaningful mobility pattern, not only count rides | Weekday destinations reflect commute/workday environment; weekend destinations reflect lakefront/tourism environment |
| Identify a specific, solvable spatial problem | The question must be narrow enough to solve with our data | We ask how weekday/weekend high-volume return destinations differ, and what nearby services are associated with them |
| Build a mathematically rigorous pipeline | Each step needs a defensible formula or rule | Normalized station shares, weighted OSM service profiles, Top-K/radius sensitivity, permutation/bootstrap validation |
| Empirically defend engineering choices | We cannot just say “we chose this because it looks good” | We defend Top100, 250m radius, excluding `other_amenity`, normalization, and validation tests |
| Present findings clearly | The audience must understand what each result proves | For each graph: say what it is meant to show, then say what it actually shows |

**Presentation rubric / 演讲评分 100 分**

| Category | Weight | What we must show | Our strongest evidence |
|---|---:|---|---|
| Problem & Solution | 20% | Clear problem and appropriate spatial/mobility solution | Research question + destination-service profiling framework |
| Data Pipeline | 20% | Detailed pipeline including spatial outliers, filtering, temporal stratification, aggregation | Cleaning, weekday/weekend labels, station aggregation, coordinate OSM matching |
| Experimental Setup | 20% | Variables, algorithms, baselines, and replicability | Day type, end station, normalized return share, OSM vectors, Top20 overlap baseline, validation null models |
| Results | 20% | Graphs/tables demonstrate results under stated conditions | Top20 overlap, normalized heatmaps, OSM profile differences, bootstrap CI, sensitivity heatmap |
| Delivery & Q&A | 20% | Clear speaking, pacing, slide design, direct answers | Use safe claim boundaries and Q&A lines in this guide |

**Important detail from paper rubric that also helps presentation**

老师对 results 的要求很明确：每张图都要先介绍它“supposed to demonstrate 什么”，再收尾说明它“demonstrates 什么”。所以演讲中每张图都按这个模板：

```text
This figure/table is designed to test/show ...
The key pattern is ...
Therefore, this supports ...
But it does not prove ...
```

中文模板：

```text
这张图/表的目的，是为了检验/展示 ...
最重要的 pattern 是 ...
所以它支持我们的哪个 claim ...
但是它不能证明 ...
```

**One-minute rubric answer / 一分钟回答老师要求**

EN: Our project identifies a specific spatial mobility problem: whether high-volume Divvy return destinations differ between weekdays and weekends, and whether those destinations are associated with different nearby OSM service environments. We build a reproducible pipeline from cleaned Divvy trips to weekday/weekend stratification, end-station aggregation, normalized spatial heatmaps, coordinate-based OSM service profiling, and multiple validation tests. The main result is that weekend-weighted destinations are more tourism-oriented, while weekday-weighted destinations are more food_drink and office-oriented. The conclusion is exploratory and associative, not causal.

CN: 我们的项目解决一个具体的 spatial mobility 问题：Divvy 工作日和周末的高频还车目的地是否不同，以及这些目的地附近的 OSM 城市服务环境是否不同。我们的 pipeline 从 Divvy trip 清洗开始，做 weekday/weekend 分层、end-station 聚合、normalized heatmap、基于坐标的 OSM service profiling，再用多种 validation 检查结果。主结果是 weekend 加权目的地更偏 tourism，weekday 加权目的地更偏 food_drink 和 office。结论是 exploratory association，不是因果证明。

## 1. Core Story

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| This project asks whether weekday and weekend bike-return destinations are different places with different nearby services. | 这个项目问的是：工作日和周末的还车目的地是不是不同？这些地方附近的城市服务是不是也不同？ |
| It is not mainly about whether weekdays have more trips. | 它不是主要问 weekday trip 是不是更多。 |
| The important idea is destination environment, not only trip volume. | 重点是目的地周边环境，不只是 trip 数量。 |

**EN**

This project is not just a weekday/weekend trip-count comparison. It builds a spatial mobility pipeline to study whether high-volume Divvy return destinations differ between weekdays and weekends, and whether those destination stations are associated with different nearby OSM service environments.

**CN**

这个 project 不是简单比较 weekday/weekend trip count。它做的是一个 spatial mobility pipeline：先看工作日和周末的高频还车目的地是否不同，再看这些目的地附近的 OSM 城市服务环境是否不同。

**One-sentence version / 一句话版本**

EN: Weekday and weekend high-volume Divvy return destinations differ spatially; weekend-weighted destinations are more tourism-oriented, while weekday-weighted destinations are more food_drink/office-oriented, but the result must be framed as exploratory association rather than causal proof or overall statistical significance.

CN: Divvy 工作日和周末高频还车目的地在空间上不同；周末更偏 tourism，工作日更偏 food_drink/office；但结论必须说成 exploratory association，不是因果证明，也不是整体显著性证明。

## 2. Research Question And Claim Boundary

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Research question = what spatial pattern are we trying to explain? | Research question 就是：我们到底要解释什么空间模式？ |
| Claim boundary = what we are allowed to say and what we must not overclaim. | Claim boundary 就是：哪些话可以说，哪些话说过头了。 |
| The safest claim is about station environments, not individual rider intentions. | 最安全的结论是讲站点周边环境，不讲个人真实目的。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Pipeline means the path from raw data to final claim. | Pipeline 就是从 raw data 到 final claim 的完整路线。 |
| Each step answers one smaller question. | 每一步回答一个更小的问题。 |
| If someone asks “what did you actually do?”, explain this pipeline. | 如果别人问“你们到底做了什么？”，就讲这个 pipeline。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Data cleaning makes sure the trips can be used for time, space, and station analysis. | 数据清洗是为了保证 trip 能用于时间、空间和站点分析。 |
| Bad coordinates are especially important because this is a spatial project. | 坐标错误特别重要，因为这是 spatial project。 |
| Weekday has more trips, so later comparisons must normalize volume. | Weekday trip 更多，所以后面必须 normalize，不能直接比 raw count。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Baseline results are the simple checks before the main OSM analysis. | Baseline 是主 OSM 分析前的简单检查。 |
| They show weekday/weekend behavior and station lists are not identical. | 它们说明 weekday/weekend 的骑行行为和高频站点不完全一样。 |
| Baseline motivates the main analysis, but it is not the final answer. | Baseline 是动机，不是最终答案。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Heatmaps answer “where are the weekday/weekend differences?” | Heatmap 回答的是：weekday/weekend 的空间差异在哪里？ |
| Normalization is needed because weekday has many more trips. | 因为 weekday trip 总量更多，所以必须 normalize。 |
| The map shows location difference, not rider intention. | 地图显示位置差异，不证明 rider intent。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| OSM profiling answers “what kind of places are near these stations?” | OSM profiling 回答的是：这些站附近是什么类型的地方？ |
| We turn nearby POIs into service categories like food, office, tourism, and transit. | 我们把附近 POI 变成 food、office、tourism、transit 等服务类别。 |
| This describes station environment, not the rider's exact destination. | 它描述站点周边环境，不是 rider 的精确目的地。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| This is the main answer to the research question. | 这是 research question 的主答案。 |
| Weekend-weighted stations are more tourism-associated. | Weekend 加权站点更偏 tourism。 |
| Weekday-weighted stations are more food_drink and office-associated. | Weekday 加权站点更偏 food_drink 和 office。 |
| The result is about association, not causality. | 这个结果是 association，不是 causality。 |

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

## 9. Validation: Simple Version

Validation 这一部分不要讲得像统计课。最直接的讲法是：

EN: Validation asks whether our result is believable, stable, and not just a random artifact.

CN: Validation 就是在问：我们的结果靠不靠谱？是不是稳定？是不是只是随机巧合？

**One-sentence summary / 一句话总结**

EN: The validation is mixed but useful: we cannot claim overall statistical significance, but several checks show the main tourism vs food_drink/office pattern is structured and partly stable.

CN: Validation 不是完美，但有用：我们不能说整体显著；但是多个检查显示 tourism vs food_drink/office 这个主方向有结构，而且部分稳定。

### 9.1 What Each Test Means

| Test | Plain question | Result | How to say it in presentation |
|---|---|---|---|
| Top20 overlap | Are weekday and weekend top stations the same? | 55% overlap | They are not identical, so spatial analysis is meaningful. |
| Normalized heatmaps | Where are the differences? | lakefront/tourism weekend; downtown commute weekday | The spatial pattern is different after normalizing trip volume. |
| Label shuffle | If weekday/weekend labels were random, is our overall difference unusually large? | p = 0.2657 | No. Do not claim overall statistical significance. |
| Station-demand randomization | Is the result only caused by station popularity and the larger weekday share? | p = 0.0010 | No. The observed profile has more structure than that simple explanation. |
| Station-service permutation | If we randomly assign service profiles to stations, do we still get this strong a result? | p = 0.0010 | No. Real station-service pairing is structured. |
| Bootstrap CI/FDR | Are individual service directions stable? | tourism weekend; food_drink, office, health weekday | The strongest category directions are stable. |
| Top-K sensitivity | Does the result disappear if we use Top20/Top50/Top100? | core tourism vs food_drink remains | The main direction is not only a Top100 accident. |
| Radius sensitivity | Does the result depend on 100m/250m/500m radius? | scale matters | The exact size changes, so radius is a limitation. |
| OSM coverage | How much of Top100 has usable OSM data? | 63.63% covered return share | Missing OSM coverage is a measured limitation. |
| Weather | Does rain/cold explain the main pattern? | max L1 = 0.0089 | Weather effect is small and secondary. |

### 9.2 中英对照讲法

| Point | EN | CN |
|---|---|---|
| What validation is for | Validation checks whether the result is believable, not whether we built a prediction model. | Validation 是检查结果靠不靠谱，不是检查 prediction accuracy。 |
| Strong evidence | Station-demand randomization and station-service permutation both have p = 0.0010. | Station-demand randomization 和 station-service permutation 都是 p = 0.0010，是比较强的支持。 |
| Stable categories | Bootstrap supports `tourism` as weekend-oriented and `food_drink`/`office` as weekday-oriented. | Bootstrap 支持 `tourism` 偏 weekend，`food_drink`/`office` 偏 weekday。 |
| Main caution | Label shuffle p = 0.2657, so we cannot claim overall statistical significance. | Label shuffle p = 0.2657，所以不能说整体显著。 |
| Limitation | OSM coverage and radius choice can affect the result. | OSM 覆盖和半径选择会影响结果，所以要当作 limitation。 |
| Final defense | The result is structured and partly stable, but exploratory and not causal. | 结果有结构、部分稳定，但仍然是 exploratory，不是因果证明。 |

### 9.3 Good News And Bad News

**Good news / 好消息**

| EN | CN |
|---|---|
| Top20 overlap is only 55%, so weekday/weekend high-volume destinations differ. | Top20 overlap 只有 55%，说明 weekday/weekend 高频目的地不同。 |
| Heatmaps show a clear spatial split. | Heatmap 显示空间差异清楚。 |
| Main OSM profile says weekend is more tourism-associated; weekday is more food_drink/office-associated. | 主 OSM profile 显示 weekend 更偏 tourism，weekday 更偏 food_drink/office。 |
| Randomization/permutation p-values are 0.0010, so the pattern is not easily explained by simple randomness. | Randomization/permutation 的 p-value 是 0.0010，说明结果不是简单随机就能解释。 |
| Bootstrap supports the main category directions. | Bootstrap 支持主要类别方向。 |

**Bad news / 谨慎点**

| EN | CN |
|---|---|
| Label shuffle is not significant. | Label shuffle 不显著。 |
| Transit is descriptive only because its CI crosses zero. | Transit 的 CI 跨 0，只能描述性提。 |
| Recreation is not a main weekend result. | Recreation 不是主要 weekend 结论。 |
| OSM coverage is incomplete. | OSM coverage 不完整。 |
| OSM and end stations do not prove rider intent. | OSM 和还车站点不能证明 rider 的真实目的。 |

## 10. Key Validation Details In Plain Language

### 10.1 Label shuffle

**Simple idea / 简单理解**

EN: Imagine we randomly mix up which trips are weekday and weekend. If our real result is much stronger than those random mixes, then the overall difference would look statistically strong.

CN: 想象我们把 weekday/weekend 标签随机打乱。如果真实结果比随机打乱后的结果强很多，就说明整体差异很强。

| Metric | Value |
|---|---:|
| Real difference score | 0.1231 |
| Shuffle mean | 0.1015 |
| Shuffle 95th percentile | 0.1783 |
| p-value | 0.2657 |

**Direct interpretation / 直接解释**

EN: p = 0.2657 is not small. So this test does not support an overall significance claim.

CN: p = 0.2657 不小。所以这个 test 不支持“整体显著”。

**Say / 可以说**

EN: Label shuffle is our caution result.

CN: Label shuffle 是我们的谨慎点。

**Do not say / 不要说**

EN: We proved the whole profile difference is statistically significant.

CN: 不要说我们证明了整体 profile difference 显著。

### 10.2 Station-demand randomization

**Simple idea / 简单理解**

EN: This test asks: maybe the result only happens because some stations are popular and weekdays have more trips overall. If we keep station popularity but randomly assign weekday/weekend demand, do we still get our result?

CN: 这个 test 问的是：我们的结果会不会只是因为有些站本来就热门，而且 weekday 总量本来就更大？如果保留每个站的总热度，但随机分配 weekday/weekend，还会不会得到这么强的结果？

| Metric | Value |
|---|---:|
| Real difference score | 0.1231 |
| Randomization mean | 0.0010 |
| Randomization 95th percentile | 0.0018 |
| p-value | 0.0010 |
| Global weekday share | 0.7356 |

**Direct interpretation / 直接解释**

EN: p = 0.0010 is very small. Station popularity plus the global weekday share cannot explain the observed difference.

CN: p = 0.0010 很小。只靠“站点热门程度 + weekday 总量更大”解释不了我们的结果。

**Important boundary / 边界**

EN: This does not prove OSM causes rider behavior.

CN: 这不证明 OSM 导致骑行行为。

### 10.3 Station-service permutation

**Simple idea / 简单理解**

EN: This test asks: what if we randomly attach service profiles to stations? If random station-service matching cannot recreate our result, then the real station-service pairing has structure.

CN: 这个 test 问的是：如果把每个站附近的 service profile 随机分配给别的站，还能不能得到这么强的差异？如果不能，说明真实的 station-service pairing 是有结构的。

| Metric | Value |
|---|---:|
| Real difference score | 0.1231 |
| Permutation mean | 0.0366 |
| Permutation 95th percentile | 0.0642 |
| p-value | 0.0010 |

**Direct interpretation / 直接解释**

EN: p = 0.0010. Real stations and their nearby services are not randomly interchangeable.

CN: p = 0.0010。真实站点和附近服务不是随便随机配对也能得到同样结果。

### 10.4 Bootstrap category stability

**Simple idea / 简单理解**

EN: Bootstrap asks: if we repeatedly resample stations, do the service-category directions stay the same?

CN: Bootstrap 问的是：如果我们反复抽样站点，service category 的方向还稳不稳定？

| Category | Observed diff | CI low | CI high | Final interpretation |
|---|---:|---:|---:|---|
| `tourism` | +0.0355 | +0.0133 | +0.0566 | Stable weekend |
| `food_drink` | -0.0436 | -0.0640 | -0.0210 | Stable weekday |
| `office` | -0.0135 | -0.0179 | -0.0091 | Stable weekday |
| `health` | -0.0026 | -0.0043 | -0.0005 | Stable weekday, small |
| `transit` | +0.0248 | -0.0021 | +0.0487 | Descriptive only |

**Direct interpretation / 直接解释**

EN: If the confidence interval stays above zero, it is stable weekend-oriented. If it stays below zero, it is stable weekday-oriented. If it crosses zero, be careful.

CN: 如果 CI 全在 0 以上，就是稳定偏 weekend；如果全在 0 以下，就是稳定偏 weekday；如果跨过 0，就要谨慎。

**Final stable directions / 最终稳定方向**

EN: Weekend = `tourism`; weekday = `food_drink`, `office`, `health`.

CN: Weekend = `tourism`；weekday = `food_drink`、`office`、`health`。

### 10.5 Sensitivity checks

**Simple idea / 简单理解**

EN: Sensitivity checks ask whether the result depends too much on one design choice.

CN: Sensitivity checks 问的是：结果是不是太依赖某一个设置？

| Choice checked | What we learned |
|---|---|
| Top20 / Top50 / Top100 | tourism vs food_drink direction remains the core pattern |
| 100m / 250m / 500m radius | radius affects details, so scale matters |
| service normalization | main interpretation should stay cautious |
| category inclusion | `other_amenity` is too mixed for the main claim |

**Direct interpretation / 直接解释**

EN: The main direction is not based on only one setting, but exact effect sizes can change.

CN: 主方向不是只靠一个设置才出现，但具体 effect size 会变化。

## 11. Weather Secondary Check

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Weather is not the main research question. | Weather 不是主研究问题。 |
| We only use it to check whether rain/cold could explain the main pattern. | 我们只是检查 rain/cold 会不会解释主 pattern。 |
| The weather effect is small, so it stays secondary. | Weather effect 很小，所以只能当 secondary check。 |

| Day type | Rain-effect L1 |
|---|---:|
| Weekday | 0.0089 |
| Weekend | 0.0085 |

**Meeting point / 开会重点**

EN: The weather effect is small compared with the main weekday/weekend destination-service difference. It is a secondary robustness check, not the main story.

CN: Weather effect 相比主 weekday/weekend destination-service difference 很小，所以它只是 secondary robustness check，不是主线。

## 12. Discussion And Limitations

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| Limitations are not failures. They define what we can safely claim. | Limitation 不是失败，而是告诉我们哪些结论可以安全地说。 |
| The biggest boundary is that end stations and OSM services do not prove rider intent. | 最大边界是：还车站点和 OSM 服务不能证明 rider 的真实目的。 |
| A good presentation says the limitation clearly before being asked. | 好的演讲要主动讲 limitation，不要等老师问。 |

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

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| This section shows how the final notebook improved after feedback. | 这一节说明 final notebook 如何根据反馈改进。 |
| It matters because the rubric gives feedback integration 10%. | 它重要是因为 rubric 里 Feedback Integration 占 10%。 |
| The key improvement is moving from simple weekday/weekend summaries to a full destination-service pipeline. | 关键改进是从简单 weekday/weekend summary 变成完整 destination-service pipeline。 |

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
   EN: Two validation checks are strong: station-demand and station-service tests both have p = 0.0010. Bootstrap also supports the main category directions.
   CN: 有两个 validation 很强：station-demand 和 station-service tests 都是 p = 0.0010。Bootstrap 也支持主要类别方向。

7. **Validation caution / 谨慎点**  
   EN: Label shuffle p = 0.2657, so we should not say the whole profile is statistically significant.
   CN: Label shuffle p = 0.2657，所以不能说整个 profile 统计显著。

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

## 18. Rubric-Aligned Presentation Structure

**Plain meaning / 先读懂**

| EN | CN |
|---|---|
| This section is the presentation order. | 这一节就是演讲顺序。 |
| Use it when deciding who says what. | 分配组员演讲内容时看这里。 |
| The order follows the teacher's grading categories. | 顺序直接对应老师评分项。 |

如果组员不知道怎么组织演讲，就按这个结构。它直接对应老师 presentation rubric 的 5 个 20%。

| Order | Rubric category | Suggested time | What to show | Main sentence |
|---:|---|---:|---|---|
| 1 | Problem & Solution | 1-2 min | Research question, hypothesis, pipeline overview | We solve a specific spatial mobility question using destination-service profiling. |
| 2 | Data Pipeline | 2-3 min | Cleaning summary, weekday/weekend labels, station aggregation, OSM matching | The pipeline converts raw trips and OSM POIs into comparable station-level service profiles. |
| 3 | Experimental Setup | 2 min | Variables, baselines, formulas, Top100/250m setting | The experiment compares normalized weekday/weekend return demand, not raw trip volume. |
| 4 | Results | 3-4 min | Top20 overlap, heatmaps, OSM profile, validation figures | Weekend destinations are more tourism-associated; weekday destinations are more food_drink/office-associated. |
| 5 | Delivery & Q&A | throughout + final 1 min | Limitations, safe wording, answers | The result is exploratory, structured, and partly stable, but not causal. |

**Recommended slide order / 推荐 slide 顺序**

| Slide | Title | Why this slide exists | What to say |
|---:|---|---|---|
| 1 | Title + Research Question | Set the problem clearly | “We study weekday/weekend Divvy end-station patterns and nearby OSM service environments.” |
| 2 | Why This Is Spatial Mobility | Prove it is not simple descriptive counting | “The spatial unit is the return station; the temporal split is weekday vs weekend; the environmental layer is OSM services.” |
| 3 | Data Sources | Show what data supports the analysis | “Divvy gives trips and station coordinates. OSM gives nearby service context. Weather is secondary.” |
| 4 | Cleaning And Preprocessing | Hit Data Pipeline rubric | “We filter timestamps, coordinates, duration, distance, spatial bounds, and invalid records.” |
| 5 | Experimental Setup | Hit reproducibility rubric | “Variables, baselines, Top-K, radius, and formulas are defined before results.” |
| 6 | Baseline Results | Show weekday/weekend behavior differs | “Weekend trips are longer; Top20 station overlap is only 55%.” |
| 7 | Normalized Heatmaps | Show spatial difference | “Lakefront/tourism stations are more weekend-oriented; downtown commute stations are more weekday-oriented.” |
| 8 | OSM Service Profiling Method | Explain main algorithm | “For each station, we build a normalized OSM vector, then weight stations by return share.” |
| 9 | Main OSM Result | Present key finding | “Tourism is weekend-oriented; food_drink and office are weekday-oriented.” |
| 10 | Validation | Defend engineering choices | “Validation is mixed but defendable: some tests are strong, label shuffle is not significant.” |
| 11 | Limitations | Show academic honesty | “End station is a proxy; OSM does not prove intent; coverage is incomplete.” |
| 12 | Final Claim | Close safely | “We find an exploratory spatial association, not a causal claim.” |

**If the presentation is short / 如果时间短**

Use 8 slides: question, data/pipeline, experimental setup, baseline, heatmap, OSM result, validation, conclusion.

**If the presentation is long / 如果时间够**

Use 12 slides and give separate slides for cleaning, OSM method, validation, and limitations.

## 19. How To Explain The Project To Group Members

这一节是中文讲解版。目标是让组员不仅会背结论，还能理解为什么每一步存在。

### 19.1 Plain-language story / 大白话版本

我们不是在问“周末骑车多还是工作日骑车多”。这个问题太普通，也不够 spatial。我们真正问的是：

```text
人在工作日和周末，最后把 Divvy 车还到哪些地方？
这些还车地点周围的城市服务环境有什么不同？
```

Divvy 数据不知道每个人下车后到底去了哪里。所以我们不能说“这个人去了景点”或“这个人去了办公室”。我们只能说：

```text
end station = destination proxy
nearby OSM services = station environment
```

也就是说，还车站点是“目的地区域”的 proxy，OSM 服务是“附近城市功能”的 proxy。

所以最终 claim 只能是：

```text
weekday/weekend return destinations are associated with different nearby service environments
```

不能说：

```text
weekday/weekend riders definitely have different personal purposes
```

### 19.2 Technical story / 技术版本

技术上，我们把问题拆成 4 层：

| Layer | Question | Method |
|---|---|---|
| Trip layer | 每条 trip 是 weekday 还是 weekend？trip duration/distance 有没有差异？ | clean data, label day type, summarize duration/distance |
| Station layer | 高频还车站点是否相同？ | aggregate by end station, compare Top20 overlap |
| Spatial layer | 差异在哪里？ | normalized station share, heatmaps, weekend-minus-weekday map |
| Service layer | 这些地方附近是什么服务环境？ | coordinate-based OSM matching, service vectors, weighted profiles |

这样设计的好处是每一层回答一个更具体的问题：

```text
trip behavior differs
-> station destinations differ
-> spatial locations differ
-> nearby service environments differ
```

### 19.3 Defense story / 答辩版本

老师可能会问：“为什么这不是简单画图？”

回答：

EN: The maps are only one output. The analytical pipeline includes cleaning, temporal stratification, station aggregation, normalized spatial comparison, coordinate-based OSM service profiling, and validation with multiple null models and sensitivity tests.

CN: 地图只是一个输出。真正的分析 pipeline 包含数据清洗、weekday/weekend 时间分层、站点聚合、normalized spatial comparison、基于坐标的 OSM service profiling，以及多个 null model 和 sensitivity test。

## 20. Key Concepts The Team Must Understand

### 20.1 Destination proxy

**Meaning**

`end_station_name` 和 `end_lat/end_lng` 代表用户还车位置。它不是用户最终目的地，只是一个合理 proxy。

**Why it matters**

如果我们说“riders went to tourist attractions”，这就太强了，因为还车后用户可能走路、坐公交、去别的地方。正确说法是“return stations are near tourism services”。

**Safe wording**

EN: End stations are used as destination proxies.

CN: 我们把还车站点当作目的地区域的 proxy。

### 20.2 Temporal stratification

**Meaning**

把 trips 分成 weekday 和 weekend。

**Why it matters**

老师 rubric 里明确提到 temporal stratification。我们不能只把所有 trip 混在一起，否则看不到工作日和周末模式差异。

**Our variable**

```text
day_type = weekday or weekend
```

### 20.3 Spatial outliers and filtering

**Meaning**

空间数据会有错误坐标、缺失坐标、超出 Chicago 合理范围的坐标、异常速度等问题。如果不处理，地图和 station aggregation 会被污染。

**Notebook checks**

| Check | Why |
|---|---|
| missing end station | 没有目的地，不能做 end-station analysis |
| missing coordinates | 没有坐标，不能 map 或 OSM matching |
| invalid dates | 不能分 weekday/weekend 或合并 weather |
| non-positive durations | duration 不合理 |
| negative trip lengths | distance 不合理 |
| unrealistic straight-line speeds | 可能是错误记录或异常值 |
| Chicago coordinate bounds | 排除不在芝加哥合理范围内的空间点 |

**Cleaning numbers to mention**

| Step | Rows after step | Removed at step |
|---|---:|---:|
| Original rows | 5,552,994 | - |
| After timestamp filter | 5,552,994 | 0 |
| After 2025 started_at filter | 5,552,941 | 53 |
| After coordinate filter | 5,547,406 | 5,535 |
| After duration filter | 5,547,168 | 238 |
| After distance filter | 5,547,168 | 0 |

**How to explain**

CN: Data Pipeline 这部分一定要讲，因为老师给了 20%。我们不是直接拿 raw data 画图，而是先排除无法用于空间分析或时间分析的记录。最主要被过滤的是坐标问题，coordinate filter 移除了 5,535 行，duration filter 又移除了 238 行。最后保留 5,547,168 行。

### 20.4 Aggregation

**Meaning**

把 trip-level data 聚合到 station-level。

```text
many trips -> one end station summary
```

**Why it matters**

OSM 服务是站点附近的环境，不是每条 trip 自己的属性。所以主分析单位必须从 trip 转为 station。

**Example**

如果 Navy Pier 有很多 weekend returns，那么 Navy Pier 在 weekend profile 里的权重会更大。

### 20.5 Normalized station share

**Problem**

weekday trip 总量远大于 weekend。如果直接比较 raw counts，weekday 几乎一定更大。

**Solution**

```text
weekday_station_share = weekday_return_count / total_weekday_returns
weekend_station_share = weekend_return_count / total_weekend_returns
```

**Meaning**

我们比较的是“这个站在 weekday 内部重要不重要”和“这个站在 weekend 内部重要不重要”，而不是比较绝对数量。

### 20.6 OSM service vector

**Meaning**

每个站点附近 250m 内的 OSM POIs 被分类成服务类别，例如：

```text
food_drink, office, tourism, transit, retail, health, education, recreation
```

然后变成一个 normalized vector。

**Example**

如果某站附近主要是 restaurants/cafes/bars，则 `food_drink` share 高。如果附近有 tourist attractions/hotels/information，则 `tourism` share 高。

### 20.7 Weighted service profile

**Meaning**

不是简单平均所有站点，而是按 station return share 加权。

```text
P_weekday = sum_i weekday_weight_i * station_service_vector_i
P_weekend = sum_i weekend_weight_i * station_service_vector_i
D = P_weekend - P_weekday
```

**Why weighted**

高频站点应该比低频站点影响更大。否则一个很少被使用的站点会和 Navy Pier 这种高频站点权重一样，不合理。

### 20.8 Null model

**Meaning**

EN: A null model is a fair random comparison. It asks: if the pattern were random or caused by a simple explanation, what result would we expect?

CN: Null model 就是一个公平的随机对照。它问：如果这个 pattern 是随机的，或者只是由一个很简单的原因造成的，我们会看到什么结果？

| Validation | Simple question | Result meaning |
|---|---|---|
| Label shuffle | What if weekday/weekend labels are random? | If p is not small, do not claim overall significance. |
| Station-demand randomization | What if only station popularity and global weekday share matter? | If p is small, that simple explanation is not enough. |
| Station-service permutation | What if services are randomly assigned to stations? | If p is small, real station-service pairing matters. |
| Bootstrap | What if we resample stations many times? | If CI stays on one side of 0, the category direction is stable. |

**Chinese shortcut / 中文速记**

| Test | 一句话 |
|---|---|
| Label shuffle | 检查“整体显著吗？”答案：不能说整体显著。 |
| Station-demand randomization | 检查“是不是只是热门站 + weekday 多？”答案：不是这么简单。 |
| Station-service permutation | 检查“站点和服务环境配对是不是有结构？”答案：有结构。 |
| Bootstrap | 检查“tourism/food_drink/office 方向稳不稳？”答案：主方向比较稳。 |

### 20.9 Sensitivity test

**Meaning**

检查结果是否只依赖某个任意选择。

| Choice | Sensitivity |
|---|---|
| Top-K stations | Top20, Top50, Top100 |
| Radius | 100m, 250m, 500m |
| Service normalization | service vector normalization sensitivity |
| Category inclusion | including/excluding `other_amenity` |

**How to say it**

CN: 如果一个结果只在 Top100 + 250m 下成立，那就比较脆弱。我们的 tourism vs food_drink 方向在 Top-K sensitivity 中比较稳定，所以可以作为核心结论；但 transit 和 recreation 不够稳定，所以不能作为强结论。

## 21. Detailed Notebook Walkthrough For Presentation

这一节按 notebook 顺序讲。每个部分都包括：目的、老师为什么在乎、组员怎么讲。

### 21.1 Project Overview

**Purpose**

开场告诉听众：我们做的是 spatial mobility pipeline，不是普通 EDA。

**What to say**

EN: This project studies how weekday and weekend high-volume Divvy return destinations differ across Chicago and whether those destinations are associated with different nearby OSM service environments.

CN: 这个项目研究 Divvy 在芝加哥的高频还车目的地，比较工作日和周末是否空间分布不同，以及这些地方附近的 OSM 城市服务环境是否不同。

**Why teacher cares**

对应 Problem & Solution 20%。老师要看到 specific, solvable spatial problem。

### 21.2 Research Question And Hypothesis

**Purpose**

把 claim 限制在数据能支持的范围内。

**What to say**

CN: 我们假设 weekday 和 weekend 的高频还车目的地不同，并且这些目的地附近的服务环境也不同。因为数据没有 rider intent，所以我们只讲 association，不讲 causality。

**Likely question**

Q: Why use end station as destination?

A: Because public Divvy data does not provide final activity location. End station is the closest available spatial proxy for where a rider ended the bike-share trip.

### 21.3 Experimental Setup

**Purpose**

让别人可以复现实验。老师 rubric 里说 variables, algorithms, baseline comparisons 要 clearly defined。

**Variables**

| Type | Variable | Explanation |
|---|---|---|
| Temporal variable | `day_type` | weekday or weekend |
| Spatial unit | end station | destination proxy |
| Demand variable | return count / station share | how important a station is within a day type |
| Environmental variable | OSM service category vector | nearby service environment |
| Main comparison | `weekend_profile - weekday_profile` | positive = weekend-oriented; negative = weekday-oriented |

**Algorithms / heuristics**

| Step | Algorithmic choice |
|---|---|
| Station demand | group trips by end station and day type |
| Spatial comparison | normalize station counts into shares |
| OSM matching | haversine distance from station coordinate to POIs within radius |
| Service profile | weighted sum of station service vectors |
| Validation | shuffle, randomization, permutation, bootstrap, sensitivity |

**Baseline comparisons**

| Baseline | Why |
|---|---|
| Duration/distance | show trip-level weekday/weekend behavior differs |
| Top20 overlap | show high-volume stations are not identical |
| Raw vs normalized heatmap logic | show why normalization is needed |
| Null models | show main profile is not only a random artifact |

### 21.4 Data Sources

**Purpose**

说明每份数据在 project 里负责什么。

| Data | Role in argument | How to explain |
|---|---|---|
| Divvy trips | Main mobility data | Provides trip dates, end stations, coordinates, duration, distance |
| OSM POI cache | Environmental context | Provides nearby services around station coordinates |
| Weather data | Secondary robustness check | Checks whether rainy/cold conditions change the service profile |

**Important wording**

CN: Weather 不是 main model，也不是用来解释主结果的主要原因。它只是 secondary check。

### 21.5 Cleaning And Preprocessing

**Purpose**

满足 Data Pipeline rubric，尤其是 filtering, temporal stratification, aggregation, spatial outliers。

**Speaker script**

CN: 清洗阶段做了几类事情。第一是时间清洗，保证 trip 在 2025 范围内，并且能生成 weekday/weekend label。第二是空间清洗，要求 end station 和坐标存在，并且坐标在 Chicago 合理范围内。第三是 trip 合理性过滤，比如 duration 必须大于 0，distance 不能为负，也会检查不现实的 straight-line speed。最后把 trip 聚合到 end station，因为后面的 OSM profile 是站点级别分析。

**Why this is defensible**

我们不是为了让结果好看而过滤，而是为了让每条保留记录都能用于：

```text
weekday/weekend labeling
end-station aggregation
spatial mapping
OSM radius matching
duration/distance baseline
```

### 21.6 Baseline Distributions

**Purpose**

先证明 weekday/weekend trip behavior 本身有差异，再进入空间分析。

**Result**

| Metric | Weekday | Weekend | Meaning |
|---|---:|---:|---|
| Mean duration | 13.47 min | 17.15 min | Weekend rides last longer |
| Mean length | 2.18 km | 2.27 km | Weekend rides are slightly longer |

**How to close the graph**

CN: 这个 baseline 支持 weekday/weekend 行为不同，但它还不能回答目的地附近是什么城市功能。所以它只是动机，不是主结果。

### 21.7 Baseline End Station Patterns

**Purpose**

检查高频还车站点是否相同。

**Result**

Top20 overlap is 55%, with 11 overlapping stations out of 20.

**How to explain**

CN: 如果 weekday 和 weekend Top20 完全一样，那后面讲空间差异会比较弱。现在只有 55% overlap，说明高频目的地确实不完全相同，因此值得继续做 heatmap 和 OSM service profile。

### 21.8 Spatial Destination Heatmaps

**Purpose**

回答 where：weekday/weekend difference 在哪里。

**What to say before showing the map**

EN: This figure is designed to show whether relative station importance differs spatially between weekdays and weekends after normalizing for the larger weekday volume.

CN: 这张图的目的，是在 normalized 后看 weekday/weekend 相对重要站点在空间上是否不同，因为 weekday 总量更大，不能直接比 raw counts。

**What to say after showing the map**

CN: 结果显示，lakefront 和 tourism-oriented stations 更偏 weekend；downtown commute stations 更偏 weekday。这回答了 where 的问题。下一步 OSM profile 回答 what kind of nearby environment 的问题。

### 21.9 OSM Service Analysis

**Purpose**

把空间位置转成可解释的城市服务环境。

**What to say**

CN: 只说某些点在湖边或 downtown 还不够。为了让解释更系统，我们用 OSM POIs 给每个站点构建服务环境 profile。比如附近 restaurants/cafes 多就是 food_drink，高楼 office tag 多就是 office，旅游相关 POI 多就是 tourism。

**Why coordinate-based matching matters**

CN: 我们不是只靠 station name 匹配，因为名字可能不稳定或不完整。我们使用站点 latitude/longitude 和 haversine distance，在半径内找 OSM POIs，这更符合 spatial analysis。

### 21.10 Destination-Service Profiling Framework

**Purpose**

这是主方法。一定要讲清楚，不然老师可能觉得只是画图。

**Simple explanation**

CN: 每个站点都有一个服务向量，表示周围各种服务的比例。weekday 和 weekend 对不同站点赋予不同权重。一个站点如果 weekend returns 很高，它对 weekend profile 影响就更大。最后我们比较 weekend profile 和 weekday profile 的差。

**Formula explanation**

```text
S_i = station i service vector
w_i = station i return share within weekday or weekend
P = sum(w_i * S_i)
D = P_weekend - P_weekday
```

**How to interpret `D`**

| `D` value | Meaning |
|---|---|
| Positive | This service category is more weekend-associated |
| Negative | This service category is more weekday-associated |
| Near zero | Little difference |

### 21.11 Main OSM Results

**Purpose**

回答 project 的 main research question。

**What to say**

CN: 在 Top100 union、250m radius、排除 `other_amenity` 的主设置下，weekend profile 在 tourism 上更高，weekday profile 在 food_drink 和 office 上更高。tourism 的 weekend-minus-weekday 是 +0.0355，food_drink 是 -0.0436，office 是 -0.0135。

**Why not overclaim**

CN: 这不是说每个 weekend rider 都去旅游，也不是说 food_drink 导致 weekday rides。它只是说在高频还车站点中，周末加权的站点附近更偏 tourism，工作日加权的站点附近更偏 food_drink 和 office。

### 21.12 Validation

**Purpose**

老师要求 evaluate results。这里不要讲成复杂统计课，直接讲成 5 个问题：

```text
1. 高频站点真的不同吗？
2. 空间位置真的不同吗？
3. 主结果会不会只是随机巧合？
4. category 方向稳不稳定？
5. 结果会不会太依赖 Top-K、radius、OSM coverage？
```

**How to introduce validation / 中英对照开场**

EN: This is not a prediction model, so validation is not about accuracy. Validation checks whether the pattern is believable, stable, and not only caused by random choices.

CN: 这不是 prediction model，所以 validation 不讲 accuracy。Validation 是检查这个 pattern 靠不靠谱、稳不稳定、是不是只是随机或某个设置造成的。

**Simple validation story / 简单讲法**

| Question | EN answer | CN answer |
|---|---|---|
| Are top stations different? | Yes, Top20 overlap is 55%. | 是，Top20 overlap 只有 55%。 |
| Is the spatial pattern clear? | Yes, heatmaps show weekend lakefront/tourism and weekday downtown/commute. | 是，heatmap 显示 weekend 偏 lakefront/tourism，weekday 偏 downtown/commute。 |
| Is the overall profile statistically significant? | No, label shuffle p = 0.2657. | 不能说整体显著，因为 label shuffle p = 0.2657。 |
| Is there structured evidence? | Yes, station-demand and station-service tests both have p = 0.0010. | 有，station-demand 和 station-service tests 都是 p = 0.0010。 |
| Are category directions stable? | Partly: tourism, food_drink, office are stable; transit is not strong. | 部分稳定：tourism、food_drink、office 稳定；transit 不算强结论。 |
| What is the main limitation? | OSM coverage and radius choice affect interpretation. | 主要限制是 OSM coverage 和 radius choice。 |

**One sentence to remember / 记住这一句**

EN: Validation is mixed but transparent: no overall significance claim, but structured evidence supports the main exploratory pattern.

CN: Validation 是 mixed but transparent：不能说整体显著，但结构性证据支持主 exploratory pattern。

### 21.13 Weather Secondary Check

**Purpose**

检查 weather 是否可能是主结果解释。

**What to say**

CN: Weather 只是 secondary check。Rain-effect L1 大约 0.0089，比主 weekday/weekend service-profile difference 小很多。所以我们不把 weather 当主解释，只说它没有明显改变主线。

### 21.14 Feedback Integration

**Purpose**

老师 paper rubric 有 Feedback Integration 10%。这个 section 说明我们根据反馈改进了项目。

**What to say**

CN: 这个 notebook 不是只保留最初的简单 weekday/weekend summary。我们根据反馈增加了更明确的 pipeline、normalized heatmaps、coordinate-based OSM matching、Top100 main profile、多种 validation，以及更谨慎的 conclusion。

### 21.15 Discussion And Conclusion

**Purpose**

控制 claim，显示我们知道方法限制。

**Final wording**

EN: The results show an exploratory spatial association between day type and nearby service environments of high-volume Divvy return destinations. They do not prove rider intent or causality.

CN: 结果显示 day type 和高频还车目的地附近服务环境之间存在探索性空间关联，但不能证明 rider intent 或 causality。

## 22. Figure And Table Explanation Cards

老师要求每张图都要有“目的”和“结论”。下面这些可以直接当演讲卡片。

### 22.1 Cleaning summary table

**Before showing**

CN: 这张表展示 raw trips 如何变成可以分析的 cleaned trips，重点是时间、空间坐标、duration 和 distance 的过滤。

**Key pattern**

Coordinate filter removes 5,535 rows; duration filter removes 238 rows; final rows are 5,547,168.

**After showing**

CN: 这说明我们的 pipeline 不是直接画 raw data，而是先保证每条记录可以用于 temporal label、spatial mapping 和 station aggregation。

### 22.2 Duration/distance distributions

**Before showing**

CN: 这些图检查 weekday 和 weekend 在基础 trip behavior 上是否不同。

**Key pattern**

Weekend trips are longer in duration and slightly longer in distance.

**After showing**

CN: 这支持 weekday/weekend behavior differs，但它不是最终 spatial service conclusion。

### 22.3 Top20 overlap table/bar

**Before showing**

CN: 这个 baseline 检查 weekday 和 weekend 的高频还车站点是不是同一组。

**Key pattern**

Only 11 out of 20 overlap; overlap = 55%.

**After showing**

CN: 高频目的地不完全相同，所以继续做 spatial heatmap 和 OSM service profile 是有意义的。

### 22.4 Normalized destination heatmaps

**Before showing**

CN: 这张图检查 normalized 后，weekday 和 weekend 相对重要的目的地是否在空间上不同。

**Key pattern**

Weekend-oriented stations appear around lakefront/tourism areas; weekday-oriented stations appear around downtown commute/work areas.

**After showing**

CN: Heatmap 回答 where。它说明空间差异在哪里，但不直接说明这些地方是什么服务环境，所以后面接 OSM profile。

### 22.5 Weekend-minus-weekday destination difference map

**Before showing**

CN: 这个 map 直接看 weekend station share 减 weekday station share。

**Key pattern**

Positive values are weekend-oriented; negative values are weekday-oriented.

**After showing**

CN: 它帮助我们识别相对 weekend 或 weekday 的 destination hotspots。

### 22.6 OSM service profile comparison

**Before showing**

CN: 这张图/表是主结果，展示 Top100 station union 的加权 OSM service profile。

**Key pattern**

`tourism` is higher for weekend; `food_drink` and `office` are higher for weekday.

**After showing**

CN: 这支持我们的核心 claim：weekday/weekend high-volume return destinations are associated with different nearby service environments。

### 22.7 Weekend-minus-weekday service difference chart

**Before showing**

CN: 这个 chart 把差异方向直接画出来，正数偏 weekend，负数偏 weekday。

**Key pattern**

Positive: tourism. Negative: food_drink and office.

**After showing**

CN: 这张图最适合讲 final result，但要马上补一句：这是 association，不是 causality。

### 22.8 Label shuffle histogram

**Purpose / 目的**

EN: Test whether the overall weekday/weekend profile difference is unusually strong if day labels are randomized.

CN: 检查如果随机打乱 weekday/weekend 标签，我们真实的整体差异是不是还算特别强。

**Result / 结果**

p = 0.2657.

**How to say it / 怎么讲**

EN: This is the caution result. p = 0.2657 is not significant, so we should not say the whole profile difference is statistically significant.

CN: 这是谨慎点。p = 0.2657 不显著，所以不能说整个 profile difference 统计显著。

### 22.9 Station-demand randomization plot

**Purpose / 目的**

EN: Test whether the result is only caused by station popularity and the fact that weekdays have more trips overall.

CN: 检查结果是不是只因为某些站本来就热门，以及 weekday 总 trip 更多。

**Result / 结果**

p = 0.0010.

**How to say it / 怎么讲**

EN: This is strong evidence. Station popularity plus the global weekday share cannot explain the observed profile difference.

CN: 这是强证据。只靠“站点热门程度 + weekday 总量更大”解释不了我们的 observed profile difference。

**Boundary / 边界**

EN: It still does not prove OSM causes rider behavior.

CN: 但它仍然不证明 OSM 导致 rider behavior。

### 22.10 Station-service permutation plot

**Purpose / 目的**

EN: Test whether the real matching between stations and nearby service environments matters.

CN: 检查真实站点和附近服务环境的配对是否重要。

**Result / 结果**

p = 0.0010.

**How to say it / 怎么讲**

EN: This is strong evidence. Random station-service matching does not reproduce the real result, so the real pairing is structured.

CN: 这是强证据。随机配对不能复制真实结果，所以真实 station-service pairing 有结构。

### 22.11 Bootstrap service category CI

**Purpose / 目的**

EN: Test whether each service-category direction stays stable when stations are resampled.

CN: 检查反复抽样站点时，每个 service category 的方向是否稳定。

**Result / 结果**

Stable weekend: `tourism`. Stable weekday: `food_drink`, `office`, `health`. `transit` crosses zero.

**How to say it / 怎么讲**

EN: Tourism, food_drink, and office are safe main claims. Transit is only descriptive because its interval crosses zero.

CN: Tourism、food_drink、office 可以作为主结论。Transit 因为区间跨 0，只能描述性提，不能当强结论。

### 22.12 Top-K radius sensitivity heatmap

**Purpose / 目的**

EN: Test whether the result depends too much on choosing Top100 or 250m.

CN: 检查结果是不是太依赖 Top100 或 250m 这个选择。

**Result / 结果**

Core tourism vs food_drink direction is fairly stable, but effect size and some categories change with radius.

**How to say it / 怎么讲**

EN: The main direction is not just one-setting luck, but scale matters, so radius must be listed as a limitation.

CN: 主方向不是只靠一个设置碰巧出现，但 scale matters，所以 radius 必须写成 limitation。

### 22.13 OSM coverage table/map

**Before showing**

CN: 这个部分检查 missing OSM coverage 是否可能影响结果。

**Key pattern**

Top100 union has 129 stations; 75 have OSM profile; covered return share is 63.63%.

**After showing**

CN: 这是一个 measured limitation。我们没有隐藏 coverage 问题，而是把它量化并放进 discussion。

### 22.14 Weather effect chart

**Before showing**

CN: 这个 chart 检查 rainy/dry weather 是否明显改变 service profile。

**Key pattern**

Rain-effect L1 is about 0.0089.

**After showing**

CN: Weather effect small, so weather remains secondary, not the main explanation.

## 23. Exact Speaking Script

下面是一版可以直接练的中文演讲稿。正式讲的时候不要逐字背，但逻辑可以照这个走。

### Opening

大家好，我们的 final project 研究 Chicago Divvy 的 weekday 和 weekend end-station patterns。我们的重点不是简单比较 weekday 和 weekend 谁的 trip count 更多，而是做一个 spatial mobility pipeline：先看高频还车目的地在空间上是否不同，再看这些目的地附近的 OSM 城市服务环境是否不同。

这个问题符合老师要求的 specific spatial problem，因为它有明确的 spatial unit，也就是 end station；有明确的 temporal stratification，也就是 weekday 和 weekend；还有明确的 environmental context，也就是站点附近的 OSM service categories。

### Problem and solution

我们的 research question 是：How do weekday and weekend Divvy end-station patterns differ in Chicago, and what nearby urban service environments are associated with high-volume weekday and weekend destinations?

这里要强调一个 claim boundary。Divvy public data 不知道 rider 还车之后真正去了哪里，所以 end station 只是 destination proxy。OSM services 也只是描述站点周边环境，不证明 rider intent。所以我们的 solution 是 destination-service profiling，而不是 causality model 或 prediction model。

### Data pipeline

Pipeline 从 Divvy trip data 开始。我们先做 cleaning，包括 timestamp、2025 date range、end station、coordinates、duration、distance、unrealistic speed 和 Chicago coordinate bounds。这个步骤很重要，因为如果坐标不可信，后面 heatmap 和 OSM matching 都会错。

清洗之后，我们给每条 trip 标记 weekday 或 weekend，然后把 trip-level data 聚合到 end station level。聚合之后，我们可以计算每个站点在 weekday 和 weekend 的 return count，以及 normalized station share。

我们还使用 OSM POI cache。对每个 Top-K union station，我们用 latitude/longitude 和 haversine distance 找半径内的 POIs，然后把 POIs 归类成 food_drink、office、tourism、transit、retail 等服务类别。

### Experimental setup

实验的主要 comparison 不是 raw weekday count vs raw weekend count，因为 weekday 总量本来就更大。我们使用 normalized station share：

```text
station share = station return count / total returns within that day type
```

这样比较的是一个站在 weekday 内部和 weekend 内部的相对重要性。

主 OSM profile 使用 Top100 weekday/weekend union、250m radius、排除 `other_amenity`，并且只使用有 OSM profile coverage 的站点。Top20 容易解释，但样本小；Top100 更稳定，但 coverage 下降，所以我们把 coverage 当作 limitation。

### Baseline results

Baseline 先看 trip behavior。Weekend trips 平均 duration 是 17.15 minutes，weekday 是 13.47 minutes；weekend trip length 也略长。这说明 weekday/weekend behavior 有差异，但还不能解释目的地环境。

然后看 Top20 end-station overlap。Weekday Top20 和 weekend Top20 只有 11 个站重合，overlap 是 55%。这说明高频还车目的地不是完全一样的，所以继续做 spatial 和 OSM service analysis 是合理的。

### Spatial heatmap result

Normalized heatmaps 显示，lakefront 和 tourism-related stations 更偏 weekend，比如 Navy Pier 和 lakefront stations；downtown commute/work stations 更偏 weekday，比如 Clinton、Canal、Franklin 一带。

这张图回答 where：差异在哪里。它还没有回答 what：这些地方附近是什么服务环境。所以我们接下来做 OSM service profile。

### OSM service profile result

每个站点都有一个 normalized OSM service vector。然后我们用 weekday 或 weekend station share 作为权重，计算 weekday profile 和 weekend profile。最后看：

```text
weekend profile - weekday profile
```

主结果是，`tourism` 在 weekend profile 更高，weekend-minus-weekday 是 +0.0355。`food_drink` 在 weekday profile 更高，差值是 -0.0436。`office` 也偏 weekday，差值是 -0.0135。

所以我们的核心解释是：weekend-weighted destinations are more tourism-associated, while weekday-weighted destinations are more food_drink and office-associated。

### Validation

Validation 这里要讲得简单。因为这不是 prediction model，所以我们不报告 accuracy。我们只回答一个问题：这个结果靠不靠谱？

第一，label shuffle test 是谨慎点。它问的是：如果随机打乱 weekday/weekend 标签，我们真实的整体差异是不是特别强？结果 p-value 是 0.2657，不显著。所以我们不能说 overall statistically significant。

第二，station-demand randomization 是强支持。它问的是：结果会不会只是因为某些站本来就热门，而且 weekday 总量更大？结果 p-value 是 0.0010，说明只靠 station popularity 和 weekday 总量解释不了我们的 profile difference。

第三，station-service permutation 也是强支持。它问的是：如果把站点和附近 service profile 随机配对，还能不能得到这么强的结果？p-value 也是 0.0010，说明真实 station-service pairing 是有结构的。

第四，bootstrap 检查 category 方向稳不稳定。结果显示 `tourism` 稳定偏 weekend，`food_drink` 和 `office` 稳定偏 weekday。`transit` 的 CI 跨 0，所以 transit 只能描述性提，不能作为强结论。

第五，Top-K 和 radius sensitivity 检查结果是不是只靠某一个设置。核心 tourism vs food_drink 方向比较稳定，但 radius 会影响部分类别，所以 radius 是 limitation。

所以最安全的总结是：validation 是 mixed but transparent。我们不 claim overall significance，但可以说结果有结构，并且主要 category direction 部分稳定。

### Limitations

我们的 limitation 有几个。第一，end station 只是 destination proxy，不是 rider 的最终活动地点。第二，OSM services 描述附近环境，不证明这些 services caused behavior。第三，Top100 OSM coverage 是 63.63%，不是 full coverage。第四，250m radius 是 modeling choice，sensitivity 显示 scale matters。第五，weather 只是 daily-level secondary check，不是 trip-time weather。

### Final conclusion

最后结论要谨慎说：weekday and weekend high-volume Divvy return destinations differ spatially, and they are associated with different nearby OSM service environments. Weekend-weighted destinations are more tourism-associated; weekday-weighted destinations are more food_drink and office-associated. The result is exploratory and associative, not causal.

## 24. Team Division Recommendation

如果组员分工演讲，可以这样分。

| Speaker | Sections | Responsibility | Must know |
|---|---|---|---|
| Speaker 1 | Opening, problem, solution | Explain research question and claim boundary | destination proxy, exploratory association |
| Speaker 2 | Data pipeline | Explain cleaning, filtering, temporal stratification, aggregation | spatial outliers, station aggregation, OSM matching |
| Speaker 3 | Experimental setup and main method | Explain variables, normalized share, service vector, weighted profile | formulas and why raw counts are unfair |
| Speaker 4 | Results | Explain baseline, heatmaps, OSM result | Top20 overlap, tourism, food_drink, office |
| Speaker 5 | Validation and conclusion | Explain tests, limitations, Q&A | p-values, bootstrap, coverage, safe wording |

**If only 3 people present**

| Speaker | Sections |
|---|---|
| Speaker 1 | Problem, data, cleaning |
| Speaker 2 | Experimental setup, baseline, heatmaps, OSM result |
| Speaker 3 | Validation, limitations, conclusion, Q&A |

**Everyone must be able to answer these 5 questions**

1. Why is this spatial?
2. Why normalize station shares?
3. Why use OSM?
4. What is the strongest result?
5. What are the biggest limitations?

## 25. Advanced Q&A

这些问题比前面的 Q&A 更细，适合老师追问时用。

**Q: Why not use start stations instead of end stations?**
EN: The research question focuses on destination environments, so end stations are the better proxy. Start stations would answer a different question about origins.
CN: 我们研究的是 destination environment，所以 end station 更合适。Start station 会变成 origin analysis，是另一个问题。

**Q: Why Top100 instead of all stations?**
EN: The project focuses on high-volume destinations where patterns are meaningful and less noisy. Top100 is broader than Top20 and less fragile, while still interpretable. Full-station coverage would be good future work.
CN: 我们关注 high-volume destinations，因为低频站点噪声更大。Top100 比 Top20 稳定，又仍然可以解释。所有站点分析可以作为 future work。

**Q: Why 250m radius?**
EN: It is a local walking-scale neighborhood around a station. The notebook also tests 100m and 500m to show that radius choice matters.
CN: 250m 是一个站点附近步行尺度的 local environment。Notebook 也测试 100m 和 500m，所以我们没有假装 250m 是唯一真理。

**Q: Why exclude `other_amenity` from the main interpreted profile?**
EN: It mixes unrelated amenities, so it weakens interpretability. Keeping it in raw outputs preserves transparency, but excluding it from main claims makes the categories more meaningful.
CN: `other_amenity` 太杂，会降低解释性。我们保留 raw output，但主结论不解释它。

**Q: Why is label shuffle not significant but other tests are significant?**
EN: They test different null hypotheses. Label shuffle is a broad overall test and does not support overall significance. Station-demand randomization and station-service permutation test more specific structural explanations, and those are significant.
CN: 因为它们检验的 null 不一样。Label shuffle 是比较宽的整体检验，不支持 overall significance；station-demand 和 station-service tests 检验更具体的结构性解释，结果显著。

**Q: Does p = 0.0010 mean the result is causal?**
EN: No. It means the observed statistic is unlikely under that particular randomization null. Causality would require a different design.
CN: 不。p = 0.0010 只说明在那个 randomization null 下结果不太可能，不等于因果。

**Q: Why not use machine learning?**
EN: The goal is not prediction. The goal is interpretable spatial mobility analysis. A transparent weighted service-profile method is more appropriate for this research question.
CN: 这个项目目标不是预测，而是解释 spatial association。透明的 weighted service-profile method 比黑箱 ML 更适合。

**Q: What would improve the project if we had more time?**
EN: Expand OSM coverage to all stations, use network walking distance instead of radius distance, test finer service categories, use trip-time weather, and compare multiple months or years.
CN: 可以扩展到所有站点、用 network walking distance 替代圆形半径、细分服务类别、使用 trip-time weather、比较多个月或多年。

**Q: Is OSM complete and reliable?**
EN: OSM is useful but incomplete and unevenly mapped. That is why coverage diagnostics are included and why missing OSM coverage is treated as a limitation.
CN: OSM 有用但不完美，覆盖可能不均匀。所以我们做 coverage diagnostics，并把 missing coverage 写成 limitation。

**Q: What is the single most important defense sentence?**
EN: Our validation is mixed but transparent: we do not claim overall significance, but we do show structured station-service association and stable category directions for the main claims.
CN: 最重要的一句话是：我们的 validation 不是完美，但透明；我们不 claim overall significance，但能显示 station-service association 有结构，而且核心 category direction 稳定。

## 26. Last-Minute Checklist Before Presenting

**Content checklist**

- Research question is stated in the first minute.
- End station is described as a destination proxy.
- Data pipeline mentions cleaning, filtering, temporal stratification, aggregation, and spatial outliers.
- Experimental setup defines variables and baseline comparisons.
- Every graph is introduced with what it is supposed to show.
- Every graph is closed with what it supports and what it does not prove.
- Main result is tourism weekend, food_drink/office weekday.
- Label shuffle p = 0.2657 is mentioned as a caution.
- Station-demand and station-service p = 0.0010 are explained as structured evidence.
- OSM coverage 63.63% is acknowledged as a limitation.
- Final claim uses exploratory association wording.

**Delivery checklist**

- Do not read every table cell.
- Do not spend too long on raw data counts.
- Spend the most time on method, main result, and validation.
- Use “proxy”, “association”, “not causal” consistently.
- If asked a hard question, answer the exact question first, then add limitation.

**Dangerous sentences to avoid**

| Avoid | Better |
|---|---|
| We proved weekend riders go to tourist attractions. | Weekend-weighted return stations are more associated with nearby tourism services. |
| Our model is accurate. | This is not a prediction model; validation checks robustness and structure. |
| The result is statistically significant overall. | The label shuffle test does not support overall significance under that null. |
| OSM explains rider behavior. | OSM describes nearby service environments. |
| Weather has no effect. | Weather effect is small in our secondary check. |

## 27. Final 30-Second Version

如果最后只剩 30 秒，就这样收尾：

EN: In summary, we built a spatial mobility pipeline for Divvy end-station behavior. After cleaning and weekday/weekend stratification, we found that high-volume return destinations differ spatially, with only 55% Top20 overlap. Normalized heatmaps show weekend-oriented lakefront/tourism destinations and weekday-oriented downtown commute destinations. The Top100 OSM service profile suggests weekend destinations are more tourism-associated, while weekday destinations are more food_drink and office-associated. Validation is mixed but transparent: label shuffle is not significant, but station-demand randomization, station-service permutation, bootstrap, and sensitivity checks support a structured exploratory association. We do not claim causality.

CN: 总结来说，我们做了一个 Divvy end-station spatial mobility pipeline。清洗并按 weekday/weekend 分层后，我们发现高频还车目的地在空间上不同，Top20 overlap 只有 55%。Normalized heatmaps 显示 weekend 更偏 lakefront/tourism，weekday 更偏 downtown commute。Top100 OSM service profile 显示 weekend destinations 更偏 tourism，weekday destinations 更偏 food_drink 和 office。Validation 是 mixed but transparent：label shuffle 不显著，但 station-demand randomization、station-service permutation、bootstrap 和 sensitivity checks 支持一个 structured exploratory association。我们不 claim causality。
