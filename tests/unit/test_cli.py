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


if __name__ == "__main__":
    unittest.main()