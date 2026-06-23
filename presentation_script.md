# CSC588B Final Project Presentation Script

## Slide 1: Research Question And Motivation

Today I am presenting our Divvy bike-share project for Chicago. The main question is: how do weekday and weekend Divvy trips differ in end-location patterns and nearby service access?

This is not just asking whether there are more trips on weekdays or weekends. We are asking a spatial question. Where do riders return bikes on weekdays, where do they return them on weekends, and what kinds of services are near those return stations?

One important boundary is that the Divvy data does not tell us the rider's final activity. So we treat the end station as a destination proxy. That means we can talk about nearby station environments, but we cannot say we proved exactly where riders went after returning the bike.

## Slide 2: Why The Problem Needs A Spatial Pipeline

The reason this project needs a pipeline is that the raw data does not directly answer the research question. The raw Divvy records give us trip times, station fields, and station coordinates. After cleaning and processing, we use duration and distance for baseline analysis. Those fields are useful, but they still need to be cleaned, grouped, and connected to spatial context.

Our pipeline starts with raw Divvy trip data. Then we clean the trips, split them into weekday and weekend, aggregate them by return station, map normalized spatial differences, and match stations to nearby OSM services.

This is why the project is more than a list of plots. Each step turns the raw records into a clearer spatial mobility question.

## Slide 3: Data Pipeline And Cleaning

For the data pipeline, we start with 5,552,994 raw rows. After cleaning, the final dataset has 5,547,168 rows.

The cleaning step handles timestamps, trips outside the 2025 date range, missing or invalid coordinates, invalid durations, and invalid distances. This matters because the project is spatial. If the coordinates are wrong, then the maps and OSM matching are also wrong.

The biggest cleaning step is the coordinate filter, which removes 5,535 rows. The duration filter removes 238 rows. After that, the cleaned data can support three things: weekday versus weekend labeling, station aggregation, and spatial matching around return stations.

## Slide 4: Experimental Setup

The experiment has a few main variables. The temporal variable is day type, which is weekday or weekend. The spatial unit is the end station. The demand variable is the return count at each station. The service variable is the OSM service profile around each station.

We do not compare raw weekday and weekend counts directly, because weekday trips are much more common. Instead, we compare station shares within each day type. In simple terms, we ask how important each station is within weekday trips, and how important it is within weekend trips.

Then we build a weighted service profile. Stations with more returns have more influence on the weekday or weekend service profile.

## Slide 5: Baseline Trip-Only Results

This baseline graph is supposed to demonstrate whether weekday and weekend trips already differ before we add OSM services.

The graph and table show that weekend trips are longer. The mean weekend duration is 17.15 minutes, compared with 13.47 minutes on weekdays. Weekend trips are also slightly longer by distance, with a mean of 2.27 kilometers compared with 2.18 kilometers on weekdays.

This supports the research question because it shows weekday and weekend trip behavior is not identical. But it is only a baseline. It does not tell us what kinds of places riders return bikes to, or what services are near those return stations. That is why we need the station and OSM analysis.

## Slide 6: End-Station Patterns And Spatial Heatmaps

This result is supposed to demonstrate whether weekday and weekend high-volume return stations are the same, and where the spatial differences appear.

The Top20 station comparison shows only 11 overlapping stations. That is a 55 percent overlap, with a union of 29 stations. So the high-volume weekday and weekend return stations are not identical.

The normalized heatmaps then show where the difference is located. Weekend-oriented stations appear more around lakefront and tourism areas. Weekday-oriented stations appear more around downtown commute areas.

This supports the research question because it shows the end-location pattern differs spatially. The limitation is that a heatmap only shows where. It does not explain the nearby service environment or rider intent.

## Slide 7: OSM Service Matching Around Return Stations

To improve the analysis beyond trip-only results, we add OSM service matching. The idea is simple: for each return station, we look at nearby OpenStreetMap points of interest and classify them into service categories.

The main categories include food_drink, office, tourism, transit, retail, health, education, and recreation. We use station coordinates for the matching, so the method is based on location instead of only station names.

The main setting uses the Top100 weekday and weekend union, a 250 meter radius, and excludes `other_amenity` from the main interpretation. We exclude it because it is too mixed and does not represent one clear type of destination environment.

## Slide 8: Main Service-Access Result

This result is supposed to demonstrate whether weekday- and weekend-weighted return stations have different nearby service profiles.

The service difference graph shows the main pattern. Tourism is weekend-oriented, with weekend minus weekday equal to +0.0355. Food_drink is weekday-oriented, with a difference of -0.0436. Office is also weekday-oriented, with a difference of -0.0135.

This supports the research question because it connects the end-location pattern to service access around the return stations. Weekend-weighted destinations are more associated with tourism services, while weekday-weighted destinations are more associated with food_drink and office.

The limitation is important: this does not prove why riders traveled. It only shows an association between return stations and nearby services.

## Slide 9: Validation And Sensitivity Checks

These validation graphs are supposed to show whether the main pattern is believable, stable, and not just random.

The label shuffle test gives p = 0.2657. That means we should not claim the whole profile difference is statistically significant under that test.

But two other tests are stronger. The station-demand randomization test has p = 0.0010. This means station popularity plus the larger weekday share do not fully explain the result under that null model. The station-service permutation test also has p = 0.0010. This means the real station-service pairing has structure.

Bootstrap supports tourism as weekend-oriented, and food_drink and office as weekday-oriented. Sensitivity checks show the main direction stays across Top20, Top50, and Top100, but radius choice still matters.

## Slide 10: Limitations, Final Claim, And Q&A

The final slide is supposed to explain what we can safely claim and what we cannot claim.

The main limitations are clear. End stations are destination proxies, not exact rider destinations. OSM services describe the nearby environment, but they do not prove rider intent. OSM coverage is also incomplete. For the Top100 union, the covered return share is 63.63 percent. The 250 meter radius is also a modeling choice.

Weather is only a secondary check. The rain-effect L1 is about 0.0089 for weekday and 0.0085 for weekend, so it is not the main story.

Our final conclusion is careful: weekday and weekend high-volume Divvy return destinations differ spatially and are associated with different nearby service environments. The result is exploratory and associative, not causal.
