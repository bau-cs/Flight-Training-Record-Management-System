import csv
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import main
from main import (
    ValidationError,
    add_record_interactively,
    ask_until_valid,
    build_record,
    delete_record_interactively,
    load_records,
    main as run_app,
    parse_category,
    parse_date,
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

    def test_zero_duration_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("0")

    def test_negative_duration_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("-1")

    def test_duration_over_eight_hours_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("8.1")

    def test_non_numeric_duration_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("abc")

    def test_tiny_positive_duration_that_rounds_to_zero_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_duration("0.001")

    def test_non_finite_duration_is_rejected(self):
        for value in ("nan", "inf", "-inf"):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    parse_duration(value)

    def test_valid_category(self):
        self.assertEqual(parse_category("2"), "Solo Flight")

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_category("9")

    def test_valid_date_is_normalized(self):
        self.assertEqual(parse_date("2026-11-14"), "2026-11-14")

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_date("14-11-2026")

    def test_impossible_date_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_date("2026-02-30")

    def test_topic_whitespace_is_normalized(self):
        self.assertEqual(parse_topic("  IFR   navigation  "), "IFR navigation")

    def test_short_topic_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_topic("  ")

    def test_long_topic_is_rejected(self):
        with self.assertRaises(ValidationError):
            parse_topic("x" * 81)

    def test_valid_record_is_built(self):
        record = build_record("2026-11-14", "3", "1,25", "ILS approach")
        self.assertEqual(record["duration"], "Simulator")
        self.assertEqual(record["hours"], 1.25)

    def test_invalid_input_reprompts_until_valid(self):
        answers = iter(["abc", "1.0"])
        result = ask_until_valid("Sure: ", parse_duration, lambda _prompt: next(answers))
        self.assertEqual(result, 1.0)

    def test_missing_csv_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing.csv"
            self.assertEqual(load_records(path), [])

    def test_csv_save_and_load_round_trip(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            self.assertEqual(load_records(path), records)

    def test_csv_has_expected_columns(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            with path.open("r", newline="", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                self.assertEqual(next(reader), ["date", "duration", "hours", "topic"])

    def test_atomic_save_keeps_previous_csv_if_replace_fails(self):
        original = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        replacement = [build_record("2026-11-15", "3", "2", "Simulator session")]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(original, path)
            with patch("main.os.replace", side_effect=OSError("replace failed")):
                with self.assertRaises(OSError):
                    save_records(replacement, path)
            self.assertEqual(load_records(path), original)
            self.assertEqual(list(Path(temp_dir).glob(".*.tmp")), [])

    def test_legacy_csv_columns_are_readable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "legacy.csv"
            path.write_text(
                "date,category,duration_hours,topic\n"
                "2026-11-14,Dual Flight,1.5,Traffic pattern\n",
                encoding="utf-8",
            )
            loaded = load_records(path)
            self.assertEqual(loaded[0]["duration"], "Dual Flight")
            self.assertEqual(loaded[0]["hours"], 1.5)

    def test_invalid_csv_row_is_skipped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "mixed.csv"
            path.write_text(
                "date,duration,hours,topic\n"
                "2026-11-14,Dual Flight,1.5,Traffic pattern\n"
                "bad-date,Dual Flight,abc,\n",
                encoding="utf-8",
            )
            self.assertEqual(len(load_records(path)), 1)

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

    def test_add_record_interactively_saves_csv(self):
        answers = iter(["2026-11-15", "1", "1,5", "Traffic pattern"])
        records = []
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            with redirect_stdout(StringIO()):
                add_record_interactively(records, lambda _prompt: next(answers), path)
            self.assertEqual(len(records), 1)
            self.assertEqual(load_records(path), records)

    def test_add_record_rolls_back_when_save_fails(self):
        answers = iter(["2026-11-15", "1", "1.5", "Traffic pattern"])
        records = []
        with patch.object(main, "save_records", side_effect=OSError("disk error")):
            with redirect_stdout(StringIO()):
                add_record_interactively(records, lambda _prompt: next(answers), Path("unused.csv"))
        self.assertEqual(records, [])

    def test_delete_confirmed_removes_record_from_memory_and_csv(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        answers = iter(["1", "E"])
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            with redirect_stdout(StringIO()):
                delete_record_interactively(records, lambda _prompt: next(answers), path)
            self.assertEqual(records, [])
            self.assertEqual(load_records(path), [])

    def test_delete_invalid_confirmation_reprompts(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        answers = iter(["1", "maybe", "H"])
        output = StringIO()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            with redirect_stdout(output):
                delete_record_interactively(records, lambda _prompt: next(answers), path)
            self.assertEqual(len(records), 1)
            self.assertIn("E (evet) veya H (hayir)", output.getvalue())

    def test_delete_declined_keeps_record_and_csv(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        answers = iter(["1", "H"])
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            before = load_records(path)
            with redirect_stdout(StringIO()):
                delete_record_interactively(records, lambda _prompt: next(answers), path)
            self.assertEqual(records, before)
            self.assertEqual(load_records(path), before)

    def test_delete_invalid_selection_then_cancel(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        answers = iter(["not-a-number", "99", "0"])
        output = StringIO()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            save_records(records, path)
            with redirect_stdout(output):
                delete_record_interactively(records, lambda _prompt: next(answers), path)
            self.assertEqual(len(records), 1)
            self.assertIn("gecerli bir kayit numarasi", output.getvalue())
            self.assertIn("Silme islemi iptal edildi", output.getvalue())

    def test_delete_save_failure_restores_record(self):
        records = [build_record("2026-11-14", "1", "1.5", "Traffic pattern")]
        answers = iter(["1", "E"])
        with patch.object(main, "save_records", side_effect=OSError("disk error")):
            with redirect_stdout(StringIO()):
                delete_record_interactively(records, lambda _prompt: next(answers), Path("unused.csv"))
        self.assertEqual(len(records), 1)

    def test_delete_with_no_records_does_not_ask_for_input(self):
        with redirect_stdout(StringIO()):
            delete_record_interactively([], lambda _prompt: self.fail("Input should not be requested"))

    def test_main_menu_has_five_options_and_exits(self):
        answers = iter(["invalid", "5"])
        output = StringIO()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "records.csv"
            with redirect_stdout(output):
                run_app(lambda _prompt: next(answers), path)
        text = output.getvalue()
        self.assertIn("4. Ucus egitim kaydi sil", text)
        self.assertIn("5. Cikis", text)
        self.assertIn("Gecersiz menu secimi", text)
        self.assertIn("Programdan cikiliyor", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
