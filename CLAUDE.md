# Coding Agent – Universal Rules (Project/Language Agnostic)

## Mission
Ship secure, maintainable, human-readable software via **strict TDD**, **OWASP-aligned security**, **DRY/SOLID**, minimal dependencies, and excellent docs. Don’t start the next task without approval.

## Repo Layout (authoritative)
```
README.md
CONTRIBUTING.md
LICENSE
todo.md                     # lives at repo root
summary/                    # daily development summaries
  YYYY-MM-DD-development-summary.md
docs/                       # everything else goes under docs/
  requirements/requirements.md
  decisions/ADR-{{id}}-{{kebab-title}}.md
  security/
    asvs-matrix.md
    threat-models/{{feature}}.md
    dep-policy.md
    secrets-and-key-management.md
  architecture/
    overview.md
    context.mmd
    containers.mmd
    components.mmd
    sequences/{{feature}}.mmd
  runbook.md
  changelog_rules.md
.github/
  ISSUE_TEMPLATE.md
src/
  {{language}}/
    domain/
    application/
    adapters/
    ports/
tests/
  unit/
  integration/
  contract/
```

---

## Global Principles
- **TDD only:** Red → Green → Refactor. No production code without a failing test first.  
- **OWASP first:** Meet or exceed **OWASP ASVS** controls, **OWASP Top 10** risks, and supply-chain hygiene.  
- **Maintainability:** Small units, clear names, cohesive modules, comments that explain **what/why**.  
- **DRY & SOLID:** Prefer composition; isolate responsibilities; avoid repetition.  
- **Right DS & Algo:** Choose structures/algorithms with measured impact (time/space tradeoffs).  
- **Minimal deps:** Add a 3rd-party lib only with justification; always wrap via adapters/ports.  
- **Docs-as-code:** All requirements, decisions, security, and ops live in `docs/`.  
- **Do not auto-advance:** Wait for explicit approval before starting the next task.  

---

## Operating Mode

### 1) Requirements
- Gather all **functional** and **non-functional** requirements.  
- Normalize and store in `docs/requirements/requirements.md` (single source of truth).  
- Derive an **ordered task list** with estimates & dependencies.  
- Keep **`todo.md`** at the repo root up to date (checked items = done).  

### 2) Architecture (per project type)
- Propose the architecture style (e.g., **Hexagonal**, **Layered**, **CQRS**, **Event-Driven**, **Serverless**), with rationale.  
- Generate diagrams as code (Mermaid or equivalent).  
- Store in `docs/architecture/`.  
- Keep diagrams updated when structure changes.  

### 3) Security (OWASP)
- **ASVS mapping:** Maintain `docs/security/asvs-matrix.md`.  
- **Top 10 alignment:** Mitigate A01–A10 in code/tests/docs.  
- **Threat modeling:** Per feature in `docs/security/threat-models/{{feature}}.md`.  
- **Secrets & keys:** Document handling in `docs/security/secrets-and-key-management.md`.  
- **Supply chain:** Pin versions, verify integrity, license allowlist in `docs/security/dep-policy.md`.  
- **Evidence:** Link SAST, dependency, secret, and IaC scans in PRs.  

### 4) Strict TDD Loop (per task)
1. Write/extend a **failing** test.  
2. Write minimal code to pass.  
3. Refactor safely with tests green.  
4. Enforce thresholds: Coverage ≥ `{{COVERAGE_THRESHOLD}}`%, Mutation ≥ `{{MUTATION_THRESHOLD}}`%.  

### 5) Third-Party Libraries
- Require an **ADR** for any new dependency.  
- Wrap libraries in `src/{{language}}/adapters/`.  
- Expose interfaces via `src/{{language}}/ports/`.  
- Prevent direct imports outside adapters.  

### 6) Documentation
- **Requirements:** `docs/requirements/requirements.md`.  
- **ADR(s):** `docs/decisions/ADR-{{id}}-{{title}}.md`.  
- **Runbook:** `docs/runbook.md`.  
- **Changelog Rules:** `docs/changelog_rules.md`.  
- **Security:** ASVS matrix, threat models, secrets, dep policy.  
- **Architecture:** Overview & diagrams.  

### 7) Daily Development Summary
- In `summary/`, append or create `YYYY-MM-DD-development-summary.md`.  
- Include: **what was done** and **why**, risks, follow-ups, ADR/PR/test links.  

---

## Repository Hygiene
- Ensure root contains: `README.md`, `CONTRIBUTING.md`, `LICENSE`.  
- If missing, create using below templates:

### README Template

````markdown
# [Application Name]

One-paragraph summary of purpose and scope. State the problem, the audience, and the measurable outcome. Keep it human-friendly.

## Architecture

- **Pattern**: <layered | hexagonal | serverless | etc.> and rationale (tie to priorities).

- **Key Modules/Boundaries**: Domain, Application, Infrastructure.

- **Data Flow**: (Mermaid or link to diagram)

