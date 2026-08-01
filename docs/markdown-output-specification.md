# Markdown Output Specification

This document specifies the markdown output format and generation rules for conv2md.

## Overview

The conv2md markdown generation engine produces clean, deterministic markdown from conversation data. The output follows GitHub Flavored Markdown (GFM) standards with additional conventions for conversation formatting.

## Core Principles

### 1. Deterministic Output
- Identical input produces byte-for-byte identical output across runs
- No timestamps, random values, or environment-dependent data in output
- Consistent ordering and formatting rules

### 2. Security First
- All content is properly escaped and sanitized
- YAML frontmatter injection prevention
- XSS and injection attack mitigation
- Content size limits to prevent DoS

### 3. Readability
- Clean, human-readable format
- Proper spacing and structure
- Consistent speaker and timestamp formatting

## Output Structure

### Document Format
```text
---
[YAML Frontmatter - Optional]
---

[Content Body]
```

### YAML Frontmatter
When metadata is provided, the document begins with YAML frontmatter. Every
value is emitted as a **double-quoted YAML scalar**, including numbers and
collections, which are stringified first:

```yaml
---
created_at: "2024-01-01T12:00:00Z"
message_count: "42"
participants: "['User', 'Assistant']"
source: "json"
title: "Conversation Title"
---
```

**Security Features:**
- All keys sanitized (alphanumeric, underscore, hyphen only)
- Keys emitted in alphabetical order for deterministic output
- Colliding sanitized keys logged as a warning; last value wins
- All values wrapped in double quotes, so `:`, `#`, `|`, `>` and a leading `-`
  are inert rather than parsed as YAML structure
- Values are **not** HTML escaped — the text round-trips back through a YAML
  parser byte-for-byte
- Length limits applied (1000 chars per value, measured before escaping)

## Content Body Structure

### Speaker Lines
```markdown
**Speaker Name — Timestamp**
**Speaker Name:**
```

- Speaker names in bold (`**name**`)
- Optional timestamp separated by em dash (`—`)
- Colon (`:`) when no timestamp present
- All markdown special characters escaped in speaker names and timestamps

### Content Types

#### 1. Text Content
Input `Hello *world* with _emphasis_!` is emitted escaped:

```markdown
**User:**
Hello \*world\* with \_emphasis\_\!
```

- Markdown special characters escaped: `` \ ` * _ { } [ ] ( ) # + - . ! | ``
- Content appears on line following speaker line
- Preserves original line breaks and formatting

#### 2. Code Content
````markdown
**Developer:**
```python
def hello():
    print("world")
