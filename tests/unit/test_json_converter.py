"""Unit tests for JSON conversation converter."""

import unittest
import json
import logging
from io import StringIO

from conv2md.converters.json_conv import JSONConverter, ConversationParseError


class TestJSONConverter(unittest.TestCase):
    """Test JSON conversation parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = JSONConverter()

        # Set up logging capture for testing
        self.log_stream = StringIO()
        self.log_handler = logging.StreamHandler(self.log_stream)
        self.log_handler.setLevel(logging.DEBUG)

        logger = logging.getLogger("conv2md.converters.json_conv")
        logger.addHandler(self.log_handler)
        logger.setLevel(logging.DEBUG)

    def tearDown(self):
        """Clean up test fixtures."""
        logger = logging.getLogger("conv2md.converters.json_conv")
        logger.removeHandler(self.log_handler)

    def test_parse_minimal_conversation_schema(self):
        """Test parsing minimal JSON conversation with required fields."""
        # Minimal valid JSON conversation
        minimal_json = {
            "messages": [
                {"speaker": "User", "content": "Hello"},
                {"speaker": "Assistant", "content": "Hi there!"},
            ]
        }

        # Convert to JSON string for parsing
        json_string = json.dumps(minimal_json)

        # This should parse successfully and return structured data
        result = self.converter.parse(json_string)

        # Verify result structure
        self.assertIsNotNone(result)
        self.assertEqual(len(result.messages), 2)
        self.assertEqual(result.messages[0].speaker, "User")
        self.assertEqual(result.messages[0].content, "Hello")
        self.assertEqual(result.messages[1].speaker, "Assistant")
        self.assertEqual(result.messages[1].content, "Hi there!")

    def test_parse_malformed_json_raises_error(self):
        """Test that malformed JSON raises appropriate error."""
        malformed_json = (
            '{"messages": [{"speaker": "User", "content": "Hello"'  # Missing braces
        )

        with self.assertRaises(json.JSONDecodeError):
            self.converter.parse(malformed_json)

    def test_parse_missing_messages_field_raises_error(self):
        """Test that JSON without 'messages' field raises error."""
        invalid_json = json.dumps({"conversations": []})  # Wrong field name

        with self.assertRaises(KeyError):
            self.converter.parse(invalid_json)

    def test_parse_missing_message_fields_raises_error(self):
        """Test that messages missing required fields raise errors."""
        # Missing 'content' field
        incomplete_json = json.dumps(
            {"messages": [{"speaker": "User"}]}  # Missing content
        )

        with self.assertRaises(KeyError):
            self.converter.parse(incomplete_json)

    def test_parse_empty_messages_raises_error(self):
        """Test that empty messages list raises validation error."""
        empty_json = json.dumps({"messages": []})

        with self.assertRaises(ConversationParseError) as cm:
            self.converter.parse(empty_json)

        self.assertIn("empty", str(cm.exception).lower())

    def test_parse_invalid_message_content_raises_error(self):
        """Test that invalid message content raises validation error."""
        # Non-string content
        invalid_json = json.dumps(
            {
                "messages": [
                    {"speaker": "User", "content": 123}
                ]  # Number instead of string
            }
        )

        with self.assertRaises(ConversationParseError) as cm:
            self.converter.parse(invalid_json)

        self.assertIn("content must be str", str(cm.exception).lower())

    def test_parse_invalid_message_speaker_raises_error(self):
        """Test that invalid message speaker raises validation error."""
        # Non-string speaker
        invalid_json = json.dumps(
            {
                "messages": [
                    {"speaker": 456, "content": "Hello"}  # Number instead of string
                ]
            }
        )

        with self.assertRaises(ConversationParseError) as cm:
            self.converter.parse(invalid_json)

        self.assertIn("speaker must be str", str(cm.exception).lower())

    def test_parse_empty_speaker_raises_error(self):
        """Test that empty speaker string raises validation error."""
        empty_speaker_json = json.dumps(
            {"messages": [{"speaker": "", "content": "Hello"}]}  # Empty speaker
        )

        with self.assertRaises(ConversationParseError) as cm:
            self.converter.parse(empty_speaker_json)

        self.assertIn("speaker cannot be empty", str(cm.exception).lower())

    def test_parse_whitespace_only_speaker_raises_error(self):
        """Test that whitespace-only speaker raises validation error."""
        whitespace_speaker_json = json.dumps(
            {"messages": [{"speaker": "   ", "content": "Hello"}]}  # Whitespace only
        )

        with self.assertRaises(ConversationParseError) as cm:
            self.converter.parse(whitespace_speaker_json)

        self.assertIn("speaker cannot be empty", str(cm.exception).lower())

    def test_parse_logs_conversion_steps(self):
        """Test that parsing logs conversion steps for observability."""
        minimal_json = {
            "messages": [
                {"speaker": "User", "content": "Hello"},
                {"speaker": "Assistant", "content": "Hi there!"},
            ]
        }
        json_string = json.dumps(minimal_json)

        # Parse conversation
        self.converter.parse(json_string)

        # Check logs were generated
        log_output = self.log_stream.getvalue()
        self.assertIn("Starting JSON conversation parsing", log_output)
        self.assertIn("Parsed 2 messages successfully", log_output)
        self.assertIn("JSON parsing completed", log_output)

    def test_parse_logs_validation_errors(self):
        """Test that validation errors are logged for debugging."""
        empty_json = json.dumps({"messages": []})

        with self.assertRaises(ConversationParseError):
            self.converter.parse(empty_json)

        # Check error was logged
        log_output = self.log_stream.getvalue()
        self.assertIn("Validation error", log_output)
        self.assertIn("empty", log_output.lower())


if __name__ == "__main__":
    unittest.main()