```text
flowchart LR
  UI[UI/Client] --> API[Application Service]
  API --> DOMAIN[Domain]
  API --> ADAPTERS[Adapters: DB, HTTP, Queue]
  ADAPTERS --> DB[(Database)]
  ADAPTERS --> EXT[External APIs]
```

- **ADR Index**:

    - ADR-000: Initial architecture (see `docs/adr/ADR-000-initial-architecture.md`)

    - ADR-00X: <decision>

## Getting Started

### Prerequisites

- <language/runtime version>

- <database/broker> (if any)

### Configuration

- Copy `.env.example` to `.env` and fill in values (no secrets committed).

### Setup

```bash
# Install
<package-manager> install
# Run (dev)
<command>
# Run (prod-ish)
<command>
```

### Testing (TDD-friendly)

```bash
# Watch mode for fast TDD cycles
<test-runner> --watch
# Full test suite (CI equivalent)
<test-runner> --ci
```

- Tests live alongside code in `__tests__` or `*.spec.*` files.

- Write a failing test for each checklist item in the Task List, then implement.

## Task List (Example Template)

```text
# Feature: <name>
- [ ] Behavior: <user-visible or API contract>
- [ ] Error/edge case: <describe>
- [ ] Boundary: <adapter or integration change>
- [ ] Observability: <log/metric/trace>
- [ ] A11y & Security: <keyboard/aria/validation/authZ>
Definition of Done:
- [ ] Tests green; TDD loop used
- [ ] No duplication; SOLID respected
- [ ] Docs updated; ADR added if needed
```

## Security

- Threats considered: <list> and mitigations chosen.

- Secrets via environment or managed secret store.

- AuthN/Z approach summary; least privilege by default.

## Accessibility (if UI)

- Semantics, keyboard support, focus management.

- Contrast and reduced-motion considerations.

- Known limitations and backlog items.

## Operations

- Logging & metrics (what/where).

- Environments & configuration strategy.

- Deployment notes (commands, pipelines).

## Contributing

- See the [CONTRIBUTING](CONTRIBUTING.md) documentation.

- This repo already includes a **Pull Request template**; please use it.

## License

[MIT](LICENSE.md)
````

---

### CONTRIBUTING Template

````markdown
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
````

---

### LICENSE Template

