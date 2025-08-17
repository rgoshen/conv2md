# conv2md Operations Runbook

## Development Setup

### Prerequisites

- Python 3.13+
- Git
- Virtual environment tools

### Installation

```bash
# Clone repository
git clone <repository-url>
cd conv2md

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test categories
python -m unittest discover tests/unit/ -v
python -m unittest discover tests/integration/ -v
python -m unittest discover tests/contract/ -v

# Run with coverage (when configured)
# coverage run -m unittest discover
# coverage report
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/ --max-line-length=88

# Type checking (optional)
mypy src/conv2md/ --ignore-missing-imports
```

## Deployment

### Build Package

```bash
# Build distribution
python -m build

# Install locally
pip install -e .
```

### Testing Installation

```bash
# Verify CLI works
conv2md --help

# Test basic functionality
conv2md --input sample.json --out ./test-output
```

## Monitoring & Troubleshooting

### Common Issues

#### CLI Not Found

- Verify virtual environment is activated
- Ensure package is installed with `pip list | grep conv2md`
- Check entry points in pyproject.toml

#### Import Errors

- Verify all required dependencies are installed
- Check Python version compatibility
- Ensure package is installed in development mode

#### Test Failures

- Check if test fixtures are corrupted
- Verify mock data is current
- Run tests individually to isolate issues

### Logging

- Application logs include conversion steps and errors
- Debug mode available with verbose flags
- Error logs include stack traces for debugging

## Maintenance

### Regular Tasks

- Update dependencies quarterly
- Review and update documentation
- Run security scans
- Performance testing with large inputs

### Backup Procedures

- Source code managed in Git
- Test fixtures stored in repository
- Documentation versioned with code

## Security

### Security Considerations

- Input validation on all external data
- Safe handling of web content
- No execution of untrusted code
- Regular dependency updates for security fixes

### Incident Response

1. Identify and isolate the issue
2. Document the problem and impact
3. Implement immediate fixes
4. Conduct post-incident review
5. Update procedures to prevent recurrence
