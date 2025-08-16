# conv2md Requirements

## Project Overview

**conv2md** is a command-line tool that converts conversations, transcripts, and websites into clean, deterministic Markdown files. It preserves structure, code blocks, and assets while adding useful metadata for archival and note-taking.

## Functional Requirements

### F001 - CLI Interface
- **Description**: Provide intuitive command-line interface for file conversion
- **Acceptance Criteria**:
  - Accept input via `--input <file|url>` parameter
  - Support output directory specification via `--out DIR` (default: ./out)
  - Include help documentation accessible via `--help`
  - Provide clear error messages for invalid inputs
- **Priority**: P0 (Critical)

### F002 - JSON Conversation Processing
- **Description**: Convert JSON conversation files to Markdown format
- **Acceptance Criteria**:
  - Support minimal schema: `{"participants": [...], "messages": [...]}`
  - Process messages with: speaker, timestamp, content fields
  - Generate speaker lines as: `**Speaker — HH:MM**`
  - Create date section headers: `## YYYY-MM-DD`
  - Preserve code blocks as fenced Markdown
  - Add YAML front matter with metadata
- **Priority**: P0 (Critical)

### F003 - Website/HTML Processing
- **Description**: Convert web pages and HTML content to Markdown
- **Acceptance Criteria**:
  - Fetch content using urllib with retries and timeouts
  - Respect robots.txt by default (with `--ignore-robots` override)
  - Extract main content using heuristics (article, main tags)
  - Strip script and style tags
  - Convert HTML elements to Markdown equivalents
  - Download and process images
  - Generate appropriate YAML front matter
- **Priority**: P0 (Critical)

### F004 - Image Handling
- **Description**: Process and store images from web content
- **Acceptance Criteria**:
  - Download images to `assets/` directory by default
  - Use content-hash filenames for deterministic naming
  - Support inline embedding with `--embed-images inline`
  - Handle common image formats (JPEG, PNG, GIF, WebP)
  - Validate image content and size
- **Priority**: P0 (Critical)

### F005 - Deterministic Output
- **Description**: Ensure identical output for identical inputs
- **Acceptance Criteria**:
  - Same input produces byte-for-byte identical output
  - Consistent file naming across runs
  - Deterministic code block fence length calculation
  - Stable ordering of metadata and content
- **Priority**: P0 (Critical)

### F006 - Markdown Generation
- **Description**: Generate clean, standards-compliant Markdown
- **Acceptance Criteria**:
  - Support headings, paragraphs, lists, blockquotes, tables
  - Handle nested backticks in code blocks (extend fence length)
  - Preserve code block language specifications
  - Normalize line endings to \n
  - Generate valid YAML front matter
- **Priority**: P0 (Critical)

### F007 - Configuration Options
- **Description**: Provide configuration flexibility
- **Acceptance Criteria**:
  - Timezone specification: `--tz TIMEZONE` (default: America/Phoenix)
  - Single-file output: `--single-file` (inline all assets)
  - Image embedding options: `--embed-images [file|inline]`
  - Robots.txt override: `--ignore-robots`
- **Priority**: P1 (High)

### F008 - Plugin System
- **Description**: Optional enhancement system using third-party libraries
- **Acceptance Criteria**:
  - Enable with `--use-plugins` flag
  - Core functionality works without plugins
  - Plugin isolation (no contamination of core)
  - Support for LLM enhancements, OCR, readability libraries
- **Priority**: P2 (Medium)

## Non-Functional Requirements

### NF001 - Performance
- **Description**: Efficient processing of various input sizes
- **Requirements**:
  - Process typical web pages (<1MB) in under 5 seconds
  - Handle large conversations (1000+ messages) efficiently
  - Memory usage scales linearly with input size
  - Warn on large inputs (>5MB HTML, >100 images)
- **Priority**: P1 (High)

### NF002 - Reliability
- **Description**: Robust error handling and recovery
- **Requirements**:
  - Graceful handling of network timeouts
  - Clear error messages for malformed inputs
  - Validation of all external inputs
  - Safe handling of missing or corrupted files
- **Priority**: P0 (Critical)

### NF003 - Security
- **Description**: Secure processing of external content
- **Requirements**:
  - Input validation and sanitization
  - Path traversal prevention
  - Safe handling of web content (XSS prevention)
  - No execution of untrusted code
  - Compliance with OWASP Top 10
- **Priority**: P0 (Critical)

### NF004 - Maintainability
- **Description**: Clean, testable codebase
- **Requirements**:
  - Stdlib-only core implementation
  - Clear separation of concerns
  - Comprehensive test coverage (≥90%)
  - Documentation for all public interfaces
  - TDD development approach
- **Priority**: P0 (Critical)

