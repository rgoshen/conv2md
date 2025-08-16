# CLAUDE_UNIVERSAL.md

Universal guidance for Claude Code across all projects. These principles apply regardless of language, framework, or architecture.

## Mission

Ship secure, maintainable, human-readable software via **strict TDD**, **OWASP-aligned security**, **DRY/SOLID principles**, minimal dependencies, and excellent documentation. **Wait for explicit approval ("approved") from the user before starting the next task.**

---

## Core Principles

### 1. Test-Driven Development (TDD) Only

- **Red → Green → Refactor cycle**: No production code without a failing test first
- Write the minimal code to make tests pass
- Refactor safely with tests green
- Maintain coverage ≥ configured threshold
- Mutation testing ≥ configured threshold

### 2. Security First (OWASP Alignment)

- Meet or exceed **OWASP ASVS** controls
- Mitigate **OWASP Top 10** risks (A01-A10)
- Maintain ASVS mapping in `docs/security/asvs-matrix.md`
- Create threat models per feature in `docs/security/threat-models/{feature}.md`
- Document secrets & key management in `docs/security/secrets-and-key-management.md`
- Supply chain security: pin versions, verify integrity, maintain license allowlist

### 3. Maintainability

- Small, cohesive units with clear responsibilities
- Clear naming conventions
- Comments explain **what/why**, not how
- Minimal cognitive load

### 4. Design Principles

