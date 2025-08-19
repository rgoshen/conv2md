"""Domain models for conversation data."""

from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    """Represents a single message in a conversation."""

    speaker: str
    content: str


@dataclass
class Conversation:
    """Represents a conversation with multiple messages."""

    messages: List[Message]
