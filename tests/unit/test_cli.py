"""Unit tests for CLI interface."""

import unittest
import tempfile
import os
from click.testing import CliRunner

from conv2md.cli import main


class TestCLIArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        # Create a temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.temp_file.write('{"test": "data"}')
        self.temp_file.close()
        self.test_file_path = self.temp_file.name

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_file_path):
            os.unlink(self.test_file_path)

    def test_cli_accepts_input_argument(self):
        """Test CLI accepts --input argument without error."""
        result = self.runner.invoke(main, ["--input", self.test_file_path])

        # Should not exit with usage error (exit code 2)
        self.assertNotEqual(result.exit_code, 2, "CLI should accept --input argument")

    def test_cli_accepts_http_url_input(self):
        """Test CLI accepts a valid HTTP(S) URL as --input argument without file-related error."""
        url = "https://example.com/test.json"
        result = self.runner.invoke(main, ["--input", url])

        # Should not exit with usage error (exit code 2)
        self.assertNotEqual(
            result.exit_code, 2, "CLI should accept a valid HTTP(S) URL as input"
        )
        # Should not raise file-related errors for URLs
        self.assertNotIn("not found", result.output.lower())
        self.assertNotIn("no such file", result.output.lower())

    def test_cli_accepts_out_argument(self):
        """Test CLI accepts --out argument without error."""
        result = self.runner.invoke(
            main, ["--input", self.test_file_path, "--out", "./output"]
        )

        # Should not exit with usage error (exit code 2)
        self.assertNotEqual(result.exit_code, 2, "CLI should accept --out argument")

    def test_cli_requires_input_argument(self):
        """Test CLI requires --input argument."""
        result = self.runner.invoke(main, [])

        # Should exit with error when no input provided
        self.assertNotEqual(result.exit_code, 0, "CLI should require --input argument")

    def test_cli_validates_input_file_exists(self):
        """Test CLI validates that input file exists."""
        result = self.runner.invoke(main, ["--input", "nonexistent.json"])

        # Should exit with error for nonexistent file
        self.assertNotEqual(
            result.exit_code, 0, "CLI should validate input file exists"
        )
        self.assertIn("not found", result.output.lower())

    def test_cli_validates_input_is_file(self):
        """Test CLI validates that input path is a file, not a directory."""
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            # Pass the directory as --input
            result = self.runner.invoke(main, ["--input", temp_dir])
            self.assertNotEqual(
                result.exit_code, 0, "CLI should error if input is a directory"
            )
            # Check for directory-related error message
            self.assertTrue(
                any(
                    phrase in result.output.lower()
                    for phrase in ["not a file", "is a directory", "invalid"]
                ),
                f"Expected directory error message, got: {result.output}",
            )

    def test_cli_shows_help(self):
        """Test CLI shows comprehensive help information."""
        result = self.runner.invoke(main, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("--input", result.output)
        self.assertIn("--out", result.output)
        self.assertIn("Convert conversations", result.output)

    def test_cli_prevents_path_traversal(self):
        """Test CLI prevents path traversal attacks."""
        result = self.runner.invoke(main, ["--input", "../../../etc/passwd"])

        # Should exit with security error for path traversal attempt
        self.assertNotEqual(result.exit_code, 0, "CLI should prevent path traversal")
        # Click's validation will show "not found" for non-existent files
        self.assertIn("not found", result.output.lower())


if __name__ == "__main__":
    unittest.main()
