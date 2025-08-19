"""Unit tests for markdown security controls."""

import unittest
from conv2md.markdown.security import validate_timestamp


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
            "25:00:00",   # Invalid time
            "random text",
            "javascript:alert(1)",  # Security test
            "<script>alert(1)</script>",  # XSS attempt
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
        self.assertTrue(len(result) <= 50)  # MAX_TIMESTAMP_LENGTH
        
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