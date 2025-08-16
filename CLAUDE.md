# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`conv2md` is a CLI tool that converts conversations, transcripts, and websites into clean, deterministic Markdown. It's designed to be dependency-free for the core functionality (stdlib only) with optional plugin support for enhancements.

## Architecture & Design Principles

### Core Design Philosophy
- **Stdlib-only core**: No third-party dependencies for core functionality
- **Deterministic output**: Identical results across runs
- **Plugin architecture**: Optional enhancements via `--use-plugins`
- **Clean separation**: Input detection → Processing → Markdown output

### Supported Input Types
1. **JSON Conversations**: Chat/conversation logs with speaker, timestamp, content
2. **Website/HTML**: Web pages with content extraction and image handling

### Key Output Features
- YAML front matter with metadata
- Deterministic code block handling (extends fence length for nested backticks)
- Asset management (images saved to `assets/` directory)
- Structured filenames based on content type and date

## Development Commands

### Setup & Installation
```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests (project uses unittest, not pytest)
python -m unittest discover tests/

# Run specific test
python -m unittest tests.test_filename

# Run with verbose output
python -m unittest discover tests/ -v
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Check formatting without changes
black --check src/ tests/
```

### Running the CLI
```bash
# Via entry point (after installation)
conv2md --input <file|url> --out ./output

# Direct module execution
python -m conv2md.cli --input <file|url>

# Development testing
python src/conv2md/cli.py --help
```

## Project Structure

```
src/conv2md/           # Main package
├── __init__.py        # Package version
├── cli.py             # CLI interface (argparse-based)
├── converters/        # Input type handlers (when implemented)
├── markdown/          # Markdown generation logic
└── plugins/           # Optional plugin system

tests/                 # Test suite with golden fixtures
docs/features/         # Feature specifications and requirements
```

## Development Guidelines

### Testing Strategy
- Use unittest with golden fixtures for deterministic output testing
- Test conversation parsing, HTML extraction, and Markdown generation separately
- Verify identical output across multiple runs (critical for deterministic guarantee)
- Focus on edge cases: nested backticks in code, malformed HTML, timezone handling

### Code Organization
- Keep core functionality in stdlib-only modules
- Isolate plugin dependencies to prevent core contamination
- Use clear separation between input detection, processing, and output generation

### Key Technical Requirements
- Python 3.8+ compatibility (pyproject.toml specifies >=3.8)
- Deterministic Markdown output (same input produces identical results)
- Proper handling of code blocks with nested backticks (extends fence length automatically)
- Timezone-aware timestamp processing (default: America/Phoenix)
- Respectful web scraping (robots.txt compliance by default, `--ignore-robots` to override)
- Minimal dependencies: click for CLI, dev tools (pytest, black, flake8) only for development

## CLI Interface

### Core Arguments
- `--input <file|url>`: Input source (JSON conversation or website URL)
- `--out DIR`: Output directory (default: ./out)
- `--tz TIMEZONE`: Timezone for timestamps (default: America/Phoenix)
- `--embed-images [file|inline]`: Image handling strategy
- `--single-file`: Inline all assets into single Markdown file
- `--ignore-robots`: Bypass robots.txt restrictions

### Future Arguments (from spec)
- `--toc`: Generate table of contents
- `--use-plugins`: Enable optional plugin features