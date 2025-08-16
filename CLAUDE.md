CLAUDE.md
Project-specific guidance for Claude Code when working with conv2md.

Note: Read CLAUDE_UNIVERSAL.md, CLAUDE_WORKFLOW.md, and CLAUDE_TEMPLATES.md first for universal principles that apply to all projects.

Python Best Practices & Standards
Always follow Python coding best practices and industry standards, including:

Code Style & Formatting
PEP 8: Python Style Guide compliance
Black formatter: Consistent code formatting (88 character line length)
Type hints: Use for all public interfaces and complex functions
Docstrings: Google or NumPy style for all modules, classes, and functions
Python-Specific Patterns
Virtual environments: Always use python -m venv .venv for development isolation
Context managers: Use with statements for resource management
Generators: Prefer generators over lists for large datasets (memory efficiency)
Pathlib: Use pathlib.Path instead of os.path for file operations
F-strings: Prefer f-strings over .format() or % formatting
Exception handling: Specific exceptions, not bare except:
Performance & Memory
Lazy evaluation: Use generators and iterators for large data processing
Memory profiling: Monitor memory usage for large file handling
Algorithmic complexity: Choose appropriate data structures (dict vs list for lookups)
Security (Python-Specific)
Input validation: Validate all external inputs before processing
Path sanitization: Prevent path traversal attacks in file operations
Safe parsing: Use safe YAML/JSON loading, avoid eval()
Subprocess security: Use subprocess safely, avoid shell injection
Testing Standards
unittest: Project standard (not pytest, per existing choice)
Mocking: Use unittest.mock for external dependencies
Fixtures: Golden fixtures for deterministic testing
Parametrized tests: Use subTest() for multiple test cases
python

# ✅ Good Python practices

from pathlib import Path
from typing import List, Dict, Optional
import logging

class ConversationConverter:
"""Convert conversations to Markdown format."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = Path(output_dir)
        self._logger = logging.getLogger(__name__)

    def convert(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to Markdown format.

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted Markdown string

        Raises:
            ValueError: If messages format is invalid
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        # Use generator for memory efficiency
        markdown_lines = (
            self._format_message(msg) for msg in messages
        )

        return '\n'.join(markdown_lines)

Project Overview
conv2md is a CLI tool that converts conversations, transcripts, and websites into clean, deterministic Markdown. The project emphasizes minimal dependencies and reproducible output.

Core Architecture Principles (Project-Specific)

1. Stdlib-Only Core Philosophy
   Core functionality uses Python stdlib only: No third-party dependencies for parsing, networking, or file operations
   HTML parsing: html.parser (custom wrapper class)
   Networking: urllib.request, urllib.parse, http.client
   Time handling: datetime, zoneinfo
   File operations: pathlib, hashlib, mimetypes
2. Plugin Architecture for Dependencies
   Third-party libraries allowed ONLY in plugins
   Plugins activated via --use-plugins flag
   Core must function without any plugins
   Plugin isolation: Plugins cannot contaminate core functionality
   python

# ✅ Correct: Core uses stdlib only

import html.parser
import urllib.request
from pathlib import Path

# ❌ Incorrect: Core using third-party libs

import requests # Only allowed in plugins
import beautifulsoup4 # Only allowed in plugins 3. Deterministic Output Guarantee
Same input → identical output every time
Critical for: Code block handling, image naming, metadata generation
Testing strategy: Golden fixtures to verify determinism
Special handling: Nested backticks in code blocks (extends fence length)
Project Structure & Adaptations
Directory Organization
src/conv2md/ # Main package (stdlib only)
├── **init**.py # Package version
├── cli.py # CLI interface (argparse-based)
├── converters/ # Input type handlers
│ ├── **init**.py
│ ├── json_conv.py # JSON conversation parsing
│ └── html_conv.py # HTML/website parsing
├── markdown/ # Markdown generation logic
│ ├── **init**.py
│ ├── generator.py # Core Markdown generation
│ └── blocks.py # Code block handling
└── plugins/ # Optional plugin system
├── **init**.py
├── loader.py # Plugin discovery/loading
└── contrib/ # Built-in plugins
├── llm_enhance.py
└── readability.py

tests/ # Test suite with golden fixtures
├── unit/ # Unit tests (stdlib components)
├── integration/ # Integration tests (full pipeline)
├── fixtures/ # Golden fixtures for determinism
│ ├── conversations/
│ ├── websites/
│ └── expected/ # Expected outputs
└── plugins/ # Plugin-specific tests
Dependency Management Adaptations
Core Dependencies (Allowed)
python

# pyproject.toml [project.dependencies]

# ONLY these core dependencies allowed:

dependencies = [
"click>=8.0.0", # CLI framework only
]
Plugin Dependencies (Isolated)
python

# pyproject.toml [project.optional-dependencies]

plugins = [
"requests>=2.28.0", # HTTP client for plugins
"beautifulsoup4>=4.11.0", # HTML parsing for plugins
"openai>=1.0.0", # LLM integration
"pytesseract>=0.3.10", # OCR functionality
]
Adapter Pattern Implementation
python

# src/conv2md/adapters/http_adapter.py (when implemented)

class HttpAdapter:
"""Adapter for HTTP operations - stdlib only"""
def **init**(self): # Use urllib only, no requests
pass

# src/conv2md/plugins/adapters/enhanced_http.py

class EnhancedHttpAdapter:
"""Plugin adapter using requests library"""
def **init**(self):
import requests # Only imported in plugins
self.session = requests.Session()
CLI-Specific Design Patterns
Argument Design Principles
Intuitive naming: Use clear, descriptive argument names
Consistent patterns: Follow Unix conventions (short -h, long --help)
Sensible defaults: Minimize required arguments where possible
Validation: Validate arguments early with clear error messages
User Experience Patterns
python

# ✅ Good CLI patterns

def validate_input_source(input_path: str) -> Path:
"""Validate and resolve input path with helpful errors."""
path = Path(input_path)

    if input_path.startswith(('http://', 'https://')):
        return input_path  # URL - validate separately

    if not path.exists():
        raise click.ClickException(
            f"Input file not found: {input_path}\n"
            f"Please check the path and try again."
        )

    if not path.is_file():
        raise click.ClickException(
            f"Input must be a file, not directory: {input_path}"
        )

    return path

Progress & Feedback Patterns
python

# For long-running operations

def show_progress(operation: str, items: List[Any]) -> None:
"""Show progress for batch operations."""
with click.progressbar(
items,
label=f"{operation}...",
show_eta=True,
show_percent=True
) as progress_items:
for item in progress_items:
process_item(item)

# For status updates

def status_message(message: str, success: bool = True) -> None:
"""Display status with appropriate styling."""
if success:
click.secho(f"✓ {message}", fg='green')
else:
click.secho(f"✗ {message}", fg='red')
Error Handling Patterns
python

# ✅ User-friendly error messages

def handle_conversion_error(error: Exception, input_source: str) -> None:
"""Convert technical errors to user-friendly messages."""
if isinstance(error, json.JSONDecodeError):
click.echo(f"Error: Invalid JSON in {input_source}")
click.echo(f"Line {error.lineno}: {error.msg}")
click.echo("Please check the JSON format and try again.")

    elif isinstance(error, urllib.error.URLError):
        click.echo(f"Error: Could not access {input_source}")
        click.echo("Please check the URL and your internet connection.")

    else:
        click.echo(f"Unexpected error: {error}")
        click.echo("Please report this issue with the above error message.")

Configuration Patterns
python

# Support multiple config sources

def load_configuration() -> Dict[str, Any]:
"""Load config from file, environment, and CLI args."""
config = {}

    # 1. Default values
    config.update(DEFAULT_CONFIG)

    # 2. Config file (if exists)
    config_file = Path.home() / '.conv2md' / 'config.json'
    if config_file.exists():
        with open(config_file) as f:
            config.update(json.load(f))

    # 3. Environment variables
    for key in config:
        env_key = f"CONV2MD_{key.upper()}"
        if env_value := os.getenv(env_key):
            config[key] = env_value

    # 4. CLI arguments override everything
    return config

Output Management Patterns
python

# Structured output with proper paths

def ensure_output_structure(output_dir: Path) -> None:
"""Create output directory structure."""
output_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (output_dir / 'assets').mkdir(exist_ok=True)

    # Validate write permissions
    try:
        test_file = output_dir / '.write_test'
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        raise click.ClickException(
            f"Cannot write to output directory: {output_dir}"
        )

# Safe file naming

def safe_filename(title: str, max_length: int = 100) -> str:
"""Generate filesystem-safe filenames.""" # Remove/replace unsafe characters
safe = re.sub(r'[<>:"/\\|?*]', '-', title)

    # Limit length while preserving extension
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[:max_length-len(ext)] + ext

    return safe

Cross-Platform Considerations
python

# Handle platform differences

def get_config_dir() -> Path:
"""Get platform-appropriate config directory."""
if os.name == 'nt': # Windows
return Path(os.environ['APPDATA']) / 'conv2md'
else: # Unix-like
return Path.home() / '.conv2md'

def open_file_with_default_app(file_path: Path) -> None:
"""Open file with OS default application."""
import subprocess
import sys

    if sys.platform == 'darwin':  # macOS
        subprocess.run(['open', file_path])
    elif sys.platform == 'win32':  # Windows
        os.startfile(file_path)
    else:  # Linux
        subprocess.run(['xdg-open', file_path])

Testing CLI Patterns
python
class TestCLIInterface(unittest.TestCase):
def setUp(self):
self.runner = CliRunner()
self.temp_dir = Path(tempfile.mkdtemp())

    def test_help_message(self):
        """Test help message is informative."""
        result = self.runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('conv2md', result.output)
        self.assertIn('Convert conversations', result.output)

    def test_invalid_input_handling(self):
        """Test graceful handling of invalid inputs."""
        result = self.runner.invoke(cli, [
            '--input', 'nonexistent.json',
            '--out', str(self.temp_dir)
        ])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('not found', result.output)
        self.assertNotIn('Traceback', result.output)  # No stack traces

    def test_output_directory_creation(self):
        """Test output directory is created if missing."""
        output_dir = self.temp_dir / 'new_output'
        result = self.runner.invoke(cli, [
            '--input', 'valid_input.json',
            '--out', str(output_dir)
        ])
        self.assertTrue(output_dir.exists())

Logging for CLI Applications
python
def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
"""Configure appropriate logging for CLI usage."""
if quiet:
level = logging.ERROR
elif verbose:
level = logging.DEBUG
else:
level = logging.INFO

    # CLI-friendly format (no timestamps for user-facing logs)
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('conv2md')
    logger.addHandler(handler)
    logger.setLevel(level)

Development Commands & Testing
Setup & Installation
Virtual Environment (Required)
bash

# Create virtual environment

python -m venv .venv

# Activate virtual environment

# On Unix/macOS:

source .venv/bin/activate

# On Windows:

.venv\Scripts\activate

# Upgrade pip

python -m pip install --upgrade pip
Installation Options
bash

# Core installation (stdlib only)

pip install -e .

# With plugin dependencies

pip install -e ".[plugins]"

# Development dependencies (includes testing, linting, formatting)

pip install -e ".[dev,plugins]"
Environment Verification
bash

# Verify correct Python environment

which python # Should show .venv/bin/python
python --version # Should show Python 3.13+

# Verify installation

conv2md --help
Testing Strategy (TDD Adaptations)

1. Core Testing (Stdlib Only)
   bash

# Run core tests (no plugin dependencies)

python -m unittest discover tests/unit/ -v

# Test specific core module

python -m unittest tests.unit.test_json_converter -v 2. Determinism Testing (Critical)
bash

# Golden fixture tests - verify identical output

python -m unittest tests.integration.test_determinism -v

# Manual determinism check

conv2md --input tests/fixtures/sample.json --out /tmp/run1
conv2md --input tests/fixtures/sample.json --out /tmp/run2
diff -r /tmp/run1 /tmp/run2 # Should be identical 3. Plugin Testing (Isolated)
bash

# Plugin tests (requires plugin dependencies)

python -m unittest discover tests/contract/ -v

# Test core functionality without plugins

conv2md --input sample.json --out ./out

# vs with plugins

conv2md --input sample.json --out ./out --use-plugins
Code Quality (Project-Specific)
bash

# Format code (stdlib and plugins)

black src/ tests/

# Lint with project-specific rules

flake8 src/ tests/ --max-line-length=88

# Type checking (optional but recommended)

mypy src/conv2md/ --ignore-missing-imports
TDD Workflow Adaptations

1. Core Functionality TDD
   python

# ✅ Correct TDD approach for core

class TestJSONConverter(unittest.TestCase):
def test_parse_conversation_minimal_schema(self): # Red: Write failing test first
input_json = '{"messages": [{"speaker": "User", "content": "Hello"}]}'
converter = JSONConverter()

        # This should fail initially
        result = converter.parse(input_json)
        self.assertEqual(len(result.messages), 1)

    # Then: Write minimal code to pass
    # Then: Refactor safely

2.  Determinism TDD
    python
    class TestDeterministicOutput(unittest.TestCase):
    def test_identical_markdown_across_runs(self): # Red: Test determinism requirement
    input_file = "tests/fixtures/sample_conversation.json"

            # Run conversion twice
            result1 = convert_to_markdown(input_file)
            result2 = convert_to_markdown(input_file)

            # Must be byte-for-byte identical
            self.assertEqual(result1, result2)

3.  Plugin Integration TDD
    python
    class TestPluginIntegration(unittest.TestCase):
    def test_core_works_without_plugins(self): # Red: Ensure core never depends on plugins
    converter = CoreConverter() # No plugin dependencies
    result = converter.convert(sample_input)
    self.assertIsNotNone(result)

        @unittest.skipUnless(PLUGINS_AVAILABLE, "Plugins not installed")
        def test_plugins_enhance_output(self):
            # Test plugin enhancements separately
            pass

    Security Adaptations (OWASP for CLI)
    Input Validation (A03 - Injection)
    python

# TDD approach for input validation

def test_malicious_json_input(self):
malicious_input = '{"messages": [{"content": "<script>alert(\\"xss\\")</script>"}]}'
result = converter.parse(malicious_input) # Ensure no script execution, proper escaping
self.assertNotIn("<script>", result.markdown)
File System Security (A01 - Access Control)
python
def test_path_traversal_prevention(self): # Test prevention of ../../../etc/passwd type attacks
malicious_path = "../../../etc/passwd"
with self.assertRaises(SecurityError):
converter.save_to_file(malicious_path)
Web Scraping Security
Robots.txt compliance by default (respectful scraping)
--ignore-robots flag for override (explicit user choice)
URL validation to prevent SSRF attacks
Content type verification before processing
Performance & Quality Gates (Project-Specific)
Determinism Quality Gate
bash

# CI must verify deterministic output

./scripts/test_determinism.sh

# Script runs same input multiple times, diffs output

Memory Usage (Large File Handling)
python
def test_large_file_memory_usage(self): # Ensure streaming for large inputs
large_input = generate_large_conversation(messages=10000)
initial_memory = get_memory_usage()

    converter.convert(large_input)

    final_memory = get_memory_usage()
    memory_growth = final_memory - initial_memory
    self.assertLess(memory_growth, MAX_MEMORY_GROWTH)

CLI-Specific Testing Patterns
Argument Parsing Tests
python
class TestCLIArguments(unittest.TestCase):
def test_input_validation(self): # Test all CLI argument combinations
with self.assertRaises(SystemExit):
main(["--input", "nonexistent.json"])

    def test_plugin_flag_isolation(self):
        # Ensure --use-plugins doesn't affect core
        args_core = parse_args(["--input", "test.json"])
        args_plugins = parse_args(["--input", "test.json", "--use-plugins"])

        # Core functionality identical regardless
        self.assertEqual(args_core.input, args_plugins.input)

Output Format Tests
python
def test_yaml_frontmatter_format(self):
result = converter.convert(sample_conversation)
lines = result.split('\n')

    # Verify YAML frontmatter structure
    self.assertEqual(lines[0], '---')
    self.assertIn('title:', lines[1])
    self.assertIn('source:', lines[2])

Documentation Adaptations
README.md Adaptations
Philosophy section: Emphasize stdlib-only and deterministic output
Installation: Core vs plugin installation options
Usage examples: Show plugin flag usage
ADR Considerations
ADR-001: Stdlib-only core decision
ADR-002: Plugin architecture design
ADR-003: Deterministic output approach
ADR-004: HTML parsing strategy (stdlib vs plugins)
Plugin Development Guidelines
Plugin Interface (When Implemented)
python
class PluginInterface:
def enhance_markdown(self, markdown: str, metadata: dict) -> str:
"""Enhance generated markdown"""
raise NotImplementedError

    def extract_content(self, html: str) -> str:
        """Enhanced content extraction"""
        raise NotImplementedError

Plugin Registration
python

# plugins/contrib/example_plugin.py

@register_plugin("example")
class ExamplePlugin(PluginInterface):
def enhance_markdown(self, markdown: str, metadata: dict) -> str: # Plugin enhancement logic
return enhanced_markdown
This project-specific guidance works alongside the universal principles to ensure conv2md maintains its core philosophy while following consistent development practices.
