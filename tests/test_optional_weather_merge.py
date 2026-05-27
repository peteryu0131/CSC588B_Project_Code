import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

spec = importlib.util.spec_from_file_location(
    "optional_weather_merge",
    SRC_DIR / "05_optional_weather_merge.py",
)
optional_weather_merge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(optional_weather_merge)


class OptionalWeatherMergeTest(unittest.TestCase):
    def test_find_weather_file_supports_data_raw_root_location(self):
        root = Path("C:/project")
        weather_path = root / "data" / "raw" / optional_weather_merge.WEATHER_FILENAME

        def fake_exists(path):
            return path == weather_path

        with patch.object(Path, "exists", fake_exists):
            self.assertEqual(optional_weather_merge.find_weather_file(root), weather_path)


if __name__ == "__main__":
    unittest.main()
