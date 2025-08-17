"""Unit tests for CLI interface."""

import unittest
from click.testing import CliRunner

from conv2md.cli import main


class TestCLIArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_accepts_input_argument(self):
        """Test CLI accepts --input argument without error."""
        result = self.runner.invoke(main, ['--input', 'test.json'])
        
        # Should not exit with usage error (exit code 2)
        self.assertNotEqual(result.exit_code, 2, 
                           "CLI should accept --input argument")

    def test_cli_accepts_out_argument(self):
        """Test CLI accepts --out argument without error."""
        result = self.runner.invoke(main, [
            '--input', 'test.json',
            '--out', './output'
        ])
        
        # Should not exit with usage error (exit code 2)
        self.assertNotEqual(result.exit_code, 2,
                           "CLI should accept --out argument")

    def test_cli_requires_input_argument(self):
        """Test CLI requires --input argument."""
        result = self.runner.invoke(main, [])
        
        # Should exit with error when no input provided
        self.assertNotEqual(result.exit_code, 0,
                           "CLI should require --input argument")

    def test_cli_validates_input_file_exists(self):
        """Test CLI validates that input file exists."""
        result = self.runner.invoke(main, ['--input', 'nonexistent.json'])
        
        # Should exit with error for nonexistent file
        self.assertNotEqual(result.exit_code, 0,
                           "CLI should validate input file exists")
        self.assertIn('not found', result.output.lower())

    def test_cli_shows_help(self):
        """Test CLI shows comprehensive help information."""
        result = self.runner.invoke(main, ['--help'])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn('--input', result.output)
        self.assertIn('--out', result.output)
        self.assertIn('Convert conversations', result.output)

    def test_cli_prevents_path_traversal(self):
        """Test CLI prevents path traversal attacks."""
        result = self.runner.invoke(main, ['--input', '../../../etc/passwd'])
        
        # Should exit with security error for path traversal attempt
        self.assertNotEqual(result.exit_code, 0,
                           "CLI should prevent path traversal")
        self.assertIn('path', result.output.lower())


if __name__ == "__main__":
    unittest.main()