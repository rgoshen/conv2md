"""Security controls for markdown generation."""

import logging
import re
from datetime import datetime
from typing import Dict, Any, Tuple
from conv2md.markdown.constants import (
    MAX_METADATA_VALUE_LENGTH,
    MAX_SPEAKER_NAME_LENGTH,
    MAX_TIMESTAMP_LENGTH,
    MAX_CONTENT_SANITIZATION_SIZE,
)

logger = logging.getLogger(__name__)

# Control characters that must never reach the output. Newline (\x0A), carriage
# return (\x0D) and tab (\x09) are deliberately excluded: they carry meaning and
# are escaped rather than dropped.
CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

# Speaker names and timestamps are single-line fields, so newline, carriage
# return and tab carry no meaning there either: the whole C0 range plus DEL is
# dropped rather than escaped.
SINGLE_LINE_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1F\x7F]")

# Calendar date with bounded month and day fields. Field bounds alone cannot
# reject dates such as 2024-02-30, so callers also confirm with the calendar.
_DATE_PATTERN = r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])"

# Timestamp shapes accepted by validate_timestamp, compiled once at import:
# the validator runs per message, so rebuilding these per call is pure overhead.
# ISO8601 (2024-08-18T14:30:00Z, 2024-08-18T14:30:00+00:00, 2024-08-18)
_ISO8601_PATTERN = re.compile(
    rf"^{_DATE_PATTERN}(?:T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d"
    r"(?:\.\d+)?(?:[+-]\d{2}:\d{2}|Z)?)?$"
)
# Human readable with spaces (2024-08-18 14:30:00)
_HUMAN_READABLE_PATTERN = re.compile(
    rf"^{_DATE_PATTERN}\s+(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"
)
# Time only, 24-hour: 00-23:00-59:00-59 (14:30:00, 14:30, 02:30:45)
_TIME_24H_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$")
# Time only, 12-hour: 01-12:00-59 AM/PM (2:30 PM)
_TIME_12H_PATTERN = re.compile(
    r"^(?:0?[1-9]|1[0-2]):[0-5]\d(?::[0-5]\d)?\s*[APap][Mm]$"
)
# Unix timestamp (1692364200, 1692364200.123)
_UNIX_PATTERN = re.compile(r"^\d{10}(?:\.\d{1,6})?$")


def sanitize_yaml_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize metadata dictionary for safe YAML frontmatter generation.

    Args:
        metadata: Raw metadata dictionary

    Returns:
        Sanitized metadata dictionary mapping clean keys to quoted YAML scalars
    """
    sanitized = {}

    for key, value in metadata.items():
        # Sanitize key - only allow alphanumeric, underscore, hyphen
        clean_key = re.sub(r"[^a-zA-Z0-9_-]", "", str(key))
        if not clean_key:
            continue  # Skip invalid keys

        # Stripping disallowed characters can map distinct keys onto the same
        # name (e.g. "title#1" and "title1"). Losing a field silently would
        # hide data from the caller, so warn but keep the last value wins rule.
        if clean_key in sanitized:
            logger.warning(
                "Metadata key %r collides with an existing key %r after "
                "sanitization; the previous value is being overwritten",
                str(key),
                clean_key,
            )

        # Sanitize value
        clean_value = sanitize_yaml_value(value)
        sanitized[clean_key] = clean_value

    return sanitized


def sanitize_yaml_value(value: Any) -> str:
    """Sanitize a value into a double-quoted YAML scalar.

    Quoting - rather than escaping metacharacters in a plain scalar - is what
    makes the output parseable: backslash has no escape meaning in a YAML plain
    scalar, so values containing ": ", "#" or a leading "-" can only be
    represented safely inside quotes.

    Args:
        value: Value to sanitize

    Returns:
        A double-quoted YAML scalar, including the surrounding quotes
    """
    # Convert to string and limit length before escaping, so the cap applies to
    # the caller's input rather than to the escape sequences we add.
    str_value = str(value)[:MAX_METADATA_VALUE_LENGTH]

    # Drop characters that a double-quoted scalar cannot carry verbatim
    str_value = CONTROL_CHARACTERS.sub("", str_value)

    # Backslash first, so the escapes added below are not themselves escaped
    str_value = str_value.replace("\\", "\\\\")
    str_value = str_value.replace('"', '\\"')
    str_value = str_value.replace("\n", "\\n")
    str_value = str_value.replace("\r", "\\r")
    str_value = str_value.replace("\t", "\\t")

    return f'"{str_value}"'


def sanitize_content(content: str) -> Tuple[str, bool]:
    """Sanitize content for safe markdown output.

    Args:
        content: Raw content string

    Returns:
        A ``(content, truncated)`` pair. ``truncated`` reports whether the input
        exceeded MAX_CONTENT_SANITIZATION_SIZE and so lost characters. Silently
        dropping the caller's text would be invisible, so the signal is returned
        alongside the text rather than left for the caller to recompute.
    """
    if not content:
        return "", False

    # Limit content length to prevent DoS
    truncated = len(content) > MAX_CONTENT_SANITIZATION_SIZE
    content = content[:MAX_CONTENT_SANITIZATION_SIZE]

    # Remove null bytes and other control characters (except newlines and tabs)
    content = CONTROL_CHARACTERS.sub("", content)

    # Normalize line endings. A "\r\n" pair split by the cut above cannot leave
    # a stray "\r" behind: the second replace maps a lone "\r" to the same "\n"
    # the intact pair would have produced.
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    return content, truncated


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
    speaker = SINGLE_LINE_CONTROL_CHARACTERS.sub("", speaker)

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
    timestamp = SINGLE_LINE_CONTROL_CHARACTERS.sub("", timestamp)

    has_calendar_date = bool(
        _ISO8601_PATTERN.match(timestamp) or _HUMAN_READABLE_PATTERN.match(timestamp)
    )

    if not (
        has_calendar_date
        or _TIME_24H_PATTERN.match(timestamp)
        or _TIME_12H_PATTERN.match(timestamp)
        or _UNIX_PATTERN.match(timestamp)
    ):
        raise ValueError(f"Invalid timestamp format: {timestamp}")

    if has_calendar_date:
        # Field bounds accept dates the calendar does not, such as 2024-02-30
        # or 2023-02-29. Only the calendar itself can settle those.
        try:
            datetime.strptime(timestamp[:10], "%Y-%m-%d")
        except ValueError as error:
            raise ValueError(f"Invalid timestamp format: {timestamp}") from error

    return timestamp
