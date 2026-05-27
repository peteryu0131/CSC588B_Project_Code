import math
import unittest

import pandas as pd

from src._pipeline_utils import (
    add_calendar_fields,
    filter_started_year,
    haversine_km,
    parse_full_timestamp,
    summary_by_group,
)


class PipelineUtilsTest(unittest.TestCase):
    def test_parse_full_timestamp_rejects_time_only_values(self):
        values = pd.Series(["2025-02-25 21:21:21.171", "23:54.5", None])

        parsed = parse_full_timestamp(values)

        self.assertFalse(pd.isna(parsed.iloc[0]))
        self.assertTrue(pd.isna(parsed.iloc[1]))
        self.assertTrue(pd.isna(parsed.iloc[2]))

    def test_add_calendar_fields_creates_day_type_month_hour_and_season(self):
        df = pd.DataFrame(
            {
                "started_at": pd.to_datetime(
                    ["2025-02-25 21:21:21", "2025-07-05 17:15:08"]
                )
            }
        )

        result = add_calendar_fields(df)

        self.assertEqual(result.loc[0, "day_type"], "weekday")
        self.assertEqual(result.loc[0, "month"], 2)
        self.assertEqual(result.loc[0, "hour"], 21)
        self.assertEqual(result.loc[0, "season"], "Winter")
        self.assertEqual(result.loc[1, "day_type"], "weekend")
        self.assertEqual(result.loc[1, "season"], "Summer")

    def test_filter_started_year_keeps_only_requested_year(self):
        df = pd.DataFrame(
            {
                "started_at": pd.to_datetime(
                    ["2024-12-31 23:59:00", "2025-01-01 00:00:00", "2026-01-01 00:00:00"]
                )
            }
        )

        result = filter_started_year(df, 2025)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["started_at"].year, 2025)

    def test_haversine_km_returns_reasonable_distance(self):
        distance = haversine_km(
            pd.Series([41.88314336]),
            pd.Series([-87.63724208]),
            pd.Series([41.89259212]),
            pd.Series([-87.61728913]),
        )

        self.assertTrue(math.isclose(distance.iloc[0], 1.95, rel_tol=0.08))

    def test_summary_by_group_uses_full_filtered_data(self):
        df = pd.DataFrame(
            {
                "day_type": ["weekday", "weekday", "weekend", "weekend"],
                "trip_length_km": [1.0, 3.0, 2.0, 10.0],
            }
        )

        summary = summary_by_group(df, "day_type", "trip_length_km")
        weekday = summary.set_index("day_type").loc["weekday"]

        self.assertEqual(weekday["count"], 2)
        self.assertEqual(weekday["mean"], 2.0)
        self.assertEqual(weekday["median"], 2.0)
        self.assertEqual(weekday["q1"], 1.5)
        self.assertEqual(weekday["q3"], 2.5)


if __name__ == "__main__":
    unittest.main()
