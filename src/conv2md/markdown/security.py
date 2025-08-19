"""Security controls for markdown generation."""

import re
import html
from typing import Dict, Any


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
    str_value = str(value)[:1000]  # Limit to prevent DoS

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
    content = content[:100000]  # 100KB limit

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
    speaker = speaker.strip()[:100]

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
    timestamp = timestamp.strip()[:50]

    # Remove control characters
    timestamp = re.sub(r"[\x00-\x1F\x7F]", "", timestamp)

    # Basic validation - should look like a timestamp
    # Allow common timestamp formats: ISO8601, Unix, human-readable
    if not re.match(r"^[0-9:\-T\sAMPM.+Z]+$", timestamp, re.IGNORECASE):
        raise ValueError(f"Invalid timestamp format: {timestamp}")

    return timestamp
