# README Template

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

- Follow **RULES.md** for priorities, TDD, and review checklists.

- This repo already includes a **Pull Request template**; please use it.

## License

<license here>
