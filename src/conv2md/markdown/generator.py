"""Markdown generator for conversations."""

import logging
from dataclasses import replace
from typing import Dict, Any, Optional, List
from conv2md.domain.models import Conversation, Message
from conv2md.markdown.blocks import format_speaker_line
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
from conv2md.markdown.constants import (
    MAX_CONTENT_SANITIZATION_SIZE,
    MAX_MESSAGE_CONTENT_SIZE,
    MAX_TOTAL_CONVERSATION_SIZE,
)

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generates Markdown from conversation data."""

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
        self.metrics_collector.start_conversion()

        try:
            # Validate input and take the sanitized messages it produces, so
            # the raw message never reaches the output
            messages = self._validate_conversation(conversation)

            logger.debug(f"Converting {len(messages)} messages to Markdown")

            lines = []

            # Add YAML frontmatter if metadata provided
            if metadata:
                lines.extend(self._build_frontmatter(metadata))

            # Process all messages
            lines.extend(self._build_message_lines(messages))

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
            # Values arrive as quoted YAML scalars - do not quote them again
            value = safe_metadata[key]
            lines.append(f"{key}: {value}")
        lines.extend(["---", ""])  # Closing delimiter and blank line

        return lines

    def _build_message_lines(self, messages: List[Message]) -> List[str]:
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
                    f"Formatting message {i + 1}: {message.speaker} "
                    f"({message.content_type.value})"
                )

                # Create speaker line with optional timestamp
                speaker_line = format_speaker_line(message.speaker, message.timestamp)
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
                # generate() records the error when it catches the re-raise;
                # recording here as well would double-count one failure
                raise InvalidContentError(
                    f"Failed to process message {i + 1}: {e}"
                ) from e

        return lines

    def _validate_conversation(self, conversation: Conversation) -> List[Message]:
        """Validate and sanitize conversation data before processing.

        Args:
            conversation: Conversation to validate

        Returns:
            List of messages whose speaker, timestamp and content have been
            replaced with their sanitized equivalents. Callers must format
            these rather than the originals, or every sanitization guarantee
            is lost.

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
        sanitized_messages: List[Message] = []

        for i, message in enumerate(conversation.messages):
            if not message.speaker:
                raise InvalidContentError(f"Message {i} missing speaker")

            if message.content is None:
                raise InvalidContentError(f"Message {i} has None content")

            # Validate and sanitize speaker name
            try:
                clean_speaker = validate_speaker_name(message.speaker)
            except ValueError as e:
                raise InvalidContentError(f"Message {i} invalid speaker: {e}") from e

            # Validate timestamp if present
            clean_timestamp = message.timestamp
            if message.timestamp:
                try:
                    clean_timestamp = validate_timestamp(message.timestamp)
                except ValueError as e:
                    raise InvalidContentError(
                        f"Message {i} invalid timestamp: {e}"
                    ) from e

            # Validate content size BEFORE sanitization to catch large content
            try:
                raw_content_bytes = str(message.content).encode("utf-8")
                raw_content_size = len(raw_content_bytes)

                if raw_content_size > MAX_MESSAGE_CONTENT_SIZE:
                    raise ContentTooLargeError(
                        f"Message {i} content exceeds size limit: "
                        f"{raw_content_size} bytes"
                    )

            except UnicodeEncodeError as e:
                raise EncodingError(f"Message {i} has encoding issues: {e}") from e

            # Count the raw payload the caller supplied. Sanitized sizes are
            # capped per message, so accumulating those would measure message
            # count rather than payload size.
            total_size += raw_content_size

            # Reject before sanitizing this message: the conversation is already
            # doomed, so sanitizing it would burn work and emit a misleading
            # truncation warning for content that is never emitted.
            if total_size > MAX_TOTAL_CONVERSATION_SIZE:
                raise ContentTooLargeError(
                    f"Total conversation size exceeds limit: {total_size} bytes"
                )

            # Sanitize content after size validation
            sanitized_content, content_truncated = sanitize_content(
                str(message.content)
            )
            if content_truncated:
                # Losing the tail of a message is a degraded conversion, not a
                # failure: report it and keep the remaining messages.
                self.metrics_collector.record_warning(
                    f"Message {i} content truncated to "
                    f"{MAX_CONTENT_SANITIZATION_SIZE} characters"
                )

            sanitized_messages.append(
                replace(
                    message,
                    speaker=clean_speaker,
                    timestamp=clean_timestamp,
                    content=sanitized_content,
                )
            )

        logger.debug(
            f"Conversation validation passed: {len(conversation.messages)} "
            f"messages, {total_size} bytes"
        )

        return sanitized_messages
