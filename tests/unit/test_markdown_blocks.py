"""Unit tests for Markdown blocks functionality."""

import unittest
from conv2md.markdown.blocks import (
    determine_fence_length,
    create_code_block,
    escape_markdown_content,
    format_speaker_line,
    create_date_marker,
)


class TestMarkdownBlocks(unittest.TestCase):
    """Test Markdown block handling functionality."""

    def test_determine_fence_length_no_backticks(self):
        """Test fence length determination with no backticks in content."""
        content = "def hello():\n    print('world')"
        result = determine_fence_length(content)
        self.assertEqual(result, 3)  # Default minimum

    def test_determine_fence_length_with_backticks(self):
        """Test fence length determination with backticks in content."""
        content = "Use `single backtick` in markdown"
        result = determine_fence_length(content)
        self.assertEqual(result, 3)  # Still minimum since only single backticks

    def test_determine_fence_length_with_triple_backticks(self):
        """Test fence length determination with triple backticks in content."""
        content = "```python\nprint('nested code')\n```"
        result = determine_fence_length(content)
        self.assertEqual(result, 4)  # One more than max sequence (3)

    def test_determine_fence_length_with_complex_backticks(self):
        """Test fence length with multiple backtick sequences."""
        content = "Use `` double and ``````` seven backticks"
        result = determine_fence_length(content)
        self.assertEqual(result, 8)  # One more than max sequence (7)

    def test_determine_fence_length_empty_content(self):
        """Test fence length with empty content."""
        result = determine_fence_length("")
        self.assertEqual(result, 3)

    def test_determine_fence_length_custom_minimum(self):
        """Test fence length with custom minimum."""
        content = "simple text"
        result = determine_fence_length(content, min_length=5)
        self.assertEqual(result, 5)

    def test_create_code_block_simple(self):
        """Test creating a simple code block."""
        content = "print('hello')"
        result = create_code_block(content)
        expected = "```\nprint('hello')\n```"
        self.assertEqual(result, expected)

    def test_create_code_block_with_language(self):
        """Test creating a code block with language specification."""
        content = "print('hello')"
        result = create_code_block(content, language="python")
        expected = "```python\nprint('hello')\n```"
        self.assertEqual(result, expected)

    def test_create_code_block_with_nested_backticks(self):
        """Test creating a code block with nested backticks."""
        content = "```bash\necho 'test'\n```"
        result = create_code_block(content, language="markdown")
        # Should use 4 backticks since content has 3
        expected = "````markdown\n```bash\necho 'test'\n```\n````"
        self.assertEqual(result, expected)

    def test_create_code_block_adds_trailing_newline(self):
        """Test that code block adds trailing newline if missing."""
        content = "no trailing newline"
        result = create_code_block(content)
        self.assertTrue(result.endswith("```"))
        self.assertIn("no trailing newline\n", result)

    def test_escape_markdown_content_basic(self):
        """Test basic markdown escaping."""
        text = "Hello *world* with _emphasis_"
        result = escape_markdown_content(text)
        expected = "Hello \\*world\\* with \\_emphasis\\_"
        self.assertEqual(result, expected)

    def test_escape_markdown_content_all_special_chars(self):
        """Test escaping all markdown special characters."""
        text = "\\`*_{}[]()#+-.!|"
        result = escape_markdown_content(text)
        expected = "\\\\\\`\\*\\_\\{\\}\\[\\]\\(\\)\\#\\+\\-\\.\\!\\|"
        self.assertEqual(result, expected)

    def test_format_speaker_line_simple(self):
        """Test formatting speaker line without timestamp."""
        speaker = "Alice"
        result = format_speaker_line(speaker)
        expected = "**Alice:**"
        self.assertEqual(result, expected)

    def test_format_speaker_line_with_timestamp(self):
        """Test formatting speaker line with timestamp."""
        speaker = "Bob"
        timestamp = "12:34"
        result = format_speaker_line(speaker, timestamp)
        expected = "**Bob — 12:34**"
        self.assertEqual(result, expected)

    def test_format_speaker_line_escapes_special_chars(self):
        """Test that speaker line escapes markdown special characters."""
        speaker = "User*Bold*"
        timestamp = "2024_01_01"
        result = format_speaker_line(speaker, timestamp)
        expected = "**User\\*Bold\\* — 2024\\_01\\_01**"
        self.assertEqual(result, expected)

    def test_create_date_marker(self):
        """Test creating date marker heading."""
        date_str = "2024-01-01"
        result = create_date_marker(date_str)
        expected = "## 2024-01-01"
        self.assertEqual(result, expected)

    def test_create_date_marker_escapes_special_chars(self):
        """Test date marker escapes special characters."""
        date_str = "2024*01*01"
        result = create_date_marker(date_str)
        expected = "## 2024\\*01\\*01"
        self.assertEqual(result, expected)


class TestDeterministicOutput(unittest.TestCase):
    """Test deterministic output across multiple runs."""

    def test_code_block_deterministic(self):
        """Test that code blocks produce identical output across runs."""
        content = "```python\ndef test():\n    pass\n```"

        # Run multiple times
        results = []
        for _ in range(5):
            result = create_code_block(content, "markdown")
            results.append(result)

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result, first_result)

    def test_speaker_formatting_deterministic(self):
        """Test that speaker formatting is deterministic."""
        speaker = "Test User"
        timestamp = "2024-01-01T12:00:00Z"

        # Run multiple times
        results = []
        for _ in range(5):
            result = format_speaker_line(speaker, timestamp)
            results.append(result)

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result, first_result)

    def test_content_escaping_deterministic(self):
        """Test that content escaping is deterministic."""
        content = "Test with *special* `chars` and [links](url)!"

        # Run multiple times
        results = []
        for _ in range(5):
            result = escape_markdown_content(content)
            results.append(result)

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result, first_result)


if __name__ == "__main__":
    unittest.main()
