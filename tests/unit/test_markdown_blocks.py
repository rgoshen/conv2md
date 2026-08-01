"""Unit tests for Markdown blocks functionality."""

import unittest
from conv2md.domain.models import ContentType, Message
from conv2md.markdown.blocks import (
    determine_fence_length,
    create_code_block,
    escape_markdown_content,
    format_speaker_line,
    create_date_marker,
)
from conv2md.markdown.pipeline import ImageContentProcessor, TextContentProcessor


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
        text = "\\`*_{}[]()#+-.!|=>"
        result = escape_markdown_content(text)
        expected = "\\\\\\`\\*\\_\\{\\}\\[\\]\\(\\)\\#\\+\\-\\.\\!\\|\\=\\>"
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


class TestCodeBlockLanguageValidation(unittest.TestCase):
    """Test that fence language tags cannot escape the code block."""

    def test_accepts_ordinary_language_tags(self):
        """Real-world language identifiers pass through unchanged."""
        languages = [
            "python",
            "c++",
            "objective-c",
            "f#",
            "C",
            "jsonl",
            "shell_session",
            "vim.script",
            "a" * 32,  # Longest accepted tag
        ]

        for language in languages:
            with self.subTest(language=language):
                result = create_code_block("code", language=language)
                self.assertEqual(result, f"```{language}\ncode\n```")

    def test_fence_closing_language_cannot_inject_markdown(self):
        """A language that closes its own fence must not escape the block."""
        malicious = "python\n```\n# FORGED HEADING\n\nnot code anymore"

        result = create_code_block("print('hi')", language=malicious)

        # The forged heading must never reach the output at all
        self.assertNotIn("FORGED HEADING", result)
        # Exactly one opening and one closing fence, and the opener is bare
        self.assertEqual(result.count("```"), 2)
        self.assertEqual(result.splitlines()[0], "```")
        self.assertEqual(result, "```\nprint('hi')\n```")

    def test_rejects_invalid_language_tags(self):
        """Tags outside the identifier charset fall back to an empty tag."""
        cases = [
            ("newline", "python\nnot-code"),
            ("carriage return", "python\r```"),
            ("fence characters", "```python"),
            ("space", "python script"),
            ("tab", "python\tscript"),
            ("html", "<script>alert(1)</script>"),
            ("path traversal", "../../etc/passwd"),
            ("too long", "a" * 33),
            ("empty string", ""),
            ("whitespace only", "   "),
        ]

        for description, language in cases:
            with self.subTest(case=description):
                result = create_code_block("code", language=language)
                self.assertEqual(result, "```\ncode\n```")

    def test_none_language_produces_bare_fence(self):
        """Omitting the language keeps the existing bare-fence behaviour."""
        self.assertEqual(create_code_block("code"), "```\ncode\n```")
        self.assertEqual(create_code_block("code", language=None), "```\ncode\n```")

    def test_language_validation_respects_extended_fences(self):
        """Fence extension and language validation compose correctly."""
        content = "```bash\necho 'test'\n```"

        result = create_code_block(content, language="markdown\n```\n# FORGED")

        self.assertEqual(result, f"````\n{content}\n````")
        self.assertNotIn("FORGED", result)


class TestBlockOpenerEscaping(unittest.TestCase):
    """Test that content cannot spell a block-level Markdown opener."""

    def test_block_openers_are_escaped(self):
        """Setext underlines and blockquote markers survive as literal text."""
        cases = [
            ("setext h1 underline", "===", "\\=\\=\\="),
            ("setext h2 underline", "---", "\\-\\-\\-"),
            ("blockquote", "> text", "\\> text"),
            ("nested blockquote", ">> text", "\\>\\> text"),
            ("lazy setext heading", "Title\n===", "Title\n\\=\\=\\="),
            ("prose equals", "x = 1", "x \\= 1"),
            ("prose greater than", "a > b", "a \\> b"),
        ]

        for description, content, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(escape_markdown_content(content), expected)

    def test_speaker_line_escapes_block_openers(self):
        """format_speaker_line inherits the widened escape set."""
        result = format_speaker_line("> Bot", "12:00 => 13:00")
        self.assertEqual(result, "**\\> Bot — 12:00 \\=\\> 13:00**")

    def test_text_processor_escapes_block_openers(self):
        """TextContentProcessor inherits the widened escape set."""
        message = Message(speaker="User", content="> quoted\n===")
        result = TextContentProcessor().process(message)
        self.assertEqual(result, "\\> quoted\n\\=\\=\\=")

    def test_image_processor_escapes_block_openers(self):
        """ImageContentProcessor inherits the widened escape set."""
        message = Message(
            speaker="User",
            content="a=b>c.png",
            content_type=ContentType.IMAGE,
        )
        result = ImageContentProcessor().process(message)
        self.assertEqual(result, "![Image](a\\=b\\>c\\.png)")