```markdown
MIT License

Copyright (c) 2025 Rick Goshen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

- Keep `README.md` (overview/setup/usage) and `CONTRIBUTING.md` (workflow, branching, review rules) up to date.  

---

## Branching, Commits, & Pull Requests

---

## CI/CD Rules
- Place CI config in `.github/workflows/` (or equivalent).
- Required jobs:
  - Lint/format
  - Tests with coverage/mutation thresholds
  - SAST, secrets, dependency, IaC scans
  - SBOM generation
- Branch protection: `main` and `develop` require PR + reviews + green CI.

---

## Versioning & Release Management
- Follow **SemVer** (major.minor.patch).
- Tag releases as `vX.Y.Z`.
- Auto-generate changelog from commits/PRs using rules in `docs/changelog_rules.md`.

---

## Observability & Monitoring
- Logs must be structured (JSON or key/value).
- Sensitive data must be redacted.
- Metrics/traces must follow standard format (`{{OBSERVABILITY_TOOL}}`).


- **Branching:** One branch per requirement: `feature/{{requirement-title-kebab}}`.  
- **Commits:**  
  - Commit after each task, updating: `todo.md`, daily summary, code docs.  
  - Use **Conventional Commits**.  
- **Pull Requests (PRs):**  
  - Open **one PR per requirement branch only** when:  
    - All tasks under the requirement are complete.  
    - Docs, ADRs, diagrams, and security notes are current.  
    - Tests/scans meet thresholds.  
    - Daily development summary is finalized.  
  - Use template ([PR Template](#pr-template)).  
  - PR must be **approved** (`APPROVED` via `{{APPROVAL_MECHANISM}}`).  
  - Next requirement starts only after merge/approval.  

---

## CI/CD Rules
- Place CI config in `.github/workflows/` (or equivalent).  
- Required jobs:  
  - Lint/format  
  - Tests with coverage/mutation thresholds  
  - SAST, secrets, dependency, IaC scans  
  - SBOM generation  
- Branch protection: `main` and `develop` require PR + reviews + green CI.  

---

## Versioning & Release Management
- Follow **SemVer** (major.minor.patch).  
- Tag releases as `vX.Y.Z`.  
- Auto-generate changelog from commits/PRs using rules in `docs/changelog_rules.md`.  

---

## Observability & Monitoring
- Logs must be structured (JSON or key/value).  
- Sensitive data must be redacted.  
- Metrics/traces must follow standard format (`{{OBSERVABILITY_TOOL}}`).  

---

## Backup & Disaster Recovery (Optional, if data-bearing)
- Document RPO/RTO in `docs/runbook.md`.  
- Include backup and restore steps.  

---

## Internationalization & Accessibility (Optional, if user-facing)
- Follow i18n/l10n standards (`{{I18N_TOOL}}`).  
- Meet **WCAG 2.1 AA** accessibility baseline.  

---

## Compliance / Licensing
- Dependencies must respect a defined license allowlist (MIT, Apache 2.0, etc.).  
- Check and document in `docs/security/dep-policy.md`.  

---

## Environment Parity
- Config via environment variables or secrets management (`{{CONFIG_MECHANISM}}`).  
- No environment-specific hacks in code.  

---

## Quality Gates (fail build if not met)

---

## Backup & Disaster Recovery (Optional, if data-bearing)
- Document RPO/RTO in `docs/runbook.md`.
- Include backup and restore steps.

---

## Internationalization & Accessibility (Optional, if user-facing)
- Follow i18n/l10n standards (`{{I18N_TOOL}}`).
- Meet **WCAG 2.1 AA** accessibility baseline.

---

## Compliance / Licensing
- Dependencies must respect a defined license allowlist (MIT, Apache 2.0, etc.).
- Check and document in `docs/security/dep-policy.md`.

---

## Environment Parity
- Config via environment variables or secrets management (`{{CONFIG_MECHANISM}}`).
- No environment-specific hacks in code.


- Format & lint clean (`{{FORMAT_CMD}}`, `{{LINTER_CMD}}`).  
- Tests with coverage ≥ `{{COVERAGE_THRESHOLD}}`%.  
- Mutation ≥ `{{MUTATION_THRESHOLD}}`%.  
- SAST, secrets, dep, and IaC scans green.  
- SBOM generated (`{{SBOM_CMD}}`).  
- Docs/ADRs/architecture updated.  
- ASVS matrix updated.  

---

## Templates

### PR Template

````markdown
# Pull Request

## Description
<!-- Provide a brief description of the changes in this PR -->

## Type of Change
<!-- Mark the relevant option with an "x" -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test improvements

## Changes Made
<!-- List the specific changes made in this PR -->
-
-
-

## Testing
<!-- Describe how you tested these changes -->
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Security validation performed

## Security Considerations
<!-- For CS-305 checksum verification system -->
- [ ] Only secure cryptographic algorithms used (SHA-256, SHA-3-256, SHA-512, SHA-3-512)
- [ ] No deprecated algorithms (MD5, SHA-1) introduced
- [ ] Input validation implemented
- [ ] Error handling doesn't expose sensitive information
- [ ] SSL/TLS configuration maintained

## Checklist
<!-- Mark completed items with an "x" -->
- [ ] Code follows project coding standards
- [ ] Self-review of code completed
- [ ] Code is properly commented
- [ ] Tests added/updated for new functionality
- [ ] Documentation updated if necessary
- [ ] No merge conflicts
- [ ] All CI checks pass

## Related Issues
<!-- Link any related issues -->
Closes #
Relates to #

## Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## Additional Notes
<!-- Any additional information that reviewers should know -->
````

---

### ADR Template

````markdown
# ADR-XXX: [ADR Title]

- **Date**: YYYY-MM-DD

- **Status**: Proposed

## Context

Summarize the problem, constraints, stakeholders, and the domain assumptions. Link to the initial requirements/user stories and any external constraints (e.g., compliance, hosting, data residency).

## Decision

Select the initial architecture pattern (e.g., layered, hexagonal/ports-and-adapters, serverless, modular monolith) and justify why it best satisfies the current requirements while honoring the repo priorities (Security → Accessibility → Readability → Maintainability → Modularity → Optimization).

## Rationale

Explain trade-offs and why alternatives were not chosen (e.g., microservices deferred to avoid operational overhead; specific framework chosen for ecosystem/security support). Reference DRY/SOLID and task-driven TDD implications on structure.

## Consequences

- **Positive**: <e.g., clear boundaries, easier testing, simpler deploys>

- **Negative**: <e.g., initial limitations, migration paths>

- **Follow-ups**: List next ADRs you expect (datastore choice, auth strategy, messaging, observability).

## Alternatives Considered

- Alternative A — pros/cons

- Alternative B — pros/cons
````

---
 
### ISSUES Template

````markdown
# Issue Template

## Issue Type
- [ ] Bug Report  
- [ ] Feature Request  
- [ ] Documentation Update  
- [ ] Security Concern  
- [ ] Other (please describe)  

---

## Summary
<!-- A clear and concise description of the issue. -->

---

## Steps to Reproduce (for bugs)
1.  
2.  
3.  
**Expected behavior:**  
**Actual behavior:**  

---

## Requirement Link (if applicable)
<!-- Reference the requirement ID or docs/requirements entry this ties to. -->

---

## Additional Context
<!-- Add any logs, screenshots, or additional details here. -->

---

## Checklist
- [ ] Linked to requirement or ADR (if applicable)  
- [ ] Added/updated tests (if needed)  
- [ ] Updated docs/summary (if needed)  
- [ ] Security/OWASP considerations reviewed  
````

---

## Definition of Done (checklist)
- [ ] Requirement slice complete; tests green locally & CI  
- [ ] Coverage/mutation thresholds met  
- [ ] Lint/format clean  
- [ ] Security scans green & ASVS updated  
- [ ] ADR/diagrams/docs updated  
- [ ] `todo.md` and summary updated  
- [ ] PR opened, reviewed, and approved  
