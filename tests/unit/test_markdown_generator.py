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
        self.assertIn("Hi there!", result)

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

        # Find closing frontmatter
        closing_index = None
        for i, line in enumerate(lines[1:], 1):
            if line == "---":
                closing_index = i
                break

        self.assertIsNotNone(closing_index, "Should have closing --- for frontmatter")
        self.assertIn("**User:**", result)


if __name__ == "__main__":
    unittest.main()
