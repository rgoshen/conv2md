# conv2md Task List

## Legend

- [ ] Not started
- [x] Complete
- [~] In progress
- [!] Blocked/Issues

## Milestone 1: MVP Core (P0) - Due: TBD

### Feature: Project Foundation (P0)

- [x] Requirements gathering and documentation
- [x] Project structure setup per CLAUDE_UNIVERSAL.md
- [x] Initial architecture design and ADR-001
- [ ] Core domain models and interfaces
- [~] Test infrastructure setup (directory structure established; pending config, CI, and initial test cases)

**Dependencies**: None
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Feature: CLI Interface (P0) - F001

- [ ] Core behavior: Argument parsing with click framework
- [ ] Error handling: Input validation and user-friendly error messages
- [ ] Security: Path sanitization and input validation
- [ ] Tests: CLI argument parsing and validation tests
- [ ] Docs: CLI usage documentation

**Dependencies**: Project Foundation
**Estimate**: S (half-day)
**Assignee**: TBD

### Feature: JSON Conversation Processing (P0) - F002

- [ ] Core behavior: Parse minimal JSON schema and convert to Markdown
- [ ] Error handling: Malformed JSON, missing fields, invalid timestamps
- [ ] Integration points: File I/O adapter, Markdown generator interface
- [ ] Security controls: JSON parsing safety, content sanitization
- [ ] Observability: Logging for parse errors and conversion steps
- [ ] Testing strategy: Unit tests + golden fixtures for determinism
- [ ] Documentation: JSON schema specification

**Dependencies**: CLI Interface, Core Domain Models
**Estimate**: L (3-5 days)
**Assignee**: TBD

### Feature: Markdown Generation Engine (P0) - F006

- [ ] Core behavior: Convert structured data to clean Markdown
- [ ] Error handling: Invalid content, encoding issues
- [ ] Integration points: Content processing pipeline
- [ ] Security controls: Output encoding and sanitization
- [ ] Observability: Conversion metrics and error tracking
- [ ] Testing strategy: Code block fence handling, determinism tests
- [ ] Documentation: Markdown output specification

**Dependencies**: Core Domain Models
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Feature: Deterministic Output System (P0) - F005

- [ ] Core behavior: Ensure identical outputs for identical inputs
- [ ] Error handling: Hash validation, consistency checks
- [ ] Integration points: File naming, content generation
- [ ] Security controls: Prevent timing attacks on file operations
- [ ] Observability: Determinism validation metrics
- [ ] Testing strategy: Golden fixture tests across multiple runs
- [ ] Documentation: Determinism guarantees and implementation

**Dependencies**: Markdown Generation Engine
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Feature: Website/HTML Processing (P0) - F003

- [ ] Core behavior: Fetch URLs and convert HTML to Markdown
- [ ] Error handling: Network timeouts, invalid URLs, malformed HTML
- [ ] Integration points: HTTP client adapter, HTML parser wrapper
- [ ] Security controls: URL validation, content sanitization, robots.txt
- [ ] Observability: Request timing, response size, error rates
- [ ] Testing strategy: Mock HTTP responses, various HTML structures
- [ ] Documentation: Supported HTML elements and conversion rules

**Dependencies**: Markdown Generation Engine, HTTP Adapter
**Estimate**: L (3-5 days)
**Assignee**: TBD

### Feature: Image Processing (P0) - F004

- [ ] Core behavior: Download, hash, and organize images
- [ ] Error handling: Download failures, invalid formats, large files
- [ ] Integration points: File system adapter, HTTP client
- [ ] Security controls: Image validation, size limits, path sanitization
- [ ] Observability: Download metrics, storage usage
- [ ] Testing strategy: Mock image downloads, various formats
- [ ] Documentation: Supported formats and storage options

**Dependencies**: Website/HTML Processing
**Estimate**: M (1-2 days)
**Assignee**: TBD

## Milestone 2: Enhanced Features (P1) - Due: TBD