### NF005 - Compatibility
- **Description**: Cross-platform compatibility
- **Requirements**:
  - Python 3.13+ support
  - Windows, macOS, Linux compatibility
  - Unicode handling for international content
  - Timezone-aware timestamp processing
- **Priority**: P1 (High)

## User Stories

### US001 - Convert ChatGPT Export
**As a** user with ChatGPT conversation exports  
**I want to** convert them to readable Markdown  
**So that** I can archive and search my conversations

**Acceptance Criteria**:
- Load JSON file from ChatGPT export
- Generate Markdown with speaker identification
- Preserve timestamps and conversation flow
- Include metadata in YAML front matter

### US002 - Archive Web Articles
**As a** researcher collecting web content  
**I want to** convert articles to Markdown with images  
**So that** I can maintain a local archive

**Acceptance Criteria**:
- Fetch article content from URL
- Download and organize images
- Generate clean Markdown output
- Include source URL and fetch timestamp

### US003 - Batch Processing
**As a** user with multiple files to convert  
**I want to** process them consistently  
**So that** all outputs follow the same format

**Acceptance Criteria**:
- Deterministic output across runs
- Consistent file naming and structure
- Identical metadata formatting

## Security Requirements

### S001 - Input Validation
- All external inputs must be validated before processing
- URL inputs must be verified as safe protocols (http/https)
- File paths must prevent directory traversal attacks
- JSON inputs must be parsed safely without code execution

### S002 - Web Content Security
- HTML content must be sanitized to prevent XSS
- No execution of JavaScript or other embedded code
- Safe handling of malformed HTML
- Proper encoding of output content

### S003 - Network Security
- Respect robots.txt unless explicitly overridden
- Implement reasonable request timeouts
- Use secure HTTP client configuration
- Handle SSL/TLS validation properly

## Architecture Requirements

### A001 - Modular Design
- Clear separation between input processing, conversion logic, and output generation
- Adapter pattern for external dependencies
- Plugin system for optional enhancements
- Testable interfaces and boundaries

### A002 - Dependency Management
- Core functionality uses Python stdlib only
- Third-party dependencies isolated to plugins
- Minimal required dependencies (only CLI framework)
- Clear documentation of all dependencies

## Testing Requirements

### T001 - Test Coverage
- Unit tests for all business logic
- Integration tests for full conversion pipelines
- Golden fixture tests for deterministic output verification
- Security tests for input validation

### T002 - Test Data
- Sample JSON conversations with various formats
- Sample HTML pages with different structures
- Edge cases: malformed inputs, large files, special characters
- Determinism verification across multiple runs

## Documentation Requirements

### D001 - User Documentation
- Clear installation and usage instructions
- Examples for all major use cases
- CLI option reference
- Troubleshooting guide

### D002 - Developer Documentation
- Architecture overview and decisions
- Plugin development guide
- Testing procedures
- Contributing guidelines

## Constraints

### C001 - Technical Constraints
- Python 3.13+ minimum version
- Stdlib-only core (no third-party parsing libraries)
- Must work offline for local files
- Cross-platform compatibility required

### C002 - Design Constraints
- Deterministic output is non-negotiable
- Plugin system must not affect core functionality
- Error handling must be user-friendly
- Performance must be reasonable for typical use cases

## Success Metrics

### M001 - Functional Success
- Successfully converts ChatGPT exports to readable Markdown
- Accurately preserves web page content and structure
- Generates identical output for identical inputs
- Handles edge cases gracefully

### M002 - Quality Success
- Test coverage ≥90%
- Zero critical security vulnerabilities
- User documentation complete and accurate
- Performance meets specified requirements

## Dependencies

### Internal Dependencies
- Python standard library (json, urllib, html.parser, etc.)
- Click framework for CLI interface

### External Dependencies (Plugins Only)
- requests (enhanced HTTP client)
- beautifulsoup4 (advanced HTML parsing)
- openai (LLM integration)
- pytesseract (OCR functionality)

## Risks

### R001 - Technical Risks
- **Risk**: Website structure changes breaking content extraction
- **Mitigation**: Robust heuristics and fallback strategies

### R002 - Security Risks
- **Risk**: Processing malicious web content
- **Mitigation**: Comprehensive input validation and sanitization

### R003 - Performance Risks
- **Risk**: Large inputs causing memory issues
- **Mitigation**: Streaming processing and input size warnings

## Assumptions

### A001 - User Environment
- Users have Python 3.13+ installed
- Users have internet connectivity for web content
- Users understand basic command-line usage

### A002 - Input Formats
- JSON conversations follow documented schema
- Web content uses standard HTML
- Images use common formats (JPEG, PNG, GIF, WebP)