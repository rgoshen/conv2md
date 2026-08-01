"""Unit tests for markdown security controls."""

import unittest

from conv2md.markdown.constants import MAX_METADATA_VALUE_LENGTH
from conv2md.markdown.security import (
    sanitize_yaml_metadata,
    sanitize_yaml_value,
    validate_timestamp,
)

try:  # pragma: no cover - availability depends on the local environment
    import yaml

    YAML_AVAILABLE = True
except ImportError:  # pragma: no cover
    yaml = None
    YAML_AVAILABLE = False

SECURITY_LOGGER = "conv2md.markdown.security"


class TestYamlValueSanitization(unittest.TestCase):
    """Test that metadata values become valid double-quoted YAML scalars."""

    def test_sanitize_yaml_value_returns_double_quoted_scalar(self):
        """Values are wrapped in double quotes with YAML-legal escapes."""
        cases = [
            # (description, raw value, expected quoted scalar)
            ("plain", "Test Conversation", '"Test Conversation"'),
            ("colon", "Chapter 1: Intro", '"Chapter 1: Intro"'),
            ("apostrophe", "it's fine", '"it\'s fine"'),
            ("hyphen", "well-known", '"well-known"'),
            ("leading dash", "- list item", '"- list item"'),
            ("hash", "# not a comment", '"# not a comment"'),
            ("pipe", "| not a block", '"| not a block"'),
            ("angle", "> not folded", '"> not folded"'),
            ("brackets", "[a, b]", '"[a, b]"'),
            ("braces", "{k: v}", '"{k: v}"'),
            ("double quote", 'He said "hi"', r'"He said \"hi\""'),
            ("backslash", r"C:\Users\x", r'"C:\\Users\\x"'),
            ("newline", "line1\nline2", r'"line1\nline2"'),
            ("carriage return", "line1\rline2", r'"line1\rline2"'),
            ("tab", "a\tb", r'"a\tb"'),
            ("html markup", "<script>alert(1)</script>", '"<script>alert(1)</script>"'),
            ("ampersand", "a & b", '"a & b"'),
            ("empty", "", '""'),
        ]

        for description, raw, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(sanitize_yaml_value(raw), expected)

    def test_sanitize_yaml_value_does_not_html_escape(self):
        """HTML entities must never be baked into metadata values."""
        for raw in ["it's fine", 'say "hi"', "a & b", "<b>"]:
            with self.subTest(raw=raw):
                self.assertNotIn("&#x", sanitize_yaml_value(raw))
                self.assertNotIn("&quot;", sanitize_yaml_value(raw))
                self.assertNotIn("&amp;", sanitize_yaml_value(raw))

    def test_sanitize_yaml_value_strips_control_characters(self):
        """Control characters are removed, printable text is preserved."""
        cases = [
            ("null byte", "bad\x00value", '"badvalue"'),
            ("start of heading", "bad\x01value", '"badvalue"'),
            ("vertical tab", "bad\x0bvalue", '"badvalue"'),
            ("form feed", "bad\x0cvalue", '"badvalue"'),
            ("delete", "bad\x7fvalue", '"badvalue"'),
        ]

        for description, raw, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(sanitize_yaml_value(raw), expected)

    def test_sanitize_yaml_value_coerces_non_string_values(self):
        """Non-string metadata values are stringified then quoted."""
        cases = [(42, '"42"'), (3.5, '"3.5"'), (True, '"True"'), (None, '"None"')]

        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(sanitize_yaml_value(raw), expected)

    def test_sanitize_yaml_value_truncates_before_escaping(self):
        """Truncation applies to the raw value, not the escaped output."""
        result = sanitize_yaml_value("a" * (MAX_METADATA_VALUE_LENGTH + 500))
        self.assertEqual(result, '"' + "a" * MAX_METADATA_VALUE_LENGTH + '"')

        # Backslashes double after truncation, so the cap bounds raw input only.
        escaped = sanitize_yaml_value("\\" * (MAX_METADATA_VALUE_LENGTH + 500))
        self.assertEqual(escaped, '"' + "\\\\" * MAX_METADATA_VALUE_LENGTH + '"')

    @unittest.skipUnless(YAML_AVAILABLE, "PyYAML not installed")
    def test_sanitized_values_round_trip_through_yaml_parser(self):
        """A sanitized value parses back to the original text."""
        raw_values = [
            "Chapter 1: Intro",
            "it's fine",
            "well-known",
            r"C:\Users\x",
            'He said "hi"',
            "line1\nline2",
            "a\tb",
            "- list item\n  nested: value",
            "# comment",
            "*anchor",
            "&anchor",
            "!!python/object:os.system",
            "<script>alert('xss')</script>",
            "value with: colon",
            "",
        ]

        for raw in raw_values:
            with self.subTest(raw=raw):
                document = f"title: {sanitize_yaml_value(raw)}"
                parsed = yaml.safe_load(document)
                self.assertEqual(parsed["title"], raw)


