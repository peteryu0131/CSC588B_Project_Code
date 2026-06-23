# CSC588B Divvy Final Project Bilingual Presentation Script

## Slide 1: Title and Research Question

**EN speaker notes**

Hello everyone. Our project studies weekday and weekend Divvy end-station patterns in Chicago. The main question is: how do weekday and weekend high-volume return destinations differ, and what nearby urban service environments are associated with those destinations?

This is not only a trip-count comparison. We are using weekday and weekend as a time split, but the real focus is spatial. We want to understand where bikes are returned, and what kinds of services are near those return stations.

One important boundary is that we use end station as destination proxy. The data does not tell us the rider's exact final activity.

**中文讲稿**

大家好。我们的项目研究 Chicago Divvy 在工作日和周末的还车站点模式。核心问题是：weekday 和 weekend 的高频还车目的地有什么空间差异？这些目的地附近对应什么样的城市服务环境？

这不是简单比较 trip count。我们用 weekday 和 weekend 做时间分层，但真正重点是空间：车还到哪里？这些还车站点附近有什么服务？

这里有一个重要边界：我们把 end station 当作 destination proxy。数据不能告诉我们 rider 下车后的真实最终活动。

## Slide 2: Why This Is a Spatial Mobility Problem

**EN speaker notes**

This is a spatial mobility problem because we are not only looking at trips as rows in a table. We connect each trip to a return station, and each return station has a location in Chicago.

The raw Divvy records give us trip time, station fields, and station coordinates. After cleaning and processing, we use duration and distance for baseline analysis. But the trip records alone do not explain service access, so we add OSM services near return stations.

So the project has three layers: movement data, station locations, and nearby service environments.

**中文讲稿**

这是一个 spatial mobility problem，因为我们不是只把每条 trip 当作表格里的一行。我们把每条 trip 连接到一个还车站点，而每个还车站点在 Chicago 有具体位置。

原始 Divvy records 提供 trip time、station fields 和 station coordinates。经过清洗处理后，我们用 duration 和 distance 做 baseline analysis。但 trip records 本身不能解释 service access，所以我们加入还车站点附近的 OSM services。

因此项目有三层：movement data、station locations、nearby service environments。

## Slide 3: Data Sources

**EN speaker notes**

The main data source is Divvy trip data. The raw records give trip dates, station names, and coordinates. The cleaned analysis table includes trip duration and trip distance. These fields let us build weekday and weekend station-level patterns.

The second source is OSM POI data. OSM lets us describe nearby services around return stations, such as food_drink, office, tourism, transit, retail, health, education, and recreation.

Weather is included only as a secondary check. It is not the main research question, and I will not use it as the main explanation.

**中文讲稿**

主要数据来源是 Divvy trip data。原始记录提供 trip date、station names 和 coordinates。清洗后的分析表包含 trip duration 和 trip distance。这些字段让我们能建立 weekday 和 weekend 的站点级模式。

第二个数据来源是 OSM POI data。OSM 可以描述还车站点附近的服务，比如 food_drink、office、tourism、transit、retail、health、education、recreation。

Weather 只作为 secondary check。它不是主研究问题，我也不会把它当作主解释。

## Slide 4: Cleaning and Spatial Filtering

**EN speaker notes**

Before analysis, we clean the trip data. The original data has 5,552,994 rows. After cleaning, the final dataset has 5,547,168 rows.

The cleaning checks timestamps, the 2025 date range, coordinates, duration, and distance. Spatial filtering is especially important because wrong coordinates would affect both maps and OSM matching.

The coordinate filter removed 5,535 rows. The duration filter removed 238 rows. After this, the data is usable for weekday/weekend labels, station aggregation, and spatial matching.

**中文讲稿**

分析之前，我们先清洗 trip data。原始数据有 5,552,994 行。清洗后最终数据有 5,547,168 行。

清洗包括 timestamp、2025 date range、coordinates、duration 和 distance。空间过滤特别重要，因为错误坐标会影响 maps 和 OSM matching。

Coordinate filter 移除了 5,535 行。Duration filter 移除了 238 行。清洗后，数据才可以用于 weekday/weekend 标记、station aggregation 和 spatial matching。

## Slide 5: Full Data Pipeline

