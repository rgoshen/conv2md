# conv2md Architecture Overview

## System Context

conv2md is a command-line tool that processes two primary input types:
1. JSON conversation files (local files)
2. Website URLs (remote HTTP resources)

Both are converted to deterministic Markdown output with optional image assets.

## Architecture Pattern

The system follows **Hexagonal Architecture (Ports & Adapters)** with Clean Architecture layering to achieve:
- Stdlib-only core functionality
- Optional plugin enhancement system
- Deterministic, testable output
- Clear security boundaries

## Layer Responsibilities

### Domain Layer (Core Business Logic)
- **Purpose**: Pure business logic using Python stdlib only
- **Contents**: Entities, value objects, domain services
- **Dependencies**: None (stdlib only)
- **Examples**: Conversation entity, Markdown generation rules, content validation

### Application Layer (Use Cases)
- **Purpose**: Orchestrate domain logic for specific user scenarios
- **Contents**: Use case implementations, workflow coordination
- **Dependencies**: Domain layer, port interfaces
- **Examples**: ConvertConversationUseCase, ConvertWebsiteUseCase

### Adapter Layer (External Integration)
- **Purpose**: Implement port interfaces for external systems
- **Contents**: Concrete implementations of external interactions
- **Dependencies**: Application ports, external libraries
- **Examples**: ClickCLIAdapter, UrllibHTTPAdapter, FilesystemStorageAdapter

### Port Layer (Interface Contracts)
- **Purpose**: Define contracts between application and external systems
- **Contents**: Abstract interfaces and protocols
- **Dependencies**: None (pure interfaces)
- **Examples**: ContentFetcherPort, FileStoragePort, MarkdownGeneratorPort

## Data Flow

```
Input (JSON/URL) 
    ↓
CLI Adapter (Click framework)
    ↓
Use Case (Application layer)
    ↓
Domain Services (Pure logic)
    ↓
Storage Adapter (File operations)
    ↓
Output (Markdown + Assets)
```

## Key Design Decisions

### 1. Stdlib-Only Core
- **Domain and Application layers**: Use only Python standard library
- **Adapter layer**: May use third-party libraries (isolated via ports)
- **Plugin system**: Provides alternative adapter implementations

### 2. Deterministic Output
- **File naming**: Content-hash based for consistency
- **Metadata generation**: Sorted, stable ordering
- **Timestamp handling**: Timezone-aware, normalized format
- **Content processing**: Reproducible parsing and formatting

### 3. Security Boundaries
- **Input validation**: Performed at adapter entry points
- **Content sanitization**: Applied before domain processing
- **Path validation**: Prevent directory traversal attacks
- **Network safety**: URL validation, timeout enforcement

### 4. Plugin Architecture
- **Core operation**: Functions completely without plugins
- **Plugin activation**: Via `--use-plugins` CLI flag
- **Implementation**: Alternative adapters loaded at runtime
- **Isolation**: Plugins cannot affect core deterministic behavior

## Component Interactions

### JSON Conversion Flow
1. CLI adapter validates input file path
2. FileReader adapter loads and validates JSON content
3. ConversationParser (domain service) processes structure
4. MarkdownGenerator (domain service) creates output
5. FileWriter adapter saves deterministic result

### Website Conversion Flow
1. CLI adapter validates URL format
2. HTTPClient adapter fetches content (respects robots.txt)
3. HTMLParser adapter extracts main content
4. ImageDownloader adapter processes embedded images
5. ContentExtractor (domain service) structures data
6. MarkdownGenerator (domain service) creates output
7. FileWriter adapter saves result with assets

## Testing Strategy

### Unit Tests
- **Domain layer**: Pure logic testing with no external dependencies
- **Application layer**: Use case testing with mocked ports
- **Adapter layer**: Integration testing with real or mocked external systems

### Integration Tests
- **Full pipeline**: End-to-end conversion testing
- **Golden fixtures**: Deterministic output verification
- **Error scenarios**: Invalid inputs, network failures, malformed content

### Contract Tests
- **Port implementations**: Verify adapters conform to port contracts
- **Plugin compatibility**: Ensure plugin adapters work with core

## Security Architecture

### Input Validation
- **CLI level**: Argument validation and sanitization
- **Adapter level**: Format-specific validation (JSON schema, URL format)
- **Domain level**: Business rule validation

### Content Processing
- **HTML sanitization**: Remove dangerous elements and attributes
- **Path validation**: Prevent directory traversal in file operations
- **Network security**: Safe HTTP client configuration, timeout handling

### Output Safety
- **File permissions**: Secure file creation and access
- **Content encoding**: Proper character encoding handling
- **Asset validation**: Image format and size validation

## Performance Considerations

### Memory Management
- **Streaming processing**: Large files processed in chunks where possible
- **Lazy loading**: Content loaded only when needed
- **Resource cleanup**: Proper cleanup of network and file handles

### Optimization Points
- **HTTP caching**: Conditional requests and caching headers
- **Image processing**: Efficient handling of large image downloads
- **Content parsing**: Optimized parsing of large HTML documents

## Extension Points

### Current Plugin Support
- **Enhanced HTTP client**: requests library for better performance
- **Advanced HTML parsing**: BeautifulSoup for complex extraction
- **LLM integration**: OpenAI API for content enhancement
- **OCR capability**: Tesseract for image text extraction

### Future Extensions
- **Additional input formats**: Support for more conversation formats
- **Output formats**: Export to other formats beyond Markdown
- **Cloud storage**: Integration with cloud storage providers
- **Batch processing**: Multiple file processing workflows