"""Constants for markdown generation."""

# Size limits for content validation
MAX_MESSAGE_CONTENT_SIZE = 10 * 1024 * 1024  # 10MB per message
MAX_TOTAL_CONVERSATION_SIZE = 100 * 1024 * 1024  # 100MB total conversation
MAX_CONTENT_SANITIZATION_SIZE = 100 * 1024  # 100KB content sanitization limit

# Size limits for metadata and fields
MAX_METADATA_VALUE_LENGTH = 1000  # Maximum length for metadata values
MAX_SPEAKER_NAME_LENGTH = 100  # Maximum length for speaker names
MAX_TIMESTAMP_LENGTH = 50  # Maximum length for timestamp strings