**EN speaker notes**

The full pipeline starts with cleaned Divvy trips. First, trips are labeled as weekday or weekend. Then trips are aggregated by return station.

Because weekday trips are much more common, we do not compare raw station counts directly. Instead, we calculate normalized station shares within weekday and within weekend.

After that, we match return stations to nearby OSM service categories. Finally, we compare the weekday and weekend service profiles and validate the result.

**中文讲稿**

完整 pipeline 从 cleaned Divvy trips 开始。第一步，把 trips 标记成 weekday 或 weekend。第二步，按还车站点进行聚合。

因为 weekday trips 总量明显更多，我们不能直接比较 raw station counts。我们要计算 normalized station share，也就是每个站在 weekday 或 weekend 内部的重要性。

之后，我们把还车站点匹配到附近 OSM service categories。最后比较 weekday 和 weekend service profiles，并做 validation。

## Slide 6: Experimental Setup and Destination-Service Profiling Formula

**EN speaker notes**

The main experiment compares weighted service profiles. The variables are day type, end station, return count, station share, and OSM service vector.

For each station, we build a service vector based on nearby OSM POIs. Then we weight that vector by how important the station is within weekday or weekend returns.

The main setting is Top100 union, 250 meter radius, excluding `other_amenity`, and covered stations only. The 250 meter radius is a modeling choice. Sensitivity checks show that scale matters, so we should not present 250 meters as the only correct radius.

**中文讲稿**

主实验比较的是 weighted service profiles。变量包括 day type、end station、return count、station share 和 OSM service vector。

对每个站点，我们根据附近 OSM POIs 建立一个 service vector。然后根据这个站点在 weekday 或 weekend returns 里的重要性进行加权。

主设置是 Top100 union、250m radius、排除 `other_amenity`、只使用 covered stations。250m 是 modeling choice。Sensitivity checks 显示 scale matters，所以不能说 250m 是唯一正确半径。

## Slide 7: Baseline Results

**EN speaker notes**

This slide is designed to show whether weekday and weekend trips already differ before we add OSM services.

The key pattern is that weekend trips are longer. Weekday mean duration is 13.47 minutes, while weekend mean duration is 17.15 minutes. Weekday mean distance is 2.18 km, while weekend mean distance is 2.27 km.

The Top20 station overlap is 11 stations, or 55%. This supports the research question because weekday and weekend patterns are not identical. But this baseline does not explain nearby service access, so we need the OSM analysis.

**中文讲稿**

这一页是为了说明，在加入 OSM services 之前，weekday 和 weekend trips 本身是否已经不同。

关键 pattern 是 weekend trips 更长。Weekday mean duration 是 13.47 minutes，weekend mean duration 是 17.15 minutes。Weekday mean distance 是 2.18 km，weekend mean distance 是 2.27 km。

Top20 station overlap 是 11 个站，也就是 55%。这支持我们的研究问题，因为 weekday 和 weekend patterns 不完全一样。但 baseline 不能解释附近 service access，所以需要 OSM analysis。

## Slide 8: Normalized Spatial Heatmaps

**EN speaker notes**

This figure is designed to show where weekday and weekend destination patterns differ after normalization.

Normalization matters because weekday trips are 3,970,986 trips, or 71.59%, while weekend trips are 1,576,182 trips, or 28.41%. If we used raw counts, weekday volume would dominate.

The key pattern is that weekend-oriented stations appear more around lakefront and tourism areas, while weekday-oriented stations appear more around downtown commute areas. This supports the research question by showing spatial difference. It does not prove rider intent.

**中文讲稿**

这张图是为了展示 normalization 之后，weekday 和 weekend destination patterns 在哪里不同。

Normalization 很重要，因为 weekday 有 3,970,986 trips，占 71.59%；weekend 有 1,576,182 trips，占 28.41%。如果直接用 raw counts，weekday 总量会主导结果。

关键 pattern 是 weekend-oriented stations 更多出现在 lakefront 和 tourism areas，weekday-oriented stations 更多出现在 downtown commute areas。这支持研究问题中的空间差异，但不能证明 rider intent。

## Slide 9: Main OSM Service Profile Result

**EN speaker notes**

