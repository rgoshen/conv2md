"""Exception classes for markdown generation."""


class MarkdownGenerationError(Exception):
    """Base exception for markdown generation errors."""

    pass


class InvalidContentError(MarkdownGenerationError):
    """Raised when content cannot be processed for markdown generation."""

    pass


class EncodingError(MarkdownGenerationError):
    """Raised when content has encoding issues."""

    pass


class ContentTooLargeError(MarkdownGenerationError):
    """Raised when content exceeds size limits."""

    pass
