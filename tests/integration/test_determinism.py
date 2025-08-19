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

        # Convert multiple times and verify deterministic output
        results = []
        for i in range(3):
            with self.subTest(run=i + 1):
                conversation = self.converter.parse(json_content)
                markdown = self.generator.generate(conversation)

                # Compare with first result if we have previous results
                if results:
                    self.assertEqual(
                        markdown,
                        results[0],
                        f"Run {i + 1} should match first run output",
                    )
                results.append(markdown)

    def test_markdown_generation_with_metadata_deterministic(self):
        """Test that Markdown generation with metadata is deterministic."""
        fixture_path = self.fixtures_dir / "conversations" / "simple_conversation.json"

        with open(fixture_path, "r") as f:
            json_content = f.read()

        conversation = self.converter.parse(json_content)
        metadata = {"title": "Test", "source": "fixture", "created": "2025-01-01"}

        # Generate multiple times with same metadata and verify deterministic output
        results = []
        for i in range(3):
            with self.subTest(run=i + 1):
                markdown = self.generator.generate(conversation, metadata=metadata)

                # Compare with first result if we have previous results
                if results:
                    self.assertEqual(
                        markdown,
                        results[0],
                        f"Run {i + 1} should match first run output",
                    )
                results.append(markdown)

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
