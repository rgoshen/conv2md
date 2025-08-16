# conv2md Features & Requirements

## Overview
`conv2md` is a CLI tool that converts **conversations, transcripts, and websites** into clean, deterministic Markdown.  
It is designed to be dependency-free (stdlib only for the core) with optional plugin support for enhancements.

---

## Tech Stack (Core - Stdlib Only)
- **Language**: Python 3.13+
- **CLI**: argparse
- **Networking**: urllib.request, urllib.parse, http.client
- **HTML Parsing**: html.parser (custom wrapper)
- **Robots.txt**: urllib.robotparser
- **Dates/Time**: datetime, zoneinfo
- **Files/IO**: pathlib, hashlib, mimetypes
- **JSON**: json (custom conversation schema support)
- **Testing**: unittest (with golden fixtures)
- **Logging**: logging

> Plugins (optional) may use third-party libraries but are opt-in only.

---

## Core Features (P0 - MVP)

### CLI
- `--input <file|url>` → input source
- `--out DIR` → output directory (default: ./out)
- `--tz TIMEZONE` → timezone (default: America/Phoenix)
- `--embed-images [file|inline]` → store images as files or inline data URIs
- `--single-file` → inline assets into a single Markdown file
- `--ignore-robots` → bypass robots.txt restrictions

### Supported Input Types
1. **JSON Conversations**  
   - Minimal schema: `{ "participants": [...], "messages": [...] }`
   - Messages include: `speaker`, `timestamp`, `content` (text/code/image)
   - Output:
     - Speaker lines: `**Rick — 12:34**`
     - Code blocks as fenced Markdown
     - Date markers: `## YYYY-MM-DD`
     - Images saved under `assets/`
   - YAML front matter:
     ```yaml
     ---
     title: "Conversation — <YYYY-MM-DD>"
     source: "json"
     participants: ["Rick","Assistant"]
     message_count: <int>
     created_at: "<UTC ISO8601>"
     ---
     ```

2. **Website / HTML**
   - Fetch with urllib (retries, timeouts)
   - Respect robots.txt by default
   - Strip `<script>`, `<style>`
   - Heuristic content extraction (prefer <article>, <main>, longest text density)
   - Markdown rendering rules:
     - `<h1..h6>` → `#..######`
     - `<p>` → blank-line paragraphs
     - `<strong>/<b>` → `**bold**`
     - `<em>/<i>` → `_italic_`
     - `<a>` → `[text](url)`
     - Lists, blockquotes, HR supported
     - Tables: GFM if simple; raw HTML otherwise
   - Images:
     - Download to `assets/` with content-hash filenames
     - Inline if `--embed-images inline`
   - YAML front matter:
     ```yaml
     ---
     title: "<page title>"
     source: "url"
     url: "<original URL>"
     fetched_at: "<UTC ISO8601>"
     description: "<meta description>"
     ---
     ```

### Markdown Output Rules
- Deterministic output (identical across runs)
- Preserve code blocks exactly
- Extend fence length if code contains backticks
- Normalize line endings to `\n`

### Output Layout
- One `.md` file per run
- Assets stored under `assets/`
- Filenames:
  - Conversations: `Conversation-<YYYY-MM-DD>-<slug>.md`
  - Websites: `<domain>-<slug>-<YYYYMMDD>.md`

---

## Strong Should-Have (P1)
- TOC generation (`--toc`)
- Task list conversion (`- [ ]`)
- Mermaid passthrough
- Math passthrough (`$..$` / `$$..$$`)
- Slugify internal anchors
- Large input guardrails (warn >5MB HTML or >100 images)

---

## Optional Plugins (P2)
- Enabled with `--use-plugins`
- LLM-enhanced features:
  - Better titles
  - Summaries
  - Image alt-text
- OCR for images
- Third-party readability library for cleaner article extraction

---

## Roadmap

### Milestone 1: P0 (MVP)
- CLI & input detection
- JSON conversation → Markdown
- URL/HTML → Markdown + images
- Deterministic code block handling
- Front matter metadata
- unittest + golden fixtures

### Milestone 2: P1 (Enhancements)
- TOC, task lists, mermaid, math, anchors
- robots.txt handling & overrides
- Large input guardrails
- Expanded testing

### Milestone 3: P2 (Plugins)
- Plugin loader
- Optional LLM-assisted features
- OCR support
- Readability library integration

---

## Acceptance Tests
- **Conversations**: multi-day, timestamps, code fidelity
- **Websites**: image placement, link conversion, metadata extraction
- **Code blocks**: nested backticks, language preservation
- **Determinism**: identical outputs across runs
- **Robots**: blocked URLs handled clearly