```
````

**Code Block Features:**
- Automatic fence length determination
- Handles nested backticks by extending fence length
- Language specification support, restricted to the tag charset
  `[A-Za-z0-9_+#.-]` with a 32 character cap. The language is interpolated into
  the opening fence, so a value outside that charset — one containing a newline
  or backticks, for example — could close its own fence and inject Markdown
  that renders outside the code block. Rejected values fall back to a bare
  fence; `python`, `c++`, `objective-c` and `f#` are all accepted.
- Preserves exact code formatting including whitespace
- Minimum 3 backticks, extends to max(content_backticks + 1, 3)

**Examples:**
- Content with `` `backticks` `` → uses ` ``` `
- Content with `` ``` `` → uses ` ```` `
- Content with `` ```````` `` → uses ` `````````` `

#### 3. Image Content
```markdown
**User:**
![Image](path/to/image.jpg)
```
- Standard markdown image syntax
- Path/URL properly escaped
- Alt text always "Image"

### Message Separation
- Blank line between each message
- No trailing blank line at end of document

## Security Specifications

### Content Sanitization
- Control characters removed (except newlines and tabs)
- Content length limited to 100KB per sanitization pass
- Raw content validated against 10MB limit before sanitization
- Unicode encoding validation

### Speaker Name Validation
- Non-empty after trimming
- 100 character limit
- Control characters removed
- Must contain valid characters after sanitization

### Timestamp Validation
- Empty or whitespace-only input returns the empty string
- Truncated to 50 characters, then control characters removed
- The result must match exactly one of five strict patterns; anything else
  raises `ValueError`:
  1. **ISO 8601** — `YYYY-MM-DD`, optionally `THH:MM:SS`, optional fractional
     seconds, optional `Z` or `±HH:MM` offset
  2. **Human readable** — `YYYY-MM-DD HH:MM:SS`
  3. **24-hour time only** — `HH:MM` or `HH:MM:SS`, hours `00`-`23`
  4. **12-hour time only** — `H:MM` or `H:MM:SS` with `AM`/`PM`, hours `1`-`12`
  5. **Unix seconds** — exactly 10 digits, optionally `.` plus 1-6 digits
- Date and time fields are bounded by the patterns themselves: month `01`-`12`,
  day `01`-`31`, hour `00`-`23`, minute and second `00`-`59`
- Field bounds cannot reject a date such as `2024-02-30` or `2023-02-29`, so
  any value carrying a calendar date has its `YYYY-MM-DD` prefix additionally
  confirmed against the real calendar

### YAML Security
- Values are emitted as **double-quoted scalars**, quotes included
- Quoting - rather than escaping metacharacters in a plain scalar - is what
  makes the output parseable: backslash carries no escape meaning in a YAML
  plain scalar, so a value containing `": "`, `#` or a leading `-` can only be
  represented safely inside quotes
- Truncation to 1000 characters is applied to the raw value, before escaping,
  so the cap bounds caller input rather than the escape sequences added
- Control characters are dropped, then the escapes a double-quoted scalar
  requires are applied in order:
  - `\` → `\\` (first, so the escapes below are not themselves escaped)
  - `"` → `\"`
  - newline → `\n`, carriage return → `\r`, tab → `\t`
- No HTML entity escaping is performed; `<`, `>`, `&` and `'` are preserved
  verbatim so values round-trip through a YAML parser unchanged

## Size Limits

### Per-Message Limits
- Raw content: 10MB before sanitization
- Individual message content checked before processing

### Total Conversation Limits
- Total size: 100MB after sanitization
- Cumulative across all messages in conversation

### Metadata Limits
- YAML values: 1000 characters each
- Keys: alphanumeric, underscore, hyphen only

## Processing Pipeline

### Content Processing Flow
1. **Validation Phase**
   - Check conversation structure
   - Validate speaker names and timestamps
   - Check content sizes before sanitization

2. **Security Phase**
   - Sanitize metadata for YAML safety
   - Sanitize content for markdown safety
   - Apply size limits and encoding validation

3. **Generation Phase**
   - Generate YAML frontmatter if metadata present
   - Process each message through content type pipeline
   - Apply proper formatting and escaping
   - Drop the single trailing blank line that message separation leaves behind,
     so the document does not end with a newline. Whitespace inside a line is
     never stripped — code content is reproduced exactly.

### Pipeline Architecture
The generation uses a pluggable pipeline architecture:

- **TextContentProcessor**: Handles regular text with escaping
- **CodeContentProcessor**: Handles code blocks with fencing
- **ImageContentProcessor**: Handles image references
- **Custom processors**: Can be added for extensibility

## Determinism Guarantees

### Sources of Non-Determinism Eliminated
- No system timestamps in output
- No random identifiers or UUIDs
- No environment-dependent paths or hostnames
- Consistent ordering of metadata keys (alphabetical)
- Stable fence length calculation algorithm

### Testing for Determinism
- Golden fixture tests compare byte-for-byte output
- Multiple runs with identical input must produce identical output
- Tests run across different environments and timestamps

## Error Handling

### Validation Errors
- `InvalidContentError`: Malformed conversation data
- `ContentTooLargeError`: Size limits exceeded  
- `EncodingError`: Unicode encoding issues

### Recovery Strategies
- Graceful degradation for invalid metadata keys
- Fallback to text processing for unknown content types
- Detailed error messages with context

## Metrics and Observability

### Collected Metrics
- Processing time and throughput
- Content size statistics (input/output)
- Content type distribution
- Error and warning counts
- Memory usage tracking

### Logging Levels
- `INFO`: High-level generation progress
- `DEBUG`: Detailed processing steps and metrics
- `ERROR`: Validation and processing failures

## Implementation Notes

### Performance Characteristics
- Memory usage scales linearly with content size
- Processing time dominated by content sanitization
- Efficient for typical conversation sizes (< 1MB)

### Compatibility
- Follows GitHub Flavored Markdown specification
- Compatible with standard markdown parsers
- YAML frontmatter follows Jekyll/Hugo conventions

## Examples

### Simple Conversation
```markdown
**User:**
Hello there!

**Assistant:**
Hi! How can I help you today?
```

### With Timestamps
```markdown
**User — 2024-01-01 12:00:00**
Can you help me with this code?

**Assistant — 2024-01-01 12:00:15**
Of course! Please share your code.
```

### With Code Block
````markdown
**Developer — 12:34**
Here's the implementation:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Reviewer — 12:35**
Looks good, but consider memoization for better performance.
````

### With Nested Backticks
`````markdown
**User:**
I found this in the docs:

````markdown
```python
print("hello")
```
````

How do I handle the nested backticks?
`````

### With Metadata
Keys are sorted alphabetically and every value is a double-quoted scalar:

```markdown
---
created_at: "2024-01-01T12:00:00Z"
message_count: "15"
participants: "['Alice', 'Bob', 'Charlie']"
repository: "my-project"
source: "json"
title: "Code Review Session"
---

**Alice — 12:00**
Let's review the new authentication module.

**Bob — 12:01**
I'll start with the security aspects.
```