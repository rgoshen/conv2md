"""Unit tests for Markdown generator."""

import unittest

from conv2md.domain.models import Conversation, Message, ContentType
from conv2md.markdown.generator import MarkdownGenerator
from conv2md.markdown.exceptions import InvalidContentError, ContentTooLargeError


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
            "description: Contains &quot;quotes&quot; and newlines\\nSecond line",
            result,
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
        # Content is now on separate line due to pipeline processing
        lines = result.split("\n")
        user_line_index = next(
            i for i, line in enumerate(lines) if line.startswith("**User:**")
        )
        content_line = (
            lines[user_line_index + 1] if user_line_index + 1 < len(lines) else ""
        )
        self.assertEqual(content_line, "")

    def test_generate_handles_single_message(self):
        """Test generation with only one message."""
        messages = [Message(speaker="Bot", content="Solo message")]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Should have proper structure with speaker and content on separate lines
        expected = "**Bot:**\nSolo message"
        self.assertEqual(result, expected)

    def test_generate_with_timestamps(self):
        """Test generation with timestamp support."""
        messages = [
            Message(speaker="User", content="Hello", timestamp="12:34"),
            Message(speaker="Bot", content="Hi there!", timestamp="12:35"),
        ]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Verify timestamp formatting
        self.assertIn("**User — 12:34**", result)
        self.assertIn("**Bot — 12:35**", result)

    def test_generate_with_code_content(self):
        """Test generation with code content type."""
        messages = [
            Message(
                speaker="Dev",
                content="def hello():\n    print('world')",
                content_type=ContentType.CODE,
                language="python",
            )
        ]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Verify code block formatting
        self.assertIn("**Dev:**", result)
        self.assertIn("```python", result)
        self.assertIn("def hello():", result)
        self.assertIn("```", result)

    def test_generate_with_image_content(self):
        """Test generation with image content type."""
        messages = [
            Message(
                speaker="User", content="screenshot.png", content_type=ContentType.IMAGE
            )
        ]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Verify image formatting
        self.assertIn("**User:**", result)
        self.assertIn("![Image](screenshot\\.png)", result)

    def test_generate_with_image_content_special_characters(self):
        """Test generation with image content containing special markdown characters."""
        messages = [
            Message(
                speaker="User", 
                content="my_image[1].png*special*.jpg", 
                content_type=ContentType.IMAGE
            )
        ]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Verify image formatting with escaped special characters
        self.assertIn("**User:**", result)
        self.assertIn("![Image](my\\_image\\[1\\]\\.png\\*special\\*\\.jpg)", result)

    def test_generate_with_nested_backticks_in_code(self):
        """Test generation with nested backticks in code blocks."""
        messages = [
            Message(
                speaker="Dev",
                content="```bash\necho 'test'\n```",
                content_type=ContentType.CODE,
                language="markdown",
            )
        ]
        conversation = Conversation(messages=messages)

        result = self.generator.generate(conversation)

        # Should use 4 backticks to fence the content with 3 backticks
        self.assertIn("````markdown", result)
        self.assertIn("````", result.split("````markdown")[1])

    def test_validation_empty_conversation(self):
        """Test validation with empty conversation."""
        conversation = Conversation(messages=[])

        with self.assertRaises(InvalidContentError) as cm:
            self.generator.generate(conversation)

        self.assertIn("at least one message", str(cm.exception))

    def test_validation_none_conversation(self):
        """Test validation with None conversation."""
        with self.assertRaises(InvalidContentError) as cm:
            self.generator.generate(None)

        self.assertIn("cannot be None", str(cm.exception))

    def test_validation_missing_speaker(self):
        """Test validation with missing speaker."""
        messages = [Message(speaker="", content="test")]
        conversation = Conversation(messages=messages)

        with self.assertRaises(InvalidContentError) as cm:
            self.generator.generate(conversation)

        self.assertIn("missing speaker", str(cm.exception))

    def test_validation_none_content(self):
        """Test validation with None content."""
        messages = [Message(speaker="User", content=None)]
        conversation = Conversation(messages=messages)

        with self.assertRaises(InvalidContentError) as cm:
            self.generator.generate(conversation)

        self.assertIn("None content", str(cm.exception))

    def test_validation_content_too_large(self):
        """Test validation with content exceeding size limits."""
        # Create a message with content larger than the limit
        # Use 11MB of content that should still be 11MB after sanitization
        large_content = "a" * (11 * 1024 * 1024)  # 11MB > 10MB limit, simple chars
        messages = [Message(speaker="User", content=large_content)]
        conversation = Conversation(messages=messages)

        with self.assertRaises(ContentTooLargeError) as cm:
            self.generator.generate(conversation)

        self.assertIn("exceeds size limit", str(cm.exception))

    def test_validation_total_conversation_size_exceeds_limit(self):
        """Test validation when total conversation size exceeds limit with multiple messages."""
        # Import constants and patch for testing
        from unittest.mock import patch
        from conv2md.markdown.constants import MAX_TOTAL_CONVERSATION_SIZE
        
        # Create a generator and patch the constant for testing
        generator = MarkdownGenerator()
        
        with patch('conv2md.markdown.generator.MAX_TOTAL_CONVERSATION_SIZE', 200000):  # 200KB limit
            # Create multiple messages that individually are under the individual limit
            # but together exceed the total limit after sanitization
            # Each message will be sanitized to 100KB, so 3 messages = 300KB > 200KB limit
            messages = []
            for i in range(3):
                # Create content larger than sanitization limit (will be truncated to 100KB)
                content = "x" * 150000  # 150KB content -> sanitized to 100KB each
                messages.append(Message(speaker=f"User{i}", content=content))
            
            conversation = Conversation(messages=messages)

            with self.assertRaises(ContentTooLargeError) as cm:
                generator.generate(conversation)
            
            self.assertIn("Total conversation size exceeds limit", str(cm.exception))

    def test_metrics_collection(self):
        """Test that metrics are collected during generation."""
        messages = [
            Message(speaker="User", content="Hello", content_type=ContentType.TEXT),
            Message(
                speaker="Dev", content="print('hi')", content_type=ContentType.CODE
            ),
            Message(
                speaker="User", content="image.png", content_type=ContentType.IMAGE
            ),
        ]
        conversation = Conversation(messages=messages)

        # Generate markdown
        result = self.generator.generate(conversation)

        # Verify metrics were collected
        metrics = self.generator.metrics_collector.current_metrics
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.message_count, 3)
        self.assertEqual(metrics.text_messages_processed, 1)
        self.assertEqual(metrics.code_blocks_processed, 1)
        self.assertEqual(metrics.images_processed, 1)
        self.assertGreater(metrics.total_content_size, 0)
        self.assertGreater(metrics.output_size, 0)

    def test_deterministic_output_multiple_runs(self):
        """Test that the same input produces identical output across multiple runs."""
        messages = [
            Message(speaker="User", content="Hello *world*!", timestamp="12:34"),
            Message(
                speaker="Bot",
                content="def test():\n    pass",
                content_type=ContentType.CODE,
                language="python",
            ),
            Message(
                speaker="User", content="image.jpg", content_type=ContentType.IMAGE
            ),
        ]
        conversation = Conversation(messages=messages)
        metadata = {"title": "Test Conversation", "source": "test"}

        # Generate markdown multiple times
        results = []
        for _ in range(5):
            result = self.generator.generate(conversation, metadata)
            results.append(result)

        # All results should be identical
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            self.assertEqual(result, first_result, f"Run {i+1} differs from run 1")

    def test_enhanced_yaml_frontmatter_sanitization(self):
        """Test enhanced YAML frontmatter with security sanitization."""
        messages = [Message(speaker="User", content="Test")]
        conversation = Conversation(messages=messages)

        # Metadata with potentially dangerous content
        metadata = {
            "title": "Test: Content with: colons",
            "malicious": "- list\n  injection: attempt",
            "quotes": 'Contains "quotes" and newlines\nSecond line',
            "script": "<script>alert('xss')</script>",
            "invalid_key_#$%": "should be sanitized",
        }

        result = self.generator.generate(conversation, metadata=metadata)

        # Verify sanitization occurred
        self.assertIn("title: Test\\: Content with\\: colons", result)
        self.assertIn("malicious: \\- list\\n  injection\\: attempt", result)
        self.assertIn("quotes: Contains &quot;quotes&quot;", result)
        self.assertIn(
            "script: &lt;script&gt;alert(&\\#x27;xss&\\#x27;)&lt;/script&gt;", result
        )
        # Invalid key should be sanitized and included
        self.assertIn("invalid_key_", result)

    def test_specific_exception_handling_in_message_processing(self):
        """Test that only specific exceptions are caught during message processing."""
        from unittest.mock import Mock
        
        # Test that ValueError (a processing error) is caught and converted
        mock_pipeline = Mock()
        mock_pipeline.process_message.side_effect = ValueError("Mock processing error")
        
        generator = MarkdownGenerator(pipeline=mock_pipeline)
        messages = [Message(speaker="User", content="Test")]
        conversation = Conversation(messages=messages)
        
        # Should catch ValueError and convert to InvalidContentError
        with self.assertRaises(InvalidContentError) as cm:
            generator.generate(conversation)
        
        self.assertIn("Failed to process message 1", str(cm.exception))
        self.assertIn("Mock processing error", str(cm.exception))

    def test_unexpected_exceptions_are_not_masked(self):
        """Test that unexpected exceptions like RuntimeError are not caught."""
        from unittest.mock import Mock
        
        # Create a mock pipeline that raises an unexpected exception
        mock_pipeline = Mock()
        mock_pipeline.process_message.side_effect = RuntimeError("Unexpected error")
        
        generator = MarkdownGenerator(pipeline=mock_pipeline)
        messages = [Message(speaker="User", content="Test")]
        conversation = Conversation(messages=messages)
        
        # RuntimeError should NOT be caught - it should bubble up
        with self.assertRaises(RuntimeError) as cm:
            generator.generate(conversation)
        
        self.assertIn("Unexpected error", str(cm.exception))

    def test_build_frontmatter_helper_method(self):
        """Test _build_frontmatter helper method directly."""
        generator = MarkdownGenerator()
        metadata = {"title": "Test Title", "source": "test.json"}
        
        result = generator._build_frontmatter(metadata)
        
        # Should have opening delimiter, content, closing delimiter, and blank line
        self.assertEqual(result[0], "---")
        self.assertIn("title: Test Title", result)
        self.assertIn("source: test.json", result)
        self.assertEqual(result[-2], "---")
        self.assertEqual(result[-1], "")  # Blank line after frontmatter

    def test_build_message_lines_helper_method(self):
        """Test _build_message_lines helper method directly."""
        generator = MarkdownGenerator()
        messages = [
            Message(speaker="User", content="Hello"),
            Message(speaker="Bot", content="Hi there!")
        ]
        
        result = generator._build_message_lines(messages)
        
        # Should have speaker lines, content lines, and blank lines
        self.assertIn("**User:**", result)
        self.assertIn("Hello", result)
        self.assertIn("**Bot:**", result)
        self.assertIn("Hi there\\!", result)  # Exclamation escaped
        # Should have blank lines between messages
        self.assertIn("", result)

    def test_frontmatter_keys_are_sorted_deterministically(self):
        """Test that metadata keys in frontmatter are sorted for deterministic output."""
        generator = MarkdownGenerator()
        # Create metadata with keys in non-alphabetical order
        metadata = {
            "zzz_last": "last value",
            "aaa_first": "first value", 
            "mmm_middle": "middle value",
            "title": "Test Title"
        }
        
        result = generator._build_frontmatter(metadata)
        
        # Find the frontmatter content (between the --- delimiters)
        content_lines = []
        in_frontmatter = False
        for line in result:
            if line == "---":
                if in_frontmatter:
                    break  # End of frontmatter
                else:
                    in_frontmatter = True  # Start of frontmatter
            elif in_frontmatter:
                content_lines.append(line)
        
        # Keys should be in alphabetical order
        expected_order = [
            "aaa_first: first value",
            "mmm_middle: middle value", 
            "title: Test Title",
            "zzz_last: last value"
        ]
        
        self.assertEqual(content_lines, expected_order)


if __name__ == "__main__":
    unittest.main()
