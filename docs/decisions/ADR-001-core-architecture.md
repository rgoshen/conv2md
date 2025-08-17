# ADR-001: Core Architecture Pattern

- **Date**: 2025-08-16

- **Status**: Proposed

## Context

conv2md is a CLI tool that converts conversations, transcripts, and websites into clean, deterministic Markdown. The core constraints and requirements are:

1. **Stdlib-only core**: Core functionality must use Python standard library only, with third-party dependencies isolated to optional plugins
2. **Deterministic output**: Same input must produce identical output across runs
3. **Plugin architecture**: Optional enhancements via `--use-plugins` flag without affecting core
4. **Security-first**: OWASP compliance, input validation, safe content processing
5. **Testability**: Support for TDD with unit, integration, and deterministic golden fixture tests
6. **Multiple input types**: JSON conversations and HTML/website content
7. **Cross-platform**: Windows, macOS, Linux compatibility

Key stakeholders include researchers, content archivists, and developers who need reliable Markdown conversion. The domain involves file I/O, network operations, content parsing, and format conversion.

## Decision

Adopt **Hexagonal Architecture (Ports & Adapters)** with Clean Architecture layering:

```
├── domain/          # Core business logic (stdlib only)
│   ├── entities/    # Conversation, Document, Image entities  
│   ├── value_objects/ # Timestamp, URL, ContentHash
│   └── services/    # Conversion orchestration
├── application/     # Use cases (stdlib only)
│   ├── use_cases/   # ConvertConversation, ConvertWebsite
│   └── interfaces/  # Port definitions
├── adapters/        # External integrations
│   ├── cli/         # Click CLI adapter
│   ├── http/        # urllib HTTP client adapter
│   ├── file_system/ # pathlib file operations adapter
│   └── html_parser/ # html.parser wrapper adapter
└── ports/           # Interface definitions
    ├── content/     # ContentParser, ContentFetcher
    ├── storage/     # FileWriter, ImageStorage  
    └── generation/  # MarkdownGenerator
```

## Rationale

**Why Hexagonal Architecture:**

1. **Dependency Isolation**: Core domain logic independent of external dependencies, supporting the stdlib-only requirement
2. **Plugin Support**: Adapters can be swapped (stdlib vs plugin implementations) without affecting core
3. **Testability**: Clear boundaries enable comprehensive mocking and golden fixture testing
4. **Security**: Input validation concentrated at adapter boundaries
5. **Determinism**: Core logic isolated from non-deterministic external operations

**Why Clean Architecture Layers:**

1. **Domain Layer**: Pure business logic using only stdlib, ensuring deterministic behavior
2. **Application Layer**: Use case orchestration, defining the "what" without "how"
3. **Adapter Layer**: External system integrations, where stdlib vs plugin choice happens
4. **Port Layer**: Interface contracts ensuring loose coupling

**Alignment with Project Priorities:**

- **Security**: Input validation at adapter boundaries, core isolation from external threats
- **Accessibility**: Clear error messages through adapter interfaces
- **Readability**: Domain logic separated from technical concerns
- **Maintainability**: SOLID principles enforced through layer boundaries
- **Modularity**: Plugin system via adapter substitution
- **Optimization**: Deferred until core functionality stable

## Consequences

### Positive

- **Clear boundaries**: Domain logic immune to external changes
- **Easier testing**: Each layer testable in isolation with well-defined interfaces
- **Plugin flexibility**: Stdlib and enhanced implementations can coexist
- **Deterministic core**: External I/O isolated from conversion logic
- **Security isolation**: Untrusted input processed only at adapter boundaries
- **TDD-friendly**: Interfaces enable test-first development

### Negative

- **Initial overhead**: More files and abstractions than simple script approach
- **Learning curve**: Team must understand hexagonal concepts
- **Potential over-engineering**: May be complex for current simple requirements

### Follow-ups

- **ADR-002**: Content parsing strategy (stdlib html.parser vs plugin alternatives)
- **ADR-003**: File storage and naming conventions for deterministic output
- **ADR-004**: Plugin loading and isolation mechanism
- **ADR-005**: Security boundary implementation and validation strategy

## Alternatives Considered

### Alternative A: Simple Script Architecture
- **Pros**: Minimal complexity, fast initial development
- **Cons**: Difficult to test, plugin system challenging, stdlib isolation hard to maintain
- **Rejected**: Conflicts with plugin requirements and testability needs

### Alternative B: Layered Architecture (Traditional N-Tier)
- **Pros**: Familiar pattern, simpler than hexagonal
- **Cons**: Dependencies flow down layers, harder to swap implementations, plugin system awkward
- **Rejected**: Plugin system requires dependency inversion that layered architecture discourages

### Alternative C: Event-Driven Architecture
- **Pros**: Highly decoupled, plugin system via event handlers
- **Cons**: Adds complexity for synchronous CLI tool, harder to debug, determinism challenges
- **Rejected**: Overkill for single-user CLI tool, determinism requirement conflicts with async nature

### Alternative D: Microservices
- **Pros**: Maximum modularity, separate deployment units
- **Cons**: Operational overhead, local tool doesn't need distribution, performance penalty
- **Rejected**: CLI tool needs single executable, not distributed system