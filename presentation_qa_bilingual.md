# CSC588B Divvy Final Project Bilingual Q&A

## Q1. Why is weekday versus weekend not too simple?

**EN:** It would be too simple if we only compared trip counts. Our project uses weekday versus weekend as the temporal split, but the real question is spatial: where bikes are returned and what services are near those return stations.

**CN:** 如果只是比较 trip count，那确实太简单。我们的项目把 weekday/weekend 当作时间分层，真正问题是空间问题：车还到哪里？这些还车站点附近有什么服务？

## Q2. Why use end stations?

**EN:** The research question is about destination patterns. Public Divvy data does not show the rider's final activity, so the end station is the best available destination proxy.

**CN:** 因为研究问题是 destination patterns。公开 Divvy 数据没有 rider 的最终活动地点，所以 end station 是最合适的 destination proxy。

## Q3. Does the end station prove where the rider went?

**EN:** No. End station is only a destination proxy. A rider may walk somewhere else after returning the bike.

**CN:** 不证明。End station 只是 destination proxy。Rider 还车后可能走去其他地方。

## Q4. Why add OSM services?

**EN:** Trip duration and distance show movement behavior, but they do not describe the urban environment near the return station. OSM services add that nearby service context.

**CN:** Trip duration 和 distance 只能说明移动行为，不能说明还车站附近的城市环境。OSM services 增加了附近服务环境的信息。

## Q5. Why use 250 meters?

**EN:** 250m is a local walking-scale radius around a station. It is a modeling choice, not a universal truth. Sensitivity checks with other radii show scale matters.

**CN:** 250m 是站点附近的 local walking-scale radius。它是 modeling choice，不是唯一真理。其他半径的 sensitivity checks 显示 scale matters。

## Q6. How were outliers handled?

**EN:** The cleaning pipeline filters timestamps, 2025 date range, coordinates, duration, and distance. Spatial filtering includes coordinate filtering; the coordinate filter removed 5,535 rows.

**CN:** Cleaning pipeline 过滤 timestamp、2025 date range、coordinates、duration 和 distance。空间过滤包括 coordinate filtering；coordinate filter 移除了 5,535 行。

## Q7. What are the main cleaning numbers?

**EN:** Original rows were 5,552,994. Final rows were 5,547,168. The coordinate filter removed 5,535 rows, and the duration filter removed 238 rows.

**CN:** 原始行数是 5,552,994。最终行数是 5,547,168。Coordinate filter 移除了 5,535 行，duration filter 移除了 238 行。

## Q8. What is the baseline comparison?

**EN:** The baseline is trip-only weekday/weekend analysis. Weekend mean duration is 17.15 minutes versus 13.47 minutes for weekdays. Weekend mean distance is 2.27 km versus 2.18 km for weekdays. Top20 overlap is 11 stations, or 55%.

**CN:** Baseline 是 trip-only weekday/weekend analysis。Weekend mean duration 是 17.15 minutes，weekday 是 13.47 minutes。Weekend mean distance 是 2.27 km，weekday 是 2.18 km。Top20 overlap 是 11 个站，也就是 55%。

## Q9. Why normalize station shares?

**EN:** Weekday trips are much more common: 3,970,986 trips, or 71.59%. Weekend trips are 1,576,182, or 28.41%. Normalization lets us compare station importance within each day type.

**CN:** Weekday trips 明显更多：3,970,986 trips，占 71.59%。Weekend trips 是 1,576,182，占 28.41%。Normalization 让我们比较每个站在各自 day type 内部的重要性。

## Q10. What is the main OSM setting?

**EN:** The main OSM setting is Top100 union, 250m radius, excluding `other_amenity`, and covered stations only.

**CN:** 主 OSM 设置是 Top100 union、250m radius、排除 `other_amenity`、只使用 covered stations。

## Q11. What is the main OSM result?

**EN:** Tourism is weekend-oriented with difference +0.0355. Food_drink is weekday-oriented with difference -0.0436. Office is weekday-oriented with difference -0.0135.

**CN:** Tourism 偏 weekend，difference 是 +0.0355。Food_drink 偏 weekday，difference 是 -0.0436。Office 偏 weekday，difference 是 -0.0135。

## Q12. What about transit?

**EN:** Transit has difference +0.0248, but it is descriptive only because the bootstrap confidence interval crosses zero. I would not present it as a strong result.

**CN:** Transit 的 difference 是 +0.0248，但因为 bootstrap confidence interval 跨 0，所以只能描述性提，不能作为强结论。

## Q13. Why not make recreation the main weekend result?

**EN:** In the main Top100 service profile, recreation is not the main weekend-oriented result. The safer main weekend result is tourism.

**CN:** 在主 Top100 service profile 里，recreation 不是主要 weekend 结果。更安全的 weekend 主结果是 tourism。

## Q14. What does validation show?

**EN:** Validation is mixed but useful. Label shuffle p = 0.2657, so we cannot claim overall statistical significance. Station-demand randomization p = 0.0010 and station-service permutation p = 0.0010 show structured evidence under those tests.

**CN:** Validation 不是完美，但有用。Label shuffle p = 0.2657，所以不能 claim overall statistical significance。Station-demand randomization p = 0.0010，station-service permutation p = 0.0010，说明在这些 test 下有结构性证据。

## Q15. Does p = 0.0010 prove causality?

**EN:** No. It only means the observed result is unlikely under that specific randomization or permutation test. It does not prove OSM services caused rider behavior.

**CN:** 不证明。它只说明在那个 randomization 或 permutation test 下，观察到的结果不太像随机产生。它不证明 OSM services 导致 rider behavior。

## Q16. What is the main limitation?

**EN:** The main limitation is that end stations are only destination proxies. OSM coverage is also incomplete; the Top100 covered return share is 63.63%.

**CN:** 主要 limitation 是 end station 只是 destination proxy。OSM coverage 也不完整；Top100 covered return share 是 63.63%。

## Q17. What role does weather play?

**EN:** Weather is only a secondary check. The rain-effect L1 is about 0.0089, so weather is not the main result.

**CN:** Weather 只是 secondary check。Rain-effect L1 大约是 0.0089，所以 weather 不是主结果。

## Q18. What should be improved in the final paper?

**EN:** The final paper should explain limitations more deeply, especially end-station proxy, incomplete OSM coverage, and radius choice. It can also discuss future work like wider OSM coverage, network distance, and finer service categories.

**CN:** Final paper 应该更深入解释 limitations，特别是 end-station proxy、OSM coverage 不完整、radius choice。Future work 可以包括更完整的 OSM coverage、network distance、更细的 service categories。

## Q19. What is the safest final conclusion?

**EN:** Weekday and weekend high-volume Divvy return destinations differ spatially and are associated with different nearby OSM service environments. This is an exploratory spatial association, not causal proof.

**CN:** Divvy 工作日和周末高频还车目的地在空间上不同，并且和不同附近 OSM service environments 有关联。这是 exploratory spatial association，不是 causal proof。
