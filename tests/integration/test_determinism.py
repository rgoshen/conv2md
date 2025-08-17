"""Integration tests for deterministic output."""

import unittest
from pathlib import Path

from conv2md.converters.json_conv import JSONConverter
from conv2md.markdown.generator import MarkdownGenerator


class TestDeterministicOutput(unittest.TestCase):
    """Test that identical inputs produce identical outputs."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = JSONConverter()
        self.generator = MarkdownGenerator()
        self.fixtures_dir = Path(__file__).parent.parent / "fixtures"

    def test_json_to_markdown_deterministic(self):
        """Test that JSON to Markdown conversion is deterministic."""
        # Load test fixture
        fixture_path = self.fixtures_dir / "conversations" / "simple_conversation.json"

        with open(fixture_path, "r") as f:
            json_content = f.read()

        # Convert multiple times
        results = []
        for _ in range(3):
            conversation = self.converter.parse(json_content)
            markdown = self.generator.generate(conversation)
            results.append(markdown)

        # All results should be identical
        self.assertEqual(
            results[0], results[1], "First and second conversion should be identical"
        )
        self.assertEqual(
            results[1], results[2], "Second and third conversion should be identical"
        )
        self.assertEqual(
            results[0], results[2], "First and third conversion should be identical"
        )

    def test_markdown_generation_with_metadata_deterministic(self):
        """Test that Markdown generation with metadata is deterministic."""
        fixture_path = self.fixtures_dir / "conversations" / "simple_conversation.json"

        with open(fixture_path, "r") as f:
            json_content = f.read()

        conversation = self.converter.parse(json_content)
        metadata = {"title": "Test", "source": "fixture", "created": "2025-01-01"}

        # Generate multiple times with same metadata
        results = []
        for _ in range(3):
            markdown = self.generator.generate(conversation, metadata=metadata)
            results.append(markdown)

        # All results should be identical
        self.assertEqual(
            len(set(results)), 1, "All Markdown outputs should be identical"
        )

    def test_golden_fixture_output_matches_expected(self):
        """Test that output matches pre-generated golden fixture."""
        fixture_path = self.fixtures_dir / "conversations" / "simple_conversation.json"
        expected_path = self.fixtures_dir / "expected" / "simple_conversation.md"

        # Generate current output
        with open(fixture_path, "r") as f:
            json_content = f.read()

        conversation = self.converter.parse(json_content)
        current_output = self.generator.generate(conversation)

        # Create expected output if it doesn't exist (first run)
        if not expected_path.exists():
            expected_path.parent.mkdir(parents=True, exist_ok=True)
            with open(expected_path, "w") as f:
                f.write(current_output)
            self.skipTest("Created golden fixture - run test again to validate")

        # Compare with expected output
        with open(expected_path, "r") as f:
            expected_output = f.read()

        self.assertEqual(
            current_output,
            expected_output,
            "Current output should match golden fixture",
        )


if __name__ == "__main__":
    unittest.main()
