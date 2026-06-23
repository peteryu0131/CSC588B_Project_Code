# CSC588B Final Project Presentation Q&A

## Q1. Why is weekday versus weekend not too simple?

It would be too simple if we only compared trip counts. Our project uses weekday versus weekend as the temporal split, but the real question is spatial. We compare high-volume return stations, normalized destination patterns, and nearby OSM service environments.

## Q2. Why use end stations?

The research question is about destination patterns. The public Divvy data does not show the rider's final activity after the trip, so the end station is the best available destination proxy. We do not claim it proves the exact final place the rider visited.

## Q3. Why add OSM services?

Trip duration and distance can show that weekday and weekend behavior differs, but they do not explain what kinds of places are near the return stations. OSM services add context around each station, such as food_drink, office, tourism, transit, retail, health, education, and recreation.

## Q4. Why use 250 meters?

The 250 meter radius is a local station-neighborhood scale. It is close enough to describe the area around a station without making the area too broad. The notebook also checks 100m and 500m, and the sensitivity result shows radius matters. So 250m is a defensible setting, not a universal truth.

## Q5. How were spatial outliers handled?

The cleaning pipeline filters invalid or missing coordinates and applies coordinate filtering for the Chicago analysis area. The coordinate filter removed 5,535 rows. This matters because incorrect coordinates would affect heatmaps, station aggregation, and OSM matching.

## Q6. What other cleaning was done?

The pipeline filters timestamps, trips outside the 2025 date range, invalid coordinates, invalid durations, and invalid distances. The final cleaned dataset has 5,547,168 rows from 5,552,994 original rows.

## Q7. What is the baseline comparison?

The baseline is trip-only weekday/weekend analysis. Weekend trips have longer mean duration, 17.15 minutes versus 13.47 minutes, and slightly longer mean length, 2.27 km versus 2.18 km. The Top20 return-station overlap is 55%, so high-volume weekday and weekend destinations are not identical.

## Q8. Why normalize station shares?

Weekday trips are much more common than weekend trips. If we used raw counts only, weekday stations would dominate. Normalized station share compares station importance within weekday and within weekend separately.

## Q9. What does the main OSM result show?

In the Top100 union at 250m, excluding `other_amenity`, weekend-weighted destinations are more tourism-associated. Tourism has weekend minus weekday = +0.0355. Weekday-weighted destinations are more food_drink and office-associated, with food_drink = -0.0436 and office = -0.0135.

## Q10. What does validation show?

Validation is mixed but useful. Label shuffle has p = 0.2657, so we should not claim overall statistical significance. But station-demand randomization has p = 0.0010, and station-service permutation also has p = 0.0010. Those tests show the pattern has structure under those null comparisons.

## Q11. What does bootstrap show?

Bootstrap checks whether category directions are stable when stations are resampled. It supports tourism as weekend-oriented, and food_drink, office, and health as weekday-oriented. Transit is descriptive only because its interval crosses zero.

## Q12. Does this prove weekend riders go to tourist attractions?

No. It shows that weekend-weighted return stations are more associated with nearby tourism services. It does not prove individual rider intent or the exact place each rider visited.

## Q13. Does OSM explain rider behavior?

No. OSM describes nearby service environments. It helps interpret the station context, but it does not prove those services caused the trips.

## Q14. What is the main limitation?

The biggest limitation is that end stations are only destination proxies. Riders may walk somewhere else after returning a bike. Another important limitation is OSM coverage: for the Top100 union, the covered return share is 63.63%, so missing OSM coverage could affect the profile.

## Q15. Why exclude `other_amenity`?

`other_amenity` mixes many different things, such as parking, benches, toilets, banks, and vending machines. It is useful for raw context, but it is too broad for the main interpretation.

## Q16. What role does weather play?

Weather is a secondary check, not the main research question. The rain-effect L1 is about 0.0089 for weekday and 0.0085 for weekend, so weather does not become the main explanation in this presentation.

## Q17. What will be improved in the final paper?

The final paper can improve the project by expanding OSM coverage, explaining missing coverage more clearly, discussing radius choice, and writing the limitations in more detail. It can also explain how the live presentation feedback was integrated into the final version.

## Q18. What is the safest final answer if asked for the main conclusion?

Weekday and weekend high-volume Divvy return destinations differ spatially and are associated with different nearby OSM service environments. Weekend-weighted destinations are more tourism-associated, while weekday-weighted destinations are more food_drink and office-associated. This is an exploratory association, not a causal claim.