### Feature: Configuration System (P1) - F007

- [ ] Core behavior: Timezone handling, output options, format settings
- [ ] Error handling: Invalid timezones, conflicting options
- [ ] Integration points: CLI argument processing, core converters
- [ ] Security controls: Configuration validation
- [ ] Tests: Configuration parsing and validation
- [ ] Docs: Configuration options reference

**Dependencies**: Core MVP functionality
**Estimate**: S (half-day)
**Assignee**: TBD

### Feature: Advanced Markdown Features (P1)

- [ ] TOC generation with `--toc` flag
- [ ] Task list conversion (`- [ ]` syntax)
- [ ] Mermaid diagram passthrough
- [ ] Math expression passthrough (`$...$`, `$$...$$`)
- [ ] Slugified internal anchors
- [ ] Tests: Various content types and edge cases
- [ ] Docs: Advanced feature documentation

**Dependencies**: Markdown Generation Engine
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Feature: Input Validation & Guardrails (P1)

- [ ] Large input warnings (>5MB HTML, >100 images)
- [ ] Content type validation
- [ ] Reasonable timeout enforcement
- [ ] Memory usage monitoring
- [ ] Tests: Large input handling, resource limits
- [ ] Docs: Performance guidelines

**Dependencies**: Core MVP functionality
**Estimate**: S (half-day)
**Assignee**: TBD

## Milestone 3: Plugin System (P2) - Due: TBD

### Feature: Plugin Architecture (P2) - F008

- [ ] Core behavior: Plugin discovery, loading, and interface
- [ ] Error handling: Plugin failures, missing dependencies
- [ ] Integration points: Plugin isolation, core functionality protection
- [ ] Security controls: Plugin sandboxing, safe loading
- [ ] Tests: Plugin loading, isolation, fallback behavior
- [ ] Docs: Plugin development guide

**Dependencies**: Core MVP stable
**Estimate**: L (3-5 days)
**Assignee**: TBD

### Feature: LLM Enhancement Plugins (P2)

- [ ] Better title generation
- [ ] Content summarization
- [ ] Image alt-text generation
- [ ] Tests: Plugin functionality with mocked LLM responses
- [ ] Docs: LLM plugin configuration

**Dependencies**: Plugin Architecture
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Feature: OCR Plugin (P2)

- [ ] Image text extraction
- [ ] Integration with tesseract
- [ ] Tests: OCR accuracy and error handling
- [ ] Docs: OCR setup and usage

**Dependencies**: Plugin Architecture, Image Processing
**Estimate**: M (1-2 days)
**Assignee**: TBD

## Cross-Cutting Tasks

### Security Implementation

- [ ] OWASP Top 10 risk assessment and mitigation
- [ ] Input validation framework
- [ ] Output sanitization
- [ ] Security testing suite
- [ ] ASVS compliance matrix

**Dependencies**: Core architecture
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Testing Infrastructure

- [ ] unittest framework setup
- [ ] Golden fixture system
- [ ] Determinism validation framework
- [ ] Mock infrastructure for external dependencies
- [ ] CI/CD pipeline configuration

**Dependencies**: Project structure
**Estimate**: M (1-2 days)
**Assignee**: TBD

### Documentation System

- [ ] API documentation
- [ ] User guide and examples
- [ ] Architecture documentation
- [ ] Security documentation
- [ ] Plugin development guide

**Dependencies**: Core functionality
**Estimate**: M (1-2 days)
**Assignee**: TBD

## Backlog (Not Scheduled)

### P2 Features

- Advanced HTML table handling
- Custom CSS styling support
- Batch processing mode
- Configuration file support

### P3 Features

- Web UI for conversion
- Browser extension
- API server mode
- Real-time collaboration features

---

## Task Management Notes

- Tasks should be completed in dependency order
- Each task requires passing tests before proceeding
- Update this list daily with progress and new discoveries
- Create ADRs for significant technical decisions
- Maintain daily development summaries in `summary/`
