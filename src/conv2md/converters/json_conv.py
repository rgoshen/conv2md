"""JSON conversation converter."""

import json
import logging

from conv2md.domain.models import Conversation, Message

logger = logging.getLogger(__name__)


class ConversationParseError(Exception):
    """Raised when conversation data cannot be parsed."""

    pass


class JSONConverter:
    """Converts JSON conversations to structured conversation objects."""

    def parse(self, json_string: str) -> Conversation:
        """Parse JSON string to Conversation object.

        Args:
            json_string: JSON formatted conversation data

        Returns:
            Conversation object with parsed messages

        Raises:
            ConversationParseError: When conversation data is invalid
            json.JSONDecodeError: When JSON is malformed
            KeyError: When required fields are missing
        """
        logger.info("Starting JSON conversation parsing")

        try:
            data = json.loads(json_string)
            logger.debug("JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            raise

        # Validate messages exist and not empty
        if "messages" not in data:
            logger.error("Missing required 'messages' field in JSON data")
            raise KeyError("Required field 'messages' not found in conversation data")

        if not data["messages"]:
            logger.error("Validation error: Messages list is empty")
            raise ConversationParseError("Conversation messages list cannot be empty")

        logger.debug(f"Found {len(data['messages'])} messages to process")

        messages = []
        for i, msg_data in enumerate(data["messages"]):
            # Validate message content types
            try:
                speaker = msg_data["speaker"]
                content = msg_data["content"]
                logger.debug(f"Processing message {i+1}: speaker='{speaker}'")
            except KeyError as e:
                logger.error(f"Message {i} missing required field: {e}")
                raise

            if not isinstance(content, str):
                error_msg = (
                    f"Message {i}: content must be string, "
                    f"got {type(content).__name__}"
                )
                logger.error(f"Validation error: {error_msg}")
                raise ConversationParseError(error_msg)

            message = Message(speaker=speaker, content=content)
            messages.append(message)

        logger.info(f"Parsed {len(messages)} messages successfully")
        conversation = Conversation(messages=messages)
        logger.info("JSON parsing completed")

        return conversation