class TestDateMarkerHardening(unittest.TestCase):
    """Test that create_date_marker confines input to the heading."""

    def test_line_breaks_cannot_escape_the_heading(self):
        """Every Unicode line break collapses to a space, keeping one line."""
        cases = [
            ("newline", "2024-01-01\n# Forged", "## 2024-01-01 \\# Forged"),
            ("carriage return", "2024-01-01\r# Forged", "## 2024-01-01 \\# Forged"),
            ("crlf", "2024-01-01\r\n# Forged", "## 2024-01-01 \\# Forged"),
            ("blank line", "2024-01-01\n\ntext", "## 2024-01-01 text"),
            ("line separator", "2024-01-01\u2028text", "## 2024-01-01 text"),
            ("paragraph separator", "2024-01-01\u2029text", "## 2024-01-01 text"),
            ("vertical tab", "2024-01-01\vtext", "## 2024-01-01 text"),
            ("form feed", "2024-01-01\ftext", "## 2024-01-01 text"),
            ("next line", "2024-01-01\x85text", "## 2024-01-01 text"),
        ]

        for description, date_str, expected in cases:
            with self.subTest(case=description):
                result = create_date_marker(date_str)
                self.assertEqual(result, expected)
                self.assertEqual(len(result.splitlines()), 1)

    def test_code_fence_injection_stays_inside_the_heading(self):
        """A fenced block smuggled through a newline cannot open a block."""
        result = create_date_marker("2024-01-01\n\n```\nrm -rf /\n```")

        self.assertEqual(len(result.splitlines()), 1)
        self.assertTrue(result.startswith("## "))
        self.assertEqual(result, "## 2024-01-01 ``` rm -rf / ```")

    def test_backslashes_cannot_defeat_the_escapes(self):
        """A caller backslash is escaped first so it cannot re-arm markup."""
        cases = [
            ("bare backslash", "2024\\01", "## 2024\\\\01"),
            ("trailing backslash", "2024-01-01\\", "## 2024-01-01\\\\"),
            ("backslash before star", "a\\*b*c", "## a\\\\\\*b\\*c"),
            ("backslash before hash", "\\#Forged", "## \\\\\\#Forged"),
            ("double backslash", "a\\\\b", "## a\\\\\\\\b"),
        ]

        for description, date_str, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(create_date_marker(date_str), expected)

    def test_non_date_input_renders_as_heading_text(self):
        """Arbitrary values still render, but only ever as heading text."""
        cases = [
            ("empty", "", "## "),
            ("whitespace only", "   \n\t ", "## "),
            ("surrounding whitespace", "  2024-01-01  ", "## 2024-01-01"),
            ("not a date", "tomorrow", "## tomorrow"),
            ("heading marker", "###### deep", "## \\#\\#\\#\\#\\#\\# deep"),
            ("emphasis", "2024*01*01", "## 2024\\*01\\*01"),
            ("underscores", "2024_01_01", "## 2024\\_01\\_01"),
            ("path traversal", "../../etc/passwd", "## ../../etc/passwd"),
        ]

        for description, date_str, expected in cases:
            with self.subTest(case=description):
                self.assertEqual(create_date_marker(date_str), expected)

    def test_date_marker_is_deterministic(self):
        """Repeated calls on hostile input produce identical output."""
        date_str = "2024-01-01\n\n# Forged\\*"
        results = {create_date_marker(date_str) for _ in range(5)}
        self.assertEqual(len(results), 1)


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
