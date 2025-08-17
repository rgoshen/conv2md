# Contributing Guidelines

Thanks for your interest in contributing! This document outlines the process and expectations for contributing to this project.

## Code of Conduct

All contributors are expected to follow the Code of Conduct (CODE_OF_CONDUCT.md) (if present) or maintain a respectful, constructive attitude.

## How to Contribute

### 1. Discuss Changes First

- For major features or changes, open an issue to discuss your idea before starting work.

- Link to any related issues, ADRs, or design docs.

### 2. Fork & Branch

- Fork the repo to your account.

- Create a feature branch:

    ```bash
    git checkout -b feature/<short-description>
    ```

### 3. Follow the Rules

- Review **RULES.md** for priorities, TDD workflow, and checklists.

- Follow the strict TDD cycle: failing test → minimal code → next failing test → refactor.

- Respect DRY, SOLID, and the project's architecture decisions.

### 4. Write Tests

- All code must have test coverage.

- Required: **unit** + **integration** tests; **end-to-end** where appropriate.

- For web apps, include **accessibility** tests.

### 5. Keep Tests Non-Brittle

- Avoid coupling to implementation details.

- Use stable selectors for UI tests.

- Keep tests deterministic and independent.

### 6. Commit Conventions

- Use clear, descriptive commit messages.

- One logical change per commit.

### 7. Pull Requests

- Ensure your branch is up-to-date with `main`.

- Run all linters, formatters, and tests before opening a PR.

- Fill out the Pull Request template (PULL_REQUEST_TEMPLATE.md) fully.

- Link related issues and ADRs in your PR description.

### 8. Documentation

- Update **README.md**, **RULES.md**, and relevant ADRs as needed.

- Add new ADRs for any significant technical decisions.

### 9. Code Review

- Be open to feedback.

- Respond to requested changes promptly.

- Keep discussions professional and constructive.

## Development Setup

1. Clone your fork:

    ```bash
    git clone <your-fork-url>
    cd <project-name>
    ```

2. Install dependencies:

    ```bash
    <package-manager> install
    ```

3. Copy `.env.example` to `.env` and fill in your local settings.

## Reporting Issues

- Search existing issues before opening a new one.

- Use the issue template, if available.

- Include steps to reproduce, expected vs actual behavior, and environment details.

---

Happy coding!
