"""Unit tests for markdown security controls."""

import unittest

from conv2md.markdown.constants import (
    MAX_CONTENT_SANITIZATION_SIZE,
    MAX_METADATA_VALUE_LENGTH,
    MAX_SPEAKER_NAME_LENGTH,
    MAX_TIMESTAMP_LENGTH,
)
from conv2md.markdown.security import (
    sanitize_content,
    sanitize_yaml_metadata,
    sanitize_yaml_value,
    validate_speaker_name,
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


class TestSpeakerNameValidation(unittest.TestCase):
    """Test speaker name validation directly, not through the generator."""

    def test_rejects_input_with_no_usable_characters(self):
        """Empty, blank and control-only names raise with a specific message."""
        cases = [
            # (description, raw speaker, expected message fragment)
            ("empty string", "", "cannot be empty"),
            ("spaces only", "   ", "cannot be empty"),
            ("tabs and newlines only", "\t\n\r", "cannot be empty"),
            # \x0B and \x0C are whitespace to str.strip(), so they are caught by
            # the emptiness check rather than the control-character check.
            ("vertical tab and form feed only", "\x0b\x0c", "cannot be empty"),
            ("control characters only", "\x00\x01\x02", "only invalid characters"),
            ("delete character only", "\x7f", "only invalid characters"),
        ]

        for description, raw, expected_fragment in cases:
            with self.subTest(case=description):
                with self.assertRaises(ValueError) as caught:
                    validate_speaker_name(raw)
                self.assertIn(expected_fragment, str(caught.exception))

    def test_accepts_and_cleans_valid_names(self):
        """Surrounding whitespace is stripped and control bytes are dropped."""
        cases = [
            # (description, raw speaker, expected result)
            ("plain", "Alice", "Alice"),
            ("surrounding whitespace", "  Alice  ", "Alice"),
            ("embedded null byte", "Al\x00ice", "Alice"),
            ("embedded newline", "Al\nice", "Alice"),
            ("embedded tab", "Al\tice", "Alice"),
            ("embedded delete", "Al\x7fice", "Alice"),
            ("internal spaces kept", "Dr. Jane Doe", "Dr. Jane Doe"),
            ("unicode kept", "Ana Lopez", "Ana Lopez"),
        ]

        for description, raw, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(validate_speaker_name(raw), expected)

    def test_truncates_names_beyond_the_length_limit(self):
        """Over-long names are cut to MAX_SPEAKER_NAME_LENGTH."""
        result = validate_speaker_name("a" * (MAX_SPEAKER_NAME_LENGTH + 50))
        self.assertEqual(result, "a" * MAX_SPEAKER_NAME_LENGTH)

    def test_name_at_the_length_limit_is_untouched(self):
        """A name of exactly the limit survives intact."""
        exact = "b" * MAX_SPEAKER_NAME_LENGTH
        self.assertEqual(validate_speaker_name(exact), exact)


class TestContentSanitization(unittest.TestCase):
    """Test content sanitization, including its truncation boundary."""

    def test_empty_content_reports_no_truncation(self):
        """Falsy content short-circuits to an empty, untruncated result."""
        self.assertEqual(sanitize_content(""), ("", False))

    def test_truncation_boundary(self):
        """Truncation begins only past MAX_CONTENT_SANITIZATION_SIZE."""
        cases = [
            # (description, input length, expected truncated flag)
            ("one below the limit", MAX_CONTENT_SANITIZATION_SIZE - 1, False),
            ("exactly at the limit", MAX_CONTENT_SANITIZATION_SIZE, False),
            ("one above the limit", MAX_CONTENT_SANITIZATION_SIZE + 1, True),
            ("far above the limit", MAX_CONTENT_SANITIZATION_SIZE * 2, True),
        ]

        for description, length, expected_truncated in cases:
            with self.subTest(case=description):
                content, truncated = sanitize_content("a" * length)
                self.assertEqual(truncated, expected_truncated)
                self.assertEqual(
                    len(content), min(length, MAX_CONTENT_SANITIZATION_SIZE)
                )
                self.assertEqual(content, "a" * len(content))

    def test_strips_control_characters_but_keeps_whitespace(self):
        """Control bytes are dropped; newline and tab carry meaning and stay."""
        cases = [
            # (description, raw content, expected content)
            ("null byte", "a\x00b", "ab"),
            ("start of heading", "a\x01b", "ab"),
            ("vertical tab", "a\x0bb", "ab"),
            ("form feed", "a\x0cb", "ab"),
            ("delete", "a\x7fb", "ab"),
            ("newline kept", "a\nb", "a\nb"),
            ("tab kept", "a\tb", "a\tb"),
        ]

        for description, raw, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(sanitize_content(raw), (expected, False))

    def test_normalizes_line_endings(self):
        """CRLF and lone CR both collapse to LF."""
        cases = [
            ("crlf", "a\r\nb", "a\nb"),
            ("lone cr", "a\rb", "a\nb"),
            ("mixed", "a\r\nb\rc\nd", "a\nb\nc\nd"),
            ("trailing crlf", "a\r\n", "a\n"),
        ]

        for description, raw, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(sanitize_content(raw), (expected, False))

    def test_crlf_split_by_truncation_leaves_no_stray_carriage_return(self):
        """A CRLF pair cut in half must not surface a lone CR in the output."""
        # Place "\r" at the last kept index and "\n" just past the cut.
        raw = "a" * (MAX_CONTENT_SANITIZATION_SIZE - 1) + "\r\n" + "bbbb"
        content, truncated = sanitize_content(raw)

        self.assertTrue(truncated)
        self.assertNotIn("\r", content)
        self.assertTrue(content.endswith("a\n"))


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
        self.assertLessEqual(len(result), MAX_TIMESTAMP_LENGTH)

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
