# conv2md

[![CI Pipeline](https://github.com/rgoshen/conv2md/actions/workflows/ci.yml/badge.svg)](https://github.com/rgoshen/conv2md/actions/workflows/ci.yml)
[![Security Scanning](https://github.com/rgoshen/conv2md/actions/workflows/security.yml/badge.svg)](https://github.com/rgoshen/conv2md/actions/workflows/security.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**conv2md** is a command-line tool that converts **conversations, transcripts, and websites** into clean, deterministic Markdown files.
It preserves structure, code blocks, and assets while adding useful metadata for archival and note-taking.

---

## ✨ Features

- Convert **JSON conversations** (minimal schema or ChatGPT export-style) → Markdown
- Convert **websites/HTML** → Markdown
- Preserve:
  - Headings, paragraphs, lists, blockquotes, tables
  - Fenced code blocks (with correct language + backtick escaping)
  - Speaker/timestamps in conversations
- Download and link **images** into an `assets/` folder (or inline as data URIs)
- Add **YAML front matter** with metadata (title, source, participants, timestamps, counts)
- Deterministic output (identical across runs given the same input)

---

## 🚀 Philosophy

- **Stdlib only**: Core implementation avoids third-party libraries.
  - HTML parsing via `html.parser`
  - Networking via `urllib`
  - Time handling via `datetime` and `zoneinfo`
- **Reproducible**: Same input → same Markdown every time.
- **Pluggable**: Optional `--use-plugins` flag enables extra features (LLM summaries, OCR, readability libraries).

---

## 📂 Example Usage

Convert a ChatGPT-style export:

```bash
conv2md --input conversations.json --out ./out
```

Convert a website to Markdown (with images stored as files):

```bash
conv2md --input https://example.com/article --out ./out
```

Single-file Markdown with inline images:

```bash
conv2md --input https://example.com/article --out ./out --single-file
```

---

## 📦 Installation

### Requirements
- Python 3.13+
- Git (for development)

### Install from Source
```bash
# Clone the repository
git clone https://github.com/rgoshen/conv2md.git
cd conv2md

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
conv2md --help
```

### Install for Plugin Support
```bash
# Install with optional plugin dependencies
pip install -e ".[plugins]"
```

---

## ⚙️ CLI Options

- `--input <file|url>` → Input file or URL
- `--out DIR` → Output directory (default: `./out`)
- `--tz TIMEZONE` → Timezone for timestamps (default: `America/Phoenix`)
- `--embed-images [file|inline]` → Save images as files (default) or inline base64
- `--single-file` → Inline all assets into one Markdown file
- `--ignore-robots` → Ignore robots.txt restrictions
- `--use-plugins` → Enable optional plugin features

---

## 🛣️ Roadmap

### Milestone 1 (MVP)

- JSON → Markdown pipeline
- URL/HTML → Markdown + images
- Deterministic code block handling
- Front matter metadata
- `unittest` + golden fixtures

### Milestone 2 (Enhancements)

- TOC (`--toc`), task lists, mermaid, math passthrough
- Slugify anchors
- Large input guardrails
- robots.txt handling & overrides

### Milestone 3 (Plugins)

- Plugin loader
- LLM-assisted enhancements (titles, summaries, alt-text)
- OCR for images
- Optional readability library

---

## 🛠️ Development

### Setup Development Environment
```bash
# Clone and setup
git clone https://github.com/rgoshen/conv2md.git
cd conv2md

# Create virtual environment  
python -m venv .venv
source .venv/bin/activate

# Install with all dependencies
pip install -e ".[dev,plugins]"
```

### Running Tests
```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test types
python -m unittest discover tests/unit/ -v
python -m unittest discover tests/integration/ -v
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code  
flake8 src/ tests/

# Security scan
bandit -r src/
```

### Contributing
We follow strict TDD and security-first development. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

- Create feature branches from `main`
- Follow conventional commit format
- Ensure all CI checks pass
- Update documentation as needed

---

## 📜 License

MIT
