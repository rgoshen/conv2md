# JSON Conversation Schema

This document defines the JSON schema for conversation inputs to conv2md.

## Minimal Schema

The minimal required JSON structure for conversation processing:

```json
{
  "messages": [
    {
      "speaker": "string",
      "content": "string"
    }
  ]
}
```

## Schema Specification

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messages` | Array[Message] | Yes | Array of conversation messages |

### Message Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `speaker` | string | Yes | Name/identifier of the message speaker |
| `content` | string | Yes | Text content of the message |

## Validation Rules

### Required Fields
- Root object MUST contain `messages` field
- `messages` array MUST NOT be empty
- Each message MUST contain both `speaker` and `content` fields

### Data Types
- `speaker`: Must be a string (any non-empty string value)
- `content`: Must be a string (can be empty string)

### Constraints
- Minimum 1 message required
- No maximum message limit (memory permitting)
- Speaker names are case-sensitive
- Content preserves whitespace and formatting

## Examples

### Simple Conversation
```json
{
  "messages": [
    {
      "speaker": "User",
      "content": "Hello!"
    },
    {
      "speaker": "Assistant",
      "content": "Hi there! How can I help you?"
    }
  ]
}
```

### Multi-turn Conversation
```json
{
  "messages": [
    {
      "speaker": "User",
      "content": "What is Python?"
    },
    {
      "speaker": "Assistant", 
      "content": "Python is a high-level programming language known for its simplicity and readability."
    },
    {
      "speaker": "User",
      "content": "Can you show me a simple example?"
    },
    {
      "speaker": "Assistant",
      "content": "Sure! Here's a simple Python script:\n\n```python\nprint('Hello, World!')\n```"
    }
  ]
}
```

### Different Speaker Types
```json
{
  "messages": [
    {
      "speaker": "Customer",
      "content": "I need help with my order."
    },
    {
      "speaker": "Support Agent",
      "content": "I'd be happy to help. What's your order number?"
    },
    {
      "speaker": "Customer", 
      "content": "Order #12345"
    }
  ]
}
```

## Error Handling

### Invalid JSON Structure
The following will raise `json.JSONDecodeError`:
```json
{
  "messages": [
    {"speaker": "User", "content": "Hello"
    // Missing closing brace
```

### Missing Required Fields
The following will raise `KeyError`:
```json
{
  "conversations": []  // Wrong field name
}
```

```json
{
  "messages": [
    {"speaker": "User"}  // Missing content field
  ]
}
```

### Invalid Data Types
The following will raise `ConversationParseError`:
```json
{
  "messages": []  // Empty messages array
}
```

```json
{
  "messages": [
    {"speaker": "User", "content": 123}  // Content must be string
  ]
}
```

## Output Format

Conversations are converted to Markdown with the following format:

```markdown
**Speaker:** Message content

**Speaker:** Message content
```

### With Metadata
When metadata is provided, YAML frontmatter is added:

```markdown
---
title: Conversation Title
source: input.json
---

**Speaker:** Message content
```

## Future Extensions

The schema may be extended in future versions to support:
- Message timestamps
- Message IDs
- Thread/conversation metadata
- Message types (text, image, file)
- Speaker metadata (roles, avatars)

Current implementation focuses on the minimal viable schema for reliable conversation processing.