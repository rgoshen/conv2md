"""Markdown generator for conversations."""

import logging
from typing import Dict, Any, Optional
from conv2md.domain.models import Conversation

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generates Markdown from conversation data."""

    def generate(
        self, conversation: Conversation, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate Markdown from conversation.

        Args:
            conversation: Conversation object to convert
            metadata: Optional metadata to include as YAML frontmatter

        Returns:
            Markdown formatted string
        """
        logger.info("Starting Markdown generation")
        logger.debug(f"Converting {len(conversation.messages)} messages to Markdown")

        lines = []

        # Add YAML frontmatter if metadata provided
        if metadata:
            logger.debug(f"Adding YAML frontmatter with {len(metadata)} fields")
            lines.append("---")
            for key, value in metadata.items():
                lines.append(f"{key}: {value}")
            lines.append("---")
            lines.append("")  # Blank line after frontmatter

        for i, message in enumerate(conversation.messages):
            # Format each message as bold speaker with content
            logger.debug(f"Formatting message {i+1}: {message.speaker}")
            lines.append(f"**{message.speaker}:** {message.content}")
            lines.append("")  # Add blank line between messages

        # Remove trailing blank line
        if lines and lines[-1] == "":
            lines.pop()

        markdown_length = len("\n".join(lines))
        logger.info(f"Markdown generation completed: {markdown_length} characters")

        return "\n".join(lines)
