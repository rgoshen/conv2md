"""Security controls for markdown generation."""

import re
import html
from typing import Dict, Any
from conv2md.markdown.constants import (
    MAX_METADATA_VALUE_LENGTH,
    MAX_SPEAKER_NAME_LENGTH,
    MAX_TIMESTAMP_LENGTH,
    MAX_CONTENT_SANITIZATION_SIZE,
)


def sanitize_yaml_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize metadata dictionary for safe YAML frontmatter generation.

    Args:
        metadata: Raw metadata dictionary

    Returns:
        Sanitized metadata dictionary
    """
    sanitized = {}

    for key, value in metadata.items():
        # Sanitize key - only allow alphanumeric, underscore, hyphen
        clean_key = re.sub(r"[^a-zA-Z0-9_-]", "", str(key))
        if not clean_key:
            continue  # Skip invalid keys

        # Sanitize value
        clean_value = sanitize_yaml_value(value)
        sanitized[clean_key] = clean_value

    return sanitized


def sanitize_yaml_value(value: Any) -> str:
    """Sanitize a value for safe YAML output.

    Args:
        value: Value to sanitize

    Returns:
        Sanitized string value safe for YAML
    """
    # Convert to string and limit length
    str_value = str(value)[:MAX_METADATA_VALUE_LENGTH]

    # HTML escape first to prevent injection
    str_value = html.escape(str_value)

    # Escape YAML special characters
    str_value = str_value.replace("\\", "\\\\")  # Escape backslashes first
    str_value = str_value.replace(":", "\\:")
    str_value = str_value.replace('"', '\\"')
    str_value = str_value.replace("'", "\\'")
    str_value = str_value.replace("\n", "\\n")
    str_value = str_value.replace("\r", "\\r")
    str_value = str_value.replace("\t", "\\t")
    str_value = str_value.replace("-", "\\-")  # Prevent list interpretation
    str_value = str_value.replace("#", "\\#")  # Prevent comment interpretation
    str_value = str_value.replace("|", "\\|")  # Prevent literal block
    str_value = str_value.replace(">", "\\>")  # Prevent folded block
    str_value = str_value.replace("[", "\\[")  # Prevent array
    str_value = str_value.replace("]", "\\]")
    str_value = str_value.replace("{", "\\{")  # Prevent object
    str_value = str_value.replace("}", "\\}")

    return str_value


def sanitize_content(content: str) -> str:
    """Sanitize content for safe markdown output.

    Args:
        content: Raw content string

    Returns:
        Sanitized content safe for markdown
    """
    if not content:
        return ""

    # Limit content length to prevent DoS
    content = content[:MAX_CONTENT_SANITIZATION_SIZE]

    # Remove null bytes and other control characters (except newlines and tabs)
    content = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", content)

    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    return content


def validate_speaker_name(speaker: str) -> str:
    """Validate and sanitize speaker name.

    Args:
        speaker: Raw speaker name

    Returns:
        Sanitized speaker name

    Raises:
        ValueError: If speaker name is invalid
    """
    if not speaker or not speaker.strip():
        raise ValueError("Speaker name cannot be empty")

    # Limit length
    speaker = speaker.strip()[:MAX_SPEAKER_NAME_LENGTH]

    # Remove control characters
    speaker = re.sub(r"[\x00-\x1F\x7F]", "", speaker)

    if not speaker:
        raise ValueError("Speaker name contains only invalid characters")

    return speaker


def validate_timestamp(timestamp: str) -> str:
    """Validate and sanitize timestamp string.

    Args:
        timestamp: Raw timestamp string

    Returns:
        Sanitized timestamp string

    Raises:
        ValueError: If timestamp format is invalid
    """
    if not timestamp:
        return ""

    # Limit length
    timestamp = timestamp.strip()[:MAX_TIMESTAMP_LENGTH]
    
    # Return empty if only whitespace after stripping
    if not timestamp:
        return ""

    # Remove control characters
    timestamp = re.sub(r"[\x00-\x1F\x7F]", "", timestamp)

    # Improved validation for common timestamp formats
    # Pattern 1: ISO8601 formats (2024-08-18T14:30:00Z, 2024-08-18T14:30:00+00:00, 2024-08-18)
    iso8601_pattern = r"^\d{4}-\d{2}-\d{2}(?:T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?(?:[+-]\d{2}:\d{2}|Z)?)?$"
    
    # Pattern 2: Time only formats (14:30:00, 14:30, 2:30 PM, 02:30:45)
    # 24-hour: 00-23:00-59:00-59, 12-hour: 01-12:00-59 AM/PM
    time_24h_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$"
    time_12h_pattern = r"^(?:0?[1-9]|1[0-2]):[0-5]\d(?::[0-5]\d)?\s*[APap][Mm]$"
    
    # Pattern 3: Unix timestamp (1692364200, 1692364200.123)
    unix_pattern = r"^\d{10}(?:\.\d{1,6})?$"
    
    # Pattern 4: Human readable with spaces (2024-08-18 14:30:00)
    human_readable_pattern = r"^\d{4}-\d{2}-\d{2}\s+(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"
    
    if not (re.match(iso8601_pattern, timestamp) or 
            re.match(time_24h_pattern, timestamp) or 
            re.match(time_12h_pattern, timestamp) or
            re.match(unix_pattern, timestamp) or
            re.match(human_readable_pattern, timestamp)):
        raise ValueError(f"Invalid timestamp format: {timestamp}")

    return timestamp
