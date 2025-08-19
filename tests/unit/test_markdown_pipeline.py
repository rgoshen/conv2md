"""Unit tests for Markdown content processing pipeline."""

import unittest
from conv2md.domain.models import Message, ContentType
from conv2md.markdown.pipeline import (
    ContentProcessingPipeline,
    TextContentProcessor,
    CodeContentProcessor,
    ImageContentProcessor,
    ContentProcessor,
)


class MockContentProcessor(ContentProcessor):
    """Mock processor for testing."""

    def __init__(self, content_type: ContentType, result: str):
        self.content_type = content_type
        self.result = result

    def can_process(self, content_type: ContentType) -> bool:
        return content_type == self.content_type

    def process(self, message: Message) -> str:
        return self.result


class TestContentProcessors(unittest.TestCase):
    """Test individual content processors."""

    def test_text_processor_can_process(self):
        """Test text processor content type detection."""
        processor = TextContentProcessor()
        self.assertTrue(processor.can_process(ContentType.TEXT))
        self.assertFalse(processor.can_process(ContentType.CODE))
        self.assertFalse(processor.can_process(ContentType.IMAGE))

    def test_text_processor_process(self):
        """Test text processor content processing."""
        processor = TextContentProcessor()
        message = Message(
            speaker="User",
            content="Hello *world* with _emphasis_",
            content_type=ContentType.TEXT,
        )
        result = processor.process(message)
        expected = "Hello \\*world\\* with \\_emphasis\\_"
        self.assertEqual(result, expected)

    def test_code_processor_can_process(self):
        """Test code processor content type detection."""
        processor = CodeContentProcessor()
        self.assertFalse(processor.can_process(ContentType.TEXT))
        self.assertTrue(processor.can_process(ContentType.CODE))
        self.assertFalse(processor.can_process(ContentType.IMAGE))

    def test_code_processor_process(self):
        """Test code processor content processing."""
        processor = CodeContentProcessor()
        message = Message(
            speaker="User",
            content="print('hello')",
            content_type=ContentType.CODE,
            language="python",
        )
        result = processor.process(message)
        expected = "```python\nprint('hello')\n```"
        self.assertEqual(result, expected)

    def test_code_processor_process_no_language(self):
        """Test code processor without language specification."""
        processor = CodeContentProcessor()
        message = Message(
            speaker="User", content="echo 'test'", content_type=ContentType.CODE
        )
        result = processor.process(message)
        expected = "```\necho 'test'\n```"
        self.assertEqual(result, expected)

    def test_image_processor_can_process(self):
        """Test image processor content type detection."""
        processor = ImageContentProcessor()
        self.assertFalse(processor.can_process(ContentType.TEXT))
        self.assertFalse(processor.can_process(ContentType.CODE))
        self.assertTrue(processor.can_process(ContentType.IMAGE))

    def test_image_processor_process(self):
        """Test image processor content processing."""
        processor = ImageContentProcessor()
        message = Message(
            speaker="User", content="path/to/image.jpg", content_type=ContentType.IMAGE
        )
        result = processor.process(message)
        expected = "![Image](path/to/image\\.jpg)"
        self.assertEqual(result, expected)


class TestContentProcessingPipeline(unittest.TestCase):
    """Test content processing pipeline."""

    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = ContentProcessingPipeline()

    def test_pipeline_process_text_message(self):
        """Test pipeline processing text message."""
        message = Message(
            speaker="User", content="Hello world!", content_type=ContentType.TEXT
        )
        result = self.pipeline.process_message(message)
        expected = "Hello world\\!"
        self.assertEqual(result, expected)

    def test_pipeline_process_code_message(self):
        """Test pipeline processing code message."""
        message = Message(
            speaker="Dev",
            content="def hello():\n    print('hi')",
            content_type=ContentType.CODE,
            language="python",
        )
        result = self.pipeline.process_message(message)
        expected = "```python\ndef hello():\n    print('hi')\n```"
        self.assertEqual(result, expected)

    def test_pipeline_process_image_message(self):
        """Test pipeline processing image message."""
        message = Message(
            speaker="User", content="screenshot.png", content_type=ContentType.IMAGE
        )
        result = self.pipeline.process_message(message)
        expected = "![Image](screenshot\\.png)"
        self.assertEqual(result, expected)

    def test_pipeline_add_custom_processor(self):
        """Test adding custom processor to pipeline."""
        # Create a new pipeline and add only our custom processor
        pipeline = ContentProcessingPipeline()
        pipeline.processors = []  # Clear default processors

        # Add a mock processor that always returns "CUSTOM"
        custom_processor = MockContentProcessor(ContentType.TEXT, "CUSTOM")
        pipeline.add_processor(custom_processor)

        message = Message(
            speaker="User", content="any text", content_type=ContentType.TEXT
        )
        result = pipeline.process_message(message)
        # Should use the custom processor
        self.assertEqual(result, "CUSTOM")

    def test_pipeline_fallback_to_text(self):
        """Test pipeline fallback to text processing for unknown types."""
        # Create a message with an unknown content type by directly setting the enum
        message = Message(
            speaker="User",
            content="unknown content",
            content_type=ContentType.TEXT,  # Using TEXT as we don't have unknown type
        )

        # Temporarily override the content_type to simulate unknown type
        # This tests the fallback behavior
        original_processors = self.pipeline.processors.copy()
        self.pipeline.processors = []  # Remove all processors

        # Should fallback to text processor
        result = self.pipeline.process_message(message)
        expected = "unknown content"  # Text processor should escape if needed
        self.assertEqual(result, expected)

        # Restore processors
        self.pipeline.processors = original_processors

    def test_pipeline_deterministic_output(self):
        """Test that pipeline produces deterministic output."""
        message = Message(
            speaker="User",
            content="Test message with *markdown*",
            content_type=ContentType.TEXT,
        )

        # Process same message multiple times
        results = []
        for _ in range(5):
            result = self.pipeline.process_message(message)
            results.append(result)

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result, first_result)


if __name__ == "__main__":
    unittest.main()
