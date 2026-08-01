"""Domain models for conversation data."""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ContentType(Enum):
    """Enumeration of supported content types."""

    TEXT = "text"
    CODE = "code"
    IMAGE = "image"


@dataclass
class Message:
    """Represents a single message in a conversation."""

    speaker: str
    content: str
    timestamp: Optional[str] = None
    content_type: ContentType = ContentType.TEXT
    language: Optional[str] = None  # For code blocks


@dataclass
class Conversation:
    """Represents a conversation with multiple messages."""

    messages: List[Message]