class TestMetadataKeySanitization(unittest.TestCase):
    """Test metadata key sanitization and collision handling."""

    def test_key_collision_warns_before_overwriting(self):
        """Colliding sanitized keys emit a warning naming the lost field."""
        metadata = {"title#1": "FIRST", "title1": "SECOND"}

        with self.assertLogs(SECURITY_LOGGER, level="WARNING") as captured:
            result = sanitize_yaml_metadata(metadata)

        self.assertEqual(result["title1"], '"SECOND"')
        self.assertEqual(len(captured.output), 1)
        self.assertIn("title1", captured.output[0])

    def test_no_warning_when_keys_are_unique(self):
        """Distinct keys must not produce collision warnings."""
        metadata = {"title": "A", "source": "B"}

        with self.assertNoLogs(SECURITY_LOGGER, level="WARNING"):
            result = sanitize_yaml_metadata(metadata)

        self.assertEqual(result, {"title": '"A"', "source": '"B"'})

    def test_invalid_keys_are_dropped(self):
        """Keys with no allowed characters are skipped entirely."""
        result = sanitize_yaml_metadata({"###": "value", "ok": "kept"})
        self.assertEqual(result, {"ok": '"kept"'})


class TestTimestampValidation(unittest.TestCase):
    """Test timestamp validation functionality."""

    def test_validate_timestamp_iso8601_formats(self):
        """Test validation of ISO8601 timestamp formats."""
        valid_timestamps = [
            "2024-08-18T14:30:00Z",
            "2024-08-18T14:30:00+00:00",
            "2024-08-18T14:30:00-05:00",
            "2024-08-18 14:30:00",
            "2024-08-18",
            "2024-02-29",  # Leap day in a leap year
            "2024-12-31",
            "2024-01-01",
        ]

        for timestamp in valid_timestamps:
            with self.subTest(timestamp=timestamp):
                result = validate_timestamp(timestamp)
                self.assertEqual(result, timestamp)

    def test_validate_timestamp_time_only_formats(self):
        """Test validation of time-only formats."""
        valid_timestamps = [
            "14:30:00",
            "14:30",
            "2:30 PM",
            "2:30 AM",
            "02:30:45",
        ]

        for timestamp in valid_timestamps:
            with self.subTest(timestamp=timestamp):
                result = validate_timestamp(timestamp)
                self.assertEqual(result, timestamp)

    def test_validate_timestamp_unix_formats(self):
        """Test validation of Unix timestamp formats."""
        valid_timestamps = [
            "1692364200",  # Unix timestamp
            "1692364200.123",  # Unix with milliseconds
        ]

        for timestamp in valid_timestamps:
            with self.subTest(timestamp=timestamp):
                result = validate_timestamp(timestamp)
                self.assertEqual(result, timestamp)

    def test_validate_timestamp_invalid_formats(self):
        """Test rejection of invalid timestamp formats."""
        invalid_timestamps = [
            "not-a-timestamp",
            "abcd-ef-gh",
            "2024/13/40",  # Invalid date
            "25:00:00",  # Invalid time
            "random text",
            "javascript:alert(1)",  # Security test
            "<script>alert(1)</script>",  # XSS attempt
        ]

        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                with self.assertRaises(ValueError):
                    validate_timestamp(timestamp)

    def test_validate_timestamp_rejects_out_of_range_date_parts(self):
        """Month and day fields outside their valid ranges are rejected."""
        invalid_timestamps = [
            "2024-13-40",
            "2024-00-00",
            "9999-99-99",
            "2024-00-10",
            "2024-13-01",
            "2024-01-00",
            "2024-01-32",
            "2024-13-01T00:00:00Z",
            "2024-01-32 10:00:00",
        ]

        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                with self.assertRaises(ValueError):
                    validate_timestamp(timestamp)

    def test_validate_timestamp_rejects_impossible_calendar_dates(self):
        """Dates that pass field bounds but do not exist are rejected."""
        invalid_timestamps = [
            "2024-02-30",
            "2023-02-29",  # 2023 is not a leap year
            "2024-04-31",
            "2024-06-31",
            "2024-09-31",
            "2024-11-31",
            "2024-02-30T10:00:00Z",
            "2023-02-29 10:00:00",
        ]

        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                with self.assertRaises(ValueError):
                    validate_timestamp(timestamp)

    def test_validate_timestamp_edge_cases(self):
        """Test edge cases for timestamp validation."""
        # Empty string should return empty
        self.assertEqual(validate_timestamp(""), "")

        # Whitespace only should return empty
        self.assertEqual(validate_timestamp("   "), "")

        # Very long valid timestamp should be truncated but still valid
        long_valid_timestamp = "2024-08-18T14:30:00.123456789012345678901234567890Z"
        result = validate_timestamp(long_valid_timestamp)
        self.assertLessEqual(len(result), 50)  # MAX_TIMESTAMP_LENGTH

        # Long invalid timestamp should fail validation
        long_invalid_timestamp = "2024-08-18T14:30:00Z" + "x" * 100
        with self.assertRaises(ValueError):
            validate_timestamp(long_invalid_timestamp)

    def test_validate_timestamp_removes_control_characters(self):
        """Test that control characters are removed."""
        timestamp_with_control = "2024-08-18\x00T14:30:00\x01Z"
        result = validate_timestamp(timestamp_with_control)
        self.assertEqual(result, "2024-08-18T14:30:00Z")


if __name__ == "__main__":
    unittest.main()