- **DRY (Don't Repeat Yourself)**: Eliminate duplication
- **SOLID principles**: Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- Prefer composition over inheritance
- Choose appropriate data structures and algorithms

### 5. Dependency Management

- **Minimal dependencies**: Only add third-party libraries with clear justification
- **Adapter pattern**: Wrap external libraries via adapters/ports
- Prevent direct imports of third-party code outside adapters
- Document all dependencies in ADRs

### 6. Documentation as Code

- All requirements, decisions, security, and operations documentation lives in `docs/`
- Keep documentation current with code changes
- Use Architecture Decision Records (ADRs) for significant technical decisions

---

## Repository Structure (Authoritative)

```
README.md
CONTRIBUTING.md
LICENSE
todo.md                     # lives at repo root
summary/                    # daily development summaries
  YYYY-MM-DD-development-summary.md
docs/                       # everything else goes under docs/
  requirements/requirements.md
  decisions/ADR-{id}-{kebab-title}.md
  security/
    asvs-matrix.md
    threat-models/{feature}.md
    dep-policy.md
    secrets-and-key-management.md
  architecture/
    overview.md
    context.mmd
    containers.mmd
    components.mmd
    sequences/{feature}.mmd
  runbook.md
  changelog_rules.md
.github/
  ISSUE_TEMPLATE.md
src/
  {language}/
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

## Operating Mode

### 1. Requirements Gathering & Task Planning

#### Requirements Collection

- Gather all **functional** and **non-functional** requirements
- Normalize and store in `docs/requirements/requirements.md` (single source of truth)
- Include: user stories, acceptance criteria, performance requirements, security requirements

#### Feature Breakdown Methodology

1. **Identify Features**: Group related requirements into logical features
2. **Define User Value**: Each feature must deliver measurable user value
3. **Create Feature Epics**: High-level feature descriptions with success criteria
4. **Break into Tasks**: Decompose features into implementable tasks

#### Task Decomposition Strategy

For each feature, create tasks that follow this pattern:

- **Core Behavior**: Main functionality (happy path)
- **Error Handling**: Edge cases, validation, error scenarios
- **Integration Points**: Adapters, external boundaries, data persistence
- **Security Controls**: Authentication, authorization, input validation
- **Observability**: Logging, metrics, monitoring, tracing
- **Testing Strategy**: Unit, integration, end-to-end test coverage
- **Documentation**: User docs, API docs, ADRs

#### Task Prioritization Framework

**Priority Levels**:

- **P0 (Critical)**: Core functionality, security fixes, data corruption risks
- **P1 (High)**: Essential features for MVP, performance issues
- **P2 (Medium)**: Important enhancements, nice-to-have features
- **P3 (Low)**: Future considerations, optimizations

**Prioritization Criteria**:

1. **User Impact**: High/Medium/Low user value
2. **Technical Risk**: Implementation complexity and unknowns
3. **Dependencies**: Blocking other work vs standalone
4. **Security**: Security implications and compliance requirements
5. **Effort**: Estimated development time (T-shirt sizing: XS/S/M/L/XL)

#### Estimation Techniques

- **Planning Poker**: Team estimation for complex features
- **T-Shirt Sizing**: XS(1-2h), S(half-day), M(1-2d), L(3-5d), XL(1w+)
- **Reference Stories**: Compare to previously completed similar work
- **Spike Tasks**: Time-boxed research for unknowns

#### Dependency Mapping

- **Technical Dependencies**: What must be built first
- **External Dependencies**: Third-party services, approvals, reviews
- **Resource Dependencies**: Team member availability, expertise needed
- **Sequencing**: Critical path analysis for parallel work

#### Task List Organization (`todo.md`)

Structure the root `todo.md` file as:

```markdown
# Project Task List

## Legend

- [ ] Not started
- [x] Complete
- [~] In progress
- [!] Blocked/Issues

## Milestone 1: [Name] - Due: YYYY-MM-DD

### Feature: [Feature Name] (P0)

- [ ] Core behavior: [specific task]
- [ ] Error handling: [specific cases]
- [ ] Security: [specific controls]
- [ ] Tests: [coverage requirements]
- [ ] Docs: [what needs documenting]

**Dependencies**: None | Requires Feature X
**Estimate**: M (1-2 days)
**Assignee**: [name or TBD]

### Feature: [Next Feature] (P1)

[same structure]

## Milestone 2: [Name] - Due: YYYY-MM-DD

[future features]

## Backlog (Not Scheduled)

### P2 Features

### P3 Features
```

#### Task Management Process

1. **Daily Updates**: Check off completed tasks, add new discoveries
2. **Weekly Review**: Reprioritize based on learnings, adjust estimates
3. **Milestone Planning**: Group tasks into achievable milestones
4. **Dependency Tracking**: Update blockers and unblock parallel work
5. **Scope Management**: Move tasks between milestones as needed

#### Integration with TDD Workflow

- **One failing test per task**: Each task starts with a failing test
- **Task completion criteria**: Tests pass, code reviewed, docs updated
- **Definition of Done**: Checklist for each task completion
- **Progress tracking**: Link commits to specific tasks

### 2. Architecture Decision Process

- Propose architecture style with clear rationale
- Generate diagrams as code (Mermaid or equivalent)
- Store in `docs/architecture/`
- Keep diagrams updated when structure changes
- Document in ADRs for significant decisions

### 3. Security Implementation

- **ASVS mapping**: Maintain compliance matrix
- **Top 10 alignment**: Address each risk category
- **Threat modeling**: Create models per feature
- **Secrets management**: Never commit secrets, use secure storage
- **Supply chain**: Verify dependencies, maintain license policy
- **Evidence**: Link security scans in PRs

### 4. TDD Loop (Per Task)

1. Write/extend a **failing** test
2. Write minimal code to pass the test
3. Refactor safely while keeping tests green
4. Ensure coverage and mutation thresholds are met
5. Commit with clear message

### 5. Third-Party Library Integration

- Require **ADR** for any new dependency
- Wrap libraries in `src/{language}/adapters/`
- Expose interfaces via `src/{language}/ports/`
- Prevent direct imports outside adapters
- Document security implications and license compatibility

### 6. Documentation Maintenance

- **Requirements**: Single source of truth in `docs/requirements/`
- **ADRs**: Document all significant technical decisions
- **Security**: Keep ASVS matrix, threat models, and policies current
- **Architecture**: Update diagrams with structural changes
- **Operations**: Maintain runbook and deployment notes

### 7. Daily Development Practices

- Append daily summaries to `summary/YYYY-MM-DD-development-summary.md`
- Include: what was done, why, risks identified, follow-ups needed
- Link to relevant ADRs, PRs, and test results

### 8. Systematic Debugging Process

When encountering failures or issues, follow this systematic approach:

#### Debugging Workflow

1. **Reproduce the Issue**

   - Create minimal reproduction case
   - Document exact steps to reproduce
   - Identify if issue is consistent or intermittent

2. **Gather Information**

   - Read complete error messages and stack traces
   - Check log files for additional context
   - Identify when issue started occurring (recent changes)
   - Test with known-good inputs for comparison

3. **Isolate the Problem**

   - Binary search approach: disable/enable components systematically
   - Test individual units in isolation
   - Use debugger or print statements to trace execution
   - Verify assumptions with assertions

4. **Form and Test Hypotheses**

   - List possible causes based on evidence
   - Test most likely causes first
   - Change one variable at a time
   - Document what was tried and results

5. **Fix and Verify**
   - Implement minimal fix that addresses root cause
   - Write test that would have caught the bug
   - Verify fix doesn't break other functionality
   - Document the fix in commit message and daily summary

#### Test Failure Analysis

When tests fail:

1. **Read the failure message carefully** - often contains the exact issue
2. **Check test isolation** - run failing test alone to verify it's not a dependency issue
3. **Verify test setup** - ensure test data and mocks are correct
4. **Compare expected vs actual** - understand what the test was trying to verify
5. **Check for timing issues** - race conditions, async operations
6. **Review recent changes** - what changed since tests last passed

#### Performance Issue Debugging

1. **Establish baseline** - measure current performance
2. **Profile the application** - identify bottlenecks
3. **Focus on hotspots** - optimize highest-impact areas first
4. **Measure improvements** - verify optimizations work
5. **Consider trade-offs** - balance performance vs maintainability

#### Memory Issue Debugging

1. **Monitor memory usage** - track growth patterns
2. **Look for leaks** - objects not being garbage collected
3. **Check large data structures** - unnecessary data retention
4. **Profile memory allocation** - identify memory-hungry operations
5. **Test with large inputs** - verify scalability

---

## Quality Standards

### Code Quality

- Follow language-specific style guides
- Use linters and formatters consistently
- Maintain consistent naming conventions
- Write self-documenting code with strategic comments

### Testing Requirements

- Unit tests for all business logic
- Integration tests for external boundaries
- Contract tests for service interactions
- End-to-end tests for critical user journeys
- Accessibility tests for user interfaces

### Security Standards

- Input validation on all external inputs
- Output encoding/escaping for all outputs
- Authentication and authorization controls
- Secure configuration management
- Error handling that doesn't leak information

### Performance Considerations

- Measure before optimizing
- Profile performance-critical paths
- Document performance requirements
- Monitor key metrics in production

---

## Definition of Done

Every task must meet these criteria before approval:

- [ ] Requirement slice complete with tests green (local & CI)
- [ ] Coverage and mutation thresholds met
- [ ] Code formatted and linted cleanly
- [ ] Security scans pass and ASVS matrix updated
- [ ] ADRs, diagrams, and documentation updated
- [ ] `todo.md` and daily summary updated
- [ ] PR opened, reviewed, and approved

---

## Architecture Patterns

### Recommended Patterns by Context

- **CLI Tools**: Clean Architecture with minimal layers
- **Web Applications**: Hexagonal/Ports & Adapters
- **Microservices**: Domain-Driven Design with bounded contexts
- **Data Processing**: Pipeline or Event-Driven Architecture
- **APIs**: RESTful with OpenAPI documentation

### Universal Architectural Principles

- Clear separation of concerns
- Dependency inversion (depend on abstractions)
- Testable boundaries
- Configuration externalization
- Observability built-in

---

## Observability & Monitoring

### Logging Requirements

- Structured logging (JSON or key/value format)
- Appropriate log levels (ERROR, WARN, INFO, DEBUG)
- Redact sensitive data from logs
- Include correlation IDs for tracing
- Log security events appropriately

### Metrics & Monitoring

- Business metrics for feature usage
- Technical metrics for performance
- Error rates and response times
- Resource utilization tracking
- Alert on threshold breaches

### Health Checks

- Application health endpoints
- Dependency health verification
- Graceful degradation strategies
- Circuit breaker patterns where appropriate

---

## Compliance & Legal

### License Management

- Maintain approved license allowlist
- Document all dependency licenses
- Regular license compliance audits
- Handle license conflicts promptly

### Data Privacy

- Implement privacy by design
- Document data flows and retention
- Comply with applicable regulations (GDPR, CCPA, etc.)
- Secure data handling practices

---

This document should be present in every project repository to ensure consistent development practices across all codebases.
