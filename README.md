# conv2md

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

## ⚙️ CLI Options (planned)

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

## 📜 License

MIT
