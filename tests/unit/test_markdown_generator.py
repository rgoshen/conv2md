"""Unit tests for Markdown generator."""

import unittest

from conv2md.domain.models import Conversation, Message
from conv2md.markdown.generator import MarkdownGenerator


class TestMarkdownGenerator(unittest.TestCase):
    """Test Markdown generation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = MarkdownGenerator()

    def test_generate_minimal_conversation_markdown(self):
        """Test generating Markdown from minimal conversation."""
        # Create test conversation
        messages = [
            Message(speaker="User", content="Hello"),
            Message(speaker="Assistant", content="Hi there!"),
        ]
        conversation = Conversation(messages=messages)

        # Generate Markdown
        result = self.generator.generate(conversation)

        # Verify result structure
        self.assertIsInstance(result, str)
        self.assertIn("User", result)
        self.assertIn("Hello", result)
        self.assertIn("Assistant", result)
        self.assertIn("Hi there\\!", result)  # Exclamation is escaped

        # Verify proper Markdown formatting
        lines = result.strip().split("\n")
        self.assertTrue(any(line.startswith("**User:**") for line in lines))
        self.assertTrue(any(line.startswith("**Assistant:**") for line in lines))

    def test_generate_with_metadata_frontmatter(self):
        """Test generating Markdown with YAML frontmatter metadata."""
        # Create test conversation
        messages = [Message(speaker="User", content="Test message")]
        conversation = Conversation(messages=messages)

        # Generate with metadata
        metadata = {"title": "Test Conversation", "source": "test.json"}
        result = self.generator.generate(conversation, metadata=metadata)

        # Verify YAML frontmatter structure
        lines = result.split("\n")
        self.assertEqual(lines[0], "---")
        self.assertIn("title: Test Conversation", result)
        self.assertIn("source: test.json", result)

        # Verify closing frontmatter exists
        self.assertIn("---", lines[1:], "Should have closing --- for frontmatter")
        self.assertIn("**User:**", result)

    def test_generate_escapes_markdown_characters(self):
        """Test that Markdown special characters are escaped in output."""
        # Create conversation with Markdown special characters
        messages = [
            Message(speaker="User*Bold*", content="Hello _italic_ and `code`!"),
            Message(speaker="Bot[link]", content="Text with # heading and **bold**"),
        ]
        conversation = Conversation(messages=messages)

        # Generate Markdown
        result = self.generator.generate(conversation)

        # Verify special characters are escaped
        self.assertIn("User\\*Bold\\*", result)
        self.assertIn("Hello \\_italic\\_ and \\`code\\`\\!", result)
        self.assertIn("Bot\\[link\\]", result)
        self.assertIn("Text with \\# heading and \\*\\*bold\\*\\*", result)

    def test_generate_escapes_yaml_frontmatter_injection(self):
        """Test that YAML special characters in metadata are escaped."""
        # Create conversation with metadata containing YAML special characters
        messages = [Message(speaker="User", content="Test")]
        conversation = Conversation(messages=messages)

        # Metadata with YAML injection attempts
        metadata = {
            "title": "Test: malicious content",
            "description": 'Contains "quotes" and newlines\nSecond line',
            "tags": "value with: colon",
            "injection": "- list item\n  nested: value",
        }

        result = self.generator.generate(conversation, metadata=metadata)

        # Verify YAML special characters are handled safely
        self.assertIn("title: Test\\: malicious content", result)
        self.assertIn(
            'description: Contains \\"quotes\\" and newlines\\nSecond line', result
        )
        self.assertIn("tags: value with\\: colon", result)
        self.assertIn("injection: \\- list item\\n  nested\\: value", result)

    def test_generate_handles_empty_content(self):
        """Test that empty content is handled properly."""
        # Create conversation with empty content
        messages = [Message(speaker="User", content="")]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Should still format properly with empty content
        self.assertIn("**User:**", result)
        # Content after colon should be empty (just the space)
        lines = result.split("\n")
        user_line = next(line for line in lines if line.startswith("**User:**"))
        self.assertEqual(user_line, "**User:** ")

    def test_generate_handles_single_message(self):
        """Test generation with only one message."""
        messages = [Message(speaker="Bot", content="Solo message")]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Should have no trailing newlines for single message
        self.assertEqual(result, "**Bot:** Solo message")
        self.assertNotIn("\n\n", result)


if __name__ == "__main__":
    unittest.main()
