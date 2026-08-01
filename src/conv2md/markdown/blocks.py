"""Code block handling for Markdown generation."""

import re
from typing import Optional

# Info strings are interpolated verbatim into the opening fence, so an
# unvalidated language can close its own fence and inject Markdown that renders
# outside the code block. Only the characters real language tags use are
# allowed; the length cap keeps an oversized tag out of the header.
LANGUAGE_TAG_PATTERN = re.compile(r"[A-Za-z0-9_+#.-]{1,32}")


def determine_fence_length(content: str, min_length: int = 3) -> int:
    """Determine appropriate fence length for code block content.

    Analyzes content to find sequences of backticks and returns
    a fence length that's longer than any backtick sequence in the content.

    Args:
        content: Code content to analyze
        min_length: Minimum fence length (default: 3)

    Returns:
        Appropriate fence length for safe code block fencing
    """
    if not content:
        return min_length

    # Find all sequences of consecutive backticks
    backtick_sequences = re.findall(r"`+", content)

    if not backtick_sequences:
        return min_length

    # Find the longest sequence
    max_backticks = max(len(seq) for seq in backtick_sequences)

    # Return fence length that's at least one longer than max sequence
    return max(min_length, max_backticks + 1)


def create_code_block(content: str, language: Optional[str] = None) -> str:
    """Create a properly fenced code block.

    Args:
        content: Code content to fence
        language: Optional language identifier for syntax highlighting. Values
            outside the accepted identifier charset are dropped rather than
            emitted, so an untrusted language cannot break out of the fence.

    Returns:
        Properly fenced code block string
    """
    fence_length = determine_fence_length(content)
    fence = "`" * fence_length

    # Add language identifier only when it is a recognisable tag
    candidate_tag = language or ""
    language_tag = (
        candidate_tag if LANGUAGE_TAG_PATTERN.fullmatch(candidate_tag) else ""
    )

    # Ensure content ends with newline for proper block formatting
    if content and not content.endswith("\n"):
        content += "\n"

    return f"{fence}{language_tag}\n{content}{fence}"


def escape_markdown_content(text: str) -> str:
    """Escape Markdown special characters in regular content.

    Args:
        text: Text content to escape

    Returns:
        Text with Markdown special characters escaped
    """
    # Escape Markdown special characters: \ ` * _ { } [ ] ( ) # + - . ! |
    escape_chars = "\\`*_{}[]()#+-.!|"
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")
    return text


def format_speaker_line(speaker: str, timestamp: Optional[str] = None) -> str:
    """Format a speaker line with optional timestamp.

    Args:
        speaker: Speaker name
        timestamp: Optional timestamp string

    Returns:
        Formatted speaker line in Markdown bold format
    """
    escaped_speaker = escape_markdown_content(speaker)

    if timestamp:
        escaped_timestamp = escape_markdown_content(timestamp)
        return f"**{escaped_speaker} — {escaped_timestamp}**"
    else:
        return f"**{escaped_speaker}:**"


def create_date_marker(date_str: str) -> str:
    """Create a date marker heading.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Formatted date marker as level 2 heading
    """
    # For date markers, we don't need to escape hyphens since they're in heading context
    # Only escape truly problematic characters for headings
    safe_date = date_str.replace("#", "\\#").replace("*", "\\*").replace("_", "\\_")
    return f"## {safe_date}"
