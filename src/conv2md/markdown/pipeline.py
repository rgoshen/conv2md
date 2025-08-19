"""Content processing pipeline for markdown generation."""

from abc import ABC, abstractmethod
from typing import Any, List
from conv2md.domain.models import Message, ContentType


class ContentProcessor(ABC):
    """Abstract base class for content processors."""

    @abstractmethod
    def can_process(self, content_type: ContentType) -> bool:
        """Check if this processor can handle the given content type."""
        pass

    @abstractmethod
    def process(self, message: Message) -> str:
        """Process message content into markdown format."""
        pass


class TextContentProcessor(ContentProcessor):
    """Processor for text content."""

    def can_process(self, content_type: ContentType) -> bool:
        """Check if processor can handle text content."""
        return content_type == ContentType.TEXT

    def process(self, message: Message) -> str:
        """Process text content into escaped markdown."""
        from conv2md.markdown.blocks import escape_markdown_content

        return escape_markdown_content(str(message.content))


class CodeContentProcessor(ContentProcessor):
    """Processor for code content."""

    def can_process(self, content_type: ContentType) -> bool:
        """Check if processor can handle code content."""
        return content_type == ContentType.CODE

    def process(self, message: Message) -> str:
        """Process code content into fenced code blocks."""
        from conv2md.markdown.blocks import create_code_block

        return create_code_block(message.content, message.language)


class ImageContentProcessor(ContentProcessor):
    """Processor for image content."""

    def can_process(self, content_type: ContentType) -> bool:
        """Check if processor can handle image content."""
        return content_type == ContentType.IMAGE

    def process(self, message: Message) -> str:
        """Process image content into markdown image format."""
        from conv2md.markdown.blocks import escape_markdown_content

        alt_text = escape_markdown_content(str(message.content))
        return f"![Image]({alt_text})"


class ContentProcessingPipeline:
    """Pipeline for processing different content types."""

    def __init__(self):
        """Initialize pipeline with default processors."""
        self.processors: List[ContentProcessor] = [
            TextContentProcessor(),
            CodeContentProcessor(),
            ImageContentProcessor(),
        ]

    def add_processor(self, processor: ContentProcessor) -> None:
        """Add a custom content processor to the pipeline."""
        self.processors.append(processor)

    def process_message(self, message: Message) -> str:
        """Process a message using the appropriate processor.

        Args:
            message: Message to process

        Returns:
            Processed markdown content

        Raises:
            ValueError: If no processor can handle the content type
        """
        for processor in self.processors:
            if processor.can_process(message.content_type):
                return processor.process(message)

        # Fallback to text processing if no specific processor found
        text_processor = TextContentProcessor()
        return text_processor.process(message)
