import tempfile
import unittest
from pathlib import Path

from main import (
    ValidationError,
    build_record,
    ask_until_valid,
    parse_date,
    load_records,
    parse_category,
    parse_duration,
    parse_topic,
    save_records,
    summarize_records,
)


class TestFlightTrainingLog(unittest.TestCase):
    def test_valid_duration(self):
        self.assertEqual(parse_duration("1.5"), 1.5)

    def test_decimal_comma_is_supported(self):
        self.assertEqual(parse_duration("1,5"), 1.5)

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_date("14-11-2026")

    def test_invalid_duration_reprompts_until_valid(self):
        answers = iter(["abc", "1.0"])
        result = ask_until_valid("Sure: ", parse_duration, lambda _prompt: next(answers))
        self.assertEqual(result, 1.0)

    def test_zero_duration_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("0")

    def test_duration_over_eight_hours_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("8.1")

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_category("9")

    def test_short_topic_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_topic("  ")

    def test_valid_record_is_built(self):
        record = build_record("2026-11-14", "3", "1,25", "ILS approach")
        self.assertEqual(record["duration"], "Simulator")
        self.assertEqual(record["hours"], 1.25)

    def test_csv_save_and_load_round_trip(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            self.assertEqual(load_records(path), records)

    def test_csv_has_separate_date_duration_hours_topic_columns(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            with path.open("r", newline="", encoding="utf-8") as csv_file:
                import csv
                reader = csv.reader(csv_file)
                self.assertEqual(next(reader), ["date", "duration", "hours", "topic"])
                self.assertEqual(next(reader), ["2026-11-14", "Dual Flight", "1.5", "Traffic pattern"])

    def test_legacy_csv_columns_are_still_readable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "legacy.csv"
            path.write_text(
                "date,category,duration_hours,topic\n"
                "2026-11-14,Dual Flight,1.5,Traffic pattern\n",
                encoding="utf-8",
            )
            loaded = load_records(path)
            self.assertEqual(loaded[0], {
                "date": "2026-11-14",
                "duration": "Dual Flight",
                "hours": 1.5,
                "topic": "Traffic pattern",
            })

    def test_summary_calculates_total_and_categories(self):
        records = [
            build_record("2026-11-14", "1", "1.5", "Traffic pattern"),
            build_record("2026-11-13", "3", "2", "Navigation practice"),
        ]
        summary = summarize_records(records)
        self.assertEqual(summary["record_count"], 2)
        self.assertEqual(summary["total_hours"], 3.5)
        self.assertEqual(summary["category_hours"]["Dual Flight"], 1.5)
        self.assertEqual(summary["category_hours"]["Simulator"], 2.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