This figure is designed to show whether weekday and weekend return stations are associated with different nearby OSM service environments.

The key result is that tourism is weekend-oriented, with a difference of +0.0355. Food_drink is weekday-oriented, with a difference of -0.0436. Office is also weekday-oriented, with a difference of -0.0135.

Transit has a positive difference of +0.0248, but it is descriptive only because the bootstrap confidence interval crosses zero. This result supports the research question by linking end-location patterns to nearby service environments. It does not prove riders definitely went to tourist places.

**中文讲稿**

这张图是为了展示 weekday 和 weekend return stations 附近的 OSM service environments 是否不同。

关键结果是 tourism 偏 weekend，difference 是 +0.0355。Food_drink 偏 weekday，difference 是 -0.0436。Office 也偏 weekday，difference 是 -0.0135。

Transit 的 difference 是 +0.0248，但是因为 bootstrap confidence interval 跨 0，所以只能描述性提。这个结果支持研究问题，因为它把 end-location patterns 和附近 service environments 联系起来。但它不能证明 riders 一定去了旅游地点。

## Slide 10: Validation

**EN speaker notes**

This slide is designed to show whether the result is believable and stable.

The first important point is caution. Label shuffle has p = 0.2657, so we should not claim overall statistical significance.

But two checks give stronger support. Station-demand randomization has p = 0.0010, meaning station popularity plus global weekday share do not fully explain the result under that null model. Station-service permutation also has p = 0.0010, meaning the real station-service pairing has structure.

Sensitivity checks also show scale matters, so 250 meters remains a modeling choice.

**中文讲稿**

这一页是为了说明结果是否可信、是否稳定。

第一点是谨慎。Label shuffle 的 p = 0.2657，所以不能 claim overall statistical significance。

但有两个检查提供更强支持。Station-demand randomization 的 p = 0.0010，说明在这个 null model 下，只靠站点热门程度和整体 weekday share 不能充分解释结果。Station-service permutation 也是 p = 0.0010，说明真实 station-service pairing 有结构。

Sensitivity checks 也显示 scale matters，所以 250m 仍然是 modeling choice。

## Slide 11: Limitations

**EN speaker notes**

This slide is designed to show what the project cannot prove.

The biggest limitation is that the end station is only a destination proxy. Riders may return a bike and then walk somewhere else. OSM services describe the nearby environment, but they do not prove rider intent.

OSM coverage is incomplete. For the Top100 union, the covered return share is 63.63%. Also, the 250 meter radius is a modeling choice. Weather is not the main result; the rain-effect L1 is about 0.0089, so it stays secondary.

**中文讲稿**

这一页是为了说明项目不能证明什么。

最大 limitation 是 end station 只是 destination proxy。Rider 还车后可能走去别的地方。OSM services 描述的是附近环境，但不能证明 rider intent。

OSM coverage 不完整。Top100 union 的 covered return share 是 63.63%。另外，250m radius 是 modeling choice。Weather 不是主结果；rain-effect L1 大约是 0.0089，所以只能作为 secondary。

## Slide 12: Final Claim and Q&A

**EN speaker notes**

The final claim is careful. Weekday and weekend high-volume Divvy return destinations differ spatially. Weekend-weighted destinations are more associated with tourism services. Weekday-weighted destinations are more associated with food_drink and office services.

But the result is an exploratory spatial association, not causal proof. We do not claim that OSM services caused rider behavior. We also do not claim that riders definitely went to tourist places.

So the contribution is a defendable spatial mobility pipeline: from raw Divvy trips, to cleaned station-level patterns, to OSM service profiles, with validation and clear limitations.

**中文讲稿**

最终结论要谨慎。Divvy 工作日和周末高频还车目的地在空间上不同。Weekend 加权目的地更偏 tourism services。Weekday 加权目的地更偏 food_drink 和 office services。

但是这个结果是 exploratory spatial association，不是 causal proof。我们不 claim OSM services 导致 rider behavior。我们也不 claim riders 一定去了旅游地点。

所以这个项目的贡献是一个可以 defend 的 spatial mobility pipeline：从 raw Divvy trips，到清洗后的 station-level patterns，再到 OSM service profiles，并且有 validation 和清楚的 limitations。
