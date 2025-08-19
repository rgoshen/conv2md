"""Markdown generator for conversations."""

import logging
from typing import Dict, Any, Optional, List
from conv2md.domain.models import Conversation, ContentType
from conv2md.markdown.blocks import format_speaker_line, create_date_marker
from conv2md.markdown.pipeline import ContentProcessingPipeline
from conv2md.markdown.metrics import MetricsCollector
from conv2md.markdown.security import (
    sanitize_yaml_metadata,
    sanitize_content,
    validate_speaker_name,
    validate_timestamp,
)
from conv2md.markdown.exceptions import (
    InvalidContentError,
    EncodingError,
    ContentTooLargeError,
)

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generates Markdown from conversation data."""

    # Configuration constants
    MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10MB limit per message
    MAX_TOTAL_SIZE = 100 * 1024 * 1024  # 100MB total limit

    def __init__(self, pipeline: Optional[ContentProcessingPipeline] = None):
        """Initialize the markdown generator.

        Args:
            pipeline: Optional custom content processing pipeline
        """
        self.pipeline = pipeline or ContentProcessingPipeline()
        self.metrics_collector = MetricsCollector()

    def generate(
        self, conversation: Conversation, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate Markdown from conversation.

        Args:
            conversation: Conversation object to convert
            metadata: Optional metadata to include as YAML frontmatter

        Returns:
            Markdown formatted string

        Raises:
            InvalidContentError: If conversation data is invalid
            EncodingError: If content has encoding issues
            ContentTooLargeError: If content exceeds size limits
        """
        logger.info("Starting Markdown generation")

        # Start metrics collection
        metrics = self.metrics_collector.start_conversion()

        try:
            # Validate input
            self._validate_conversation(conversation)

            logger.debug(
                f"Converting {len(conversation.messages)} messages to Markdown"
            )

            lines = []

            # Add YAML frontmatter if metadata provided
            if metadata:
                lines.extend(self._build_frontmatter(metadata))

            # Process all messages
            lines.extend(self._build_message_lines(conversation.messages))

            # Remove trailing blank line
            if lines and lines[-1] == "":
                lines.pop()

            result = "\n".join(lines)
            markdown_length = len(result)

            # Finish metrics collection
            final_metrics = self.metrics_collector.finish_conversion(markdown_length)

            logger.info(f"Markdown generation completed: {markdown_length} characters")
            logger.debug(f"Conversion metrics: {final_metrics.to_dict()}")

            return result

        except Exception as e:
            # Record error in metrics before re-raising
            self.metrics_collector.record_error(e)
            raise

    def _build_frontmatter(self, metadata: Dict[str, Any]) -> List[str]:
        """Build YAML frontmatter lines from metadata.

        Args:
            metadata: Metadata dictionary to convert to YAML frontmatter

        Returns:
            List of frontmatter lines including opening/closing delimiters
        """
        logger.debug(f"Adding YAML frontmatter with {len(metadata)} fields")
        
        # Sanitize metadata for security
        safe_metadata = sanitize_yaml_metadata(metadata)

        lines = ["---"]
        # Sort keys for deterministic output
        for key in sorted(safe_metadata.keys()):
            value = safe_metadata[key]
            lines.append(f"{key}: {value}")
        lines.extend(["---", ""])  # Closing delimiter and blank line

        return lines

    def _build_message_lines(self, messages) -> List[str]:
        """Build markdown lines from conversation messages.

        Args:
            messages: List of Message objects to process

        Returns:
            List of markdown lines for all messages

        Raises:
            InvalidContentError: If message processing fails
        """
        lines = []

        for i, message in enumerate(messages):
            try:
                # Format each message with enhanced speaker line and content handling
                logger.debug(
                    f"Formatting message {i + 1}: {message.speaker} ({message.content_type.value})"
                )

                # Create speaker line with optional timestamp
                speaker_line = format_speaker_line(
                    message.speaker, message.timestamp
                )
                lines.append(speaker_line)

                # Process content using the pipeline
                processed_content = self.pipeline.process_message(message)
                lines.append(processed_content)

                # Record metrics for this message
                content_size = len(str(message.content))
                self.metrics_collector.record_message_processed(
                    message.content_type.value, content_size
                )

                lines.append("")  # Add blank line between messages

            except (ValueError, TypeError, AttributeError) as e:
                logger.error(f"Error processing message {i + 1}: {e}")
                self.metrics_collector.record_error(e)
                raise InvalidContentError(
                    f"Failed to process message {i + 1}: {e}"
                ) from e

        return lines

    def _validate_conversation(self, conversation: Conversation) -> None:
        """Validate conversation data before processing.

        Args:
            conversation: Conversation to validate

        Raises:
            InvalidContentError: If conversation data is invalid
            ContentTooLargeError: If content exceeds limits
            EncodingError: If content has encoding issues
        """
        if not conversation:
            raise InvalidContentError("Conversation cannot be None")

        if not conversation.messages:
            raise InvalidContentError("Conversation must have at least one message")

        total_size = 0

        for i, message in enumerate(conversation.messages):
            if not message.speaker:
                raise InvalidContentError(f"Message {i} missing speaker")

            if message.content is None:
                raise InvalidContentError(f"Message {i} has None content")

            # Validate and sanitize speaker name
            try:
                validate_speaker_name(message.speaker)
            except ValueError as e:
                raise InvalidContentError(f"Message {i} invalid speaker: {e}")

            # Validate timestamp if present
            if message.timestamp:
                try:
                    validate_timestamp(message.timestamp)
                except ValueError as e:
                    raise InvalidContentError(f"Message {i} invalid timestamp: {e}")

            # Validate content size BEFORE sanitization to catch large content
            try:
                raw_content_bytes = str(message.content).encode("utf-8")
                raw_content_size = len(raw_content_bytes)

                if raw_content_size > self.MAX_CONTENT_SIZE:
                    raise ContentTooLargeError(
                        f"Message {i} content exceeds size limit: {raw_content_size} bytes"
                    )

            except UnicodeEncodeError as e:
                raise EncodingError(f"Message {i} has encoding issues: {e}")

            # Sanitize content after size validation
            sanitized_content = sanitize_content(str(message.content))

            # Add sanitized content size to total
            sanitized_size = len(sanitized_content.encode("utf-8"))
            total_size += sanitized_size

        if total_size > self.MAX_TOTAL_SIZE:
            raise ContentTooLargeError(
                f"Total conversation size exceeds limit: {total_size} bytes"
            )

        logger.debug(
            f"Conversation validation passed: {len(conversation.messages)} messages, {total_size} bytes"
        )
