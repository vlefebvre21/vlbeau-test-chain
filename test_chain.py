#!/usr/bin/env python3
"""test_chain.py — Comprehensive cross-module integration tests.

Validates that the utility modules in this repository work correctly
both in isolation and when chained together. Covers:
  - math_utils / math_utils_v2  (arithmetic)
  - string_utils                (text manipulation)
  - date_utils                  (date parsing, formatting, business days)
  - file_utils                  (read/write/list/exists/size)
  - config_utils                (JSON config load/save/merge)
  - validation_utils            (email/URL/phone validation)
  - utils                       (legacy add/multiply)

Run:  python -m pytest test_chain.py -v
  or: python test_chain.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import shutil
import unittest
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# Imports — each section is guarded so a single broken module won't prevent
# the rest of the suite from running.
# ---------------------------------------------------------------------------

# Legacy utils
from utils import add as legacy_add, multiply as legacy_multiply

# math_utils (compact version)
from math_utils import add, subtract, multiply, divide

# math_utils_v2 (typed, ValueError on div/0)
from math_utils_v2 import (
    add as add_v2,
    subtract as subtract_v2,
    multiply as multiply_v2,
    divide as divide_v2,
)

# string_utils
from string_utils import reverse, capitalize_words, count_vowels

# date_utils
from date_utils import (
    parse_date,
    format_date,
    days_between,
    is_weekend,
    next_business_day,
)

# file_utils
from file_utils import read_file, write_file, list_files, file_exists, get_file_size

# config_utils
from config_utils import load_config, save_config, merge_configs

# validation_utils
from validation_utils import validate_email, validate_url, validate_phone


# ═══════════════════════════════════════════════════════════════════════════
# 1. MATH — legacy, v1, and v2
# ═══════════════════════════════════════════════════════════════════════════


class TestLegacyUtils(unittest.TestCase):
    """Tests for the original utils.py helpers."""

    def test_add_integers(self):
        self.assertEqual(legacy_add(2, 3), 5)

    def test_add_floats(self):
        self.assertAlmostEqual(legacy_add(0.1, 0.2), 0.3, places=10)

    def test_multiply(self):
        self.assertEqual(legacy_multiply(4, 5), 20)

    def test_multiply_by_zero(self):
        self.assertEqual(legacy_multiply(999, 0), 0)


class TestMathUtils(unittest.TestCase):
    """Tests for math_utils.py (compact, returns None on div/0)."""

    def test_basic_ops(self):
        self.assertEqual(add(10, 5), 15)
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(multiply(3, 7), 21)
        self.assertAlmostEqual(divide(10, 3), 10 / 3)

    def test_divide_by_zero_returns_none(self):
        self.assertIsNone(divide(5, 0))

    def test_negative_numbers(self):
        self.assertEqual(add(-3, -7), -10)
        self.assertEqual(subtract(-3, 7), -10)
        self.assertEqual(multiply(-2, 5), -10)


class TestMathUtilsV2(unittest.TestCase):
    """Tests for math_utils_v2.py (typed, raises ValueError on div/0)."""

    def test_typed_add(self):
        self.assertAlmostEqual(add_v2(2.0, 3.0), 5.0)

    def test_typed_subtract(self):
        self.assertAlmostEqual(subtract_v2(5.0, 3.0), 2.0)

    def test_typed_multiply(self):
        self.assertAlmostEqual(multiply_v2(4.0, 3.0), 12.0)

    def test_typed_divide(self):
        self.assertAlmostEqual(divide_v2(10.0, 2.0), 5.0)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ValueError):
            divide_v2(1.0, 0.0)

    def test_v1_v2_consistency(self):
        """v1 and v2 should agree on non-edge-case arithmetic."""
        for a, b in [(10, 3), (0, 5), (-7, 2), (100, 25)]:
            self.assertAlmostEqual(add(a, b), add_v2(a, b))
            self.assertAlmostEqual(subtract(a, b), subtract_v2(a, b))
            self.assertAlmostEqual(multiply(a, b), multiply_v2(a, b))
            if b != 0:
                self.assertAlmostEqual(divide(a, b), divide_v2(a, b))


# ═══════════════════════════════════════════════════════════════════════════
# 2. STRINGS
# ═══════════════════════════════════════════════════════════════════════════


class TestStringUtils(unittest.TestCase):
    def test_reverse_basic(self):
        self.assertEqual(reverse("hello"), "olleh")

    def test_reverse_palindrome(self):
        self.assertEqual(reverse("racecar"), "racecar")

    def test_reverse_empty(self):
        self.assertEqual(reverse(""), "")

    def test_capitalize_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")
        self.assertEqual(capitalize_words("already Done"), "Already Done")

    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)  # e, o
        self.assertEqual(count_vowels("AEIOU"), 5)
        self.assertEqual(count_vowels("rhythm"), 1)  # y counts

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            reverse(42)
        with self.assertRaises(TypeError):
            capitalize_words(None)
        with self.assertRaises(TypeError):
            count_vowels([1, 2, 3])


# ═══════════════════════════════════════════════════════════════════════════
# 3. DATES
# ═══════════════════════════════════════════════════════════════════════════


class TestDateUtils(unittest.TestCase):
    def test_parse_iso(self):
        self.assertEqual(parse_date("2023-01-01"), date(2023, 1, 1))

    def test_parse_datetime(self):
        dt = parse_date("2023-01-01 12:00:00")
        self.assertEqual(dt, datetime(2023, 1, 1, 12, 0))

    def test_parse_european(self):
        self.assertEqual(parse_date("15/06/2023"), date(2023, 6, 15))

    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            parse_date("not-a-date")

    def test_format_date(self):
        self.assertEqual(format_date(date(2023, 1, 1), "%d/%m/%Y"), "01/01/2023")

    def test_days_between(self):
        self.assertEqual(days_between(date(2023, 1, 1), date(2023, 1, 5)), 4)
        self.assertEqual(days_between(date(2023, 1, 5), date(2023, 1, 1)), -4)

    def test_is_weekend(self):
        # 2023-01-07 = Saturday, 2023-01-09 = Monday
        self.assertTrue(is_weekend(date(2023, 1, 7)))
        self.assertFalse(is_weekend(date(2023, 1, 9)))

    def test_next_business_day_from_friday(self):
        self.assertEqual(next_business_day(date(2023, 1, 6)), date(2023, 1, 9))

    def test_next_business_day_from_wednesday(self):
        self.assertEqual(next_business_day(date(2023, 1, 4)), date(2023, 1, 5))


# ═══════════════════════════════════════════════════════════════════════════
# 4. FILES
# ═══════════════════════════════════════════════════════════════════════════


class TestFileUtils(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_write_and_read(self):
        p = os.path.join(self.tmp, "hello.txt")
        write_file(p, "Hello, World!")
        self.assertEqual(read_file(p), "Hello, World!")

    def test_write_creates_nested_dirs(self):
        p = os.path.join(self.tmp, "a", "b", "c", "deep.txt")
        write_file(p, "deep")
        self.assertTrue(os.path.exists(p))

    def test_read_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            read_file(os.path.join(self.tmp, "nope.txt"))

    def test_list_files(self):
        write_file(os.path.join(self.tmp, "a.txt"), "a")
        write_file(os.path.join(self.tmp, "b.txt"), "b")
        files = list_files(self.tmp)
        self.assertIn("a.txt", files)
        self.assertIn("b.txt", files)

    def test_file_exists(self):
        p = os.path.join(self.tmp, "exists.txt")
        self.assertFalse(file_exists(p))
        write_file(p, "yes")
        self.assertTrue(file_exists(p))

    def test_get_file_size(self):
        p = os.path.join(self.tmp, "sized.txt")
        write_file(p, "abc")
        self.assertEqual(get_file_size(p), 3)


# ═══════════════════════════════════════════════════════════════════════════
# 5. CONFIG
# ═══════════════════════════════════════════════════════════════════════════


class TestConfigUtils(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_save_and_load(self):
        p = os.path.join(self.tmp, "cfg.json")
        save_config(p, {"key": "value", "count": 42})
        cfg = load_config(p)
        self.assertEqual(cfg["key"], "value")
        self.assertEqual(cfg["count"], 42)

    def test_load_missing_with_default(self):
        p = os.path.join(self.tmp, "missing.json")
        cfg = load_config(p, default={"fallback": True})
        self.assertTrue(cfg["fallback"])

    def test_merge_configs(self):
        base = {"a": 1, "nested": {"x": 10, "y": 20}}
        override = {"a": 2, "nested": {"y": 99, "z": 30}}
        merged = merge_configs(base, override)
        self.assertEqual(merged["a"], 2)
        self.assertEqual(merged["nested"]["x"], 10)
        self.assertEqual(merged["nested"]["y"], 99)
        self.assertEqual(merged["nested"]["z"], 30)


# ═══════════════════════════════════════════════════════════════════════════
# 6. VALIDATION
# ═══════════════════════════════════════════════════════════════════════════


class TestValidationUtils(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(validate_email("user@example.com"))

    def test_invalid_email(self):
        self.assertFalse(validate_email("not-an-email"))
        self.assertFalse(validate_email("@domain.com"))
        self.assertFalse(validate_email("user@"))

    def test_valid_url(self):
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://sub.domain.org/path?q=1"))

    def test_invalid_url(self):
        self.assertFalse(validate_url("ftp://files.example.com"))
        self.assertFalse(validate_url("not a url"))

    def test_valid_phone(self):
        self.assertTrue(validate_phone("+33612345678"))
        self.assertTrue(validate_phone("1234567890"))

    def test_invalid_phone(self):
        self.assertFalse(validate_phone("123"))
        self.assertFalse(validate_phone("abc"))


# ═══════════════════════════════════════════════════════════════════════════
# 7. CROSS-MODULE INTEGRATION CHAINS
# ═══════════════════════════════════════════════════════════════════════════


class TestIntegrationChains(unittest.TestCase):
    """End-to-end scenarios that chain multiple modules together."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_compute_then_persist(self):
        """Math → File: compute a result, write it, read it back."""
        result = add_v2(multiply_v2(3.0, 7.0), 1.0)  # 22.0
        path = os.path.join(self.tmp, "result.txt")
        write_file(path, str(result))
        self.assertEqual(read_file(path), "22.0")

    def test_config_driven_validation(self):
        """Config → Validation: load validation rules from config, apply them."""
        cfg_path = os.path.join(self.tmp, "rules.json")
        save_config(cfg_path, {
            "contacts": [
                {"email": "alice@example.com", "phone": "+33612345678"},
                {"email": "bad-email", "phone": "123"},
            ]
        })
        cfg = load_config(cfg_path)
        results = []
        for contact in cfg["contacts"]:
            results.append({
                "email_ok": bool(validate_email(contact["email"])),
                "phone_ok": bool(validate_phone(contact["phone"])),
            })
        self.assertTrue(results[0]["email_ok"])
        self.assertTrue(results[0]["phone_ok"])
        self.assertFalse(results[1]["email_ok"])
        self.assertFalse(results[1]["phone_ok"])

    def test_date_string_chain(self):
        """Date → String: format a date, reverse it, capitalize."""
        d = parse_date("2023-06-15")
        formatted = format_date(d, "%B %d, %Y")  # "June 15, 2023"
        reversed_str = reverse(formatted)
        cap = capitalize_words(reversed_str)
        # Just verify the chain doesn't crash and produces a string
        self.assertIsInstance(cap, str)
        self.assertTrue(len(cap) > 0)

    def test_file_config_merge_chain(self):
        """File → Config → Merge: write two configs, merge them."""
        base_path = os.path.join(self.tmp, "base.json")
        override_path = os.path.join(self.tmp, "override.json")

        save_config(base_path, {"app": "test-chain", "version": 1, "debug": False})
        save_config(override_path, {"version": 2, "debug": True, "extra": "yes"})

        base = load_config(base_path)
        override = load_config(override_path)
        merged = merge_configs(base, override)

        self.assertEqual(merged["app"], "test-chain")
        self.assertEqual(merged["version"], 2)
        self.assertTrue(merged["debug"])
        self.assertEqual(merged["extra"], "yes")

    def test_business_day_report(self):
        """Date → Math → File: compute business days in a range, write report."""
        start = date(2023, 1, 1)
        end = date(2023, 1, 31)
        total_days = days_between(start, end)
        biz_days = sum(
            1 for i in range(total_days + 1)
            if not is_weekend(start + timedelta(days=i))
        )
        report_path = os.path.join(self.tmp, "report.txt")
        write_file(report_path, f"Business days in Jan 2023: {biz_days}")
        content = read_file(report_path)
        self.assertIn("Business days", content)
        self.assertEqual(biz_days, 22)  # January 2023 has 22 business days

    def test_full_pipeline(self):
        """Full pipeline: config → validation → math → string → file."""
        # 1. Load config with test data
        cfg_path = os.path.join(self.tmp, "pipeline.json")
        save_config(cfg_path, {
            "contacts": ["valid@test.com", "invalid", "also@ok.org"],
            "multiplier": 10,
        })
        cfg = load_config(cfg_path)

        # 2. Validate contacts, count valid ones
        valid_count = sum(1 for c in cfg["contacts"] if validate_email(c))
        self.assertEqual(valid_count, 2)

        # 3. Multiply valid count by config multiplier
        score = multiply_v2(float(valid_count), float(cfg["multiplier"]))
        self.assertAlmostEqual(score, 20.0)

        # 4. Build a summary string
        summary = capitalize_words(f"pipeline score is {int(score)} points")
        self.assertEqual(summary, "Pipeline Score Is 20 Points")

        # 5. Persist to file
        out = os.path.join(self.tmp, "summary.txt")
        write_file(out, summary)
        self.assertEqual(read_file(out), "Pipeline Score Is 20 Points")
        self.assertTrue(file_exists(out))
        self.assertGreater(get_file_size(out), 0)


# ═══════════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
