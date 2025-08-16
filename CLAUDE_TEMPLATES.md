# CLAUDE_TEMPLATES.md

Universal guidance for using project templates with Claude Code. Templates are located in `claude/templates/` directory.

---

## Template Overview

Templates ensure consistent documentation and workflow across all projects. Each template serves a specific purpose in the development lifecycle and integrates with the TDD workflow defined in CLAUDE_UNIVERSAL.md and CLAUDE_WORKFLOW.md.

---

## Available Templates

### 1. README_TEMPLATE.md

**Location**: `claude/templates/README_TEMPLATE.md`

**Purpose**: Standard project overview and setup documentation

**When to Use**:

- Every new project requires a README
- When updating project documentation structure
- During architecture changes that affect setup/usage

**Key Sections**:

- Project purpose and scope (one paragraph)
- Architecture pattern and rationale
- Getting started instructions
- Task list template for TDD workflow
- Security and accessibility considerations

**TDD Integration**:

- Task list section supports TDD workflow
- Links to test commands and coverage reports
- Includes test-first approach in setup instructions

---

### 2. CONTRIBUTING_TEMPLATE.md

**Location**: `claude/templates/CONTRIBUTING_TEMPLATE.md`

**Purpose**: Standardize contribution process and code review guidelines

**When to Use**:

- Every project should have contribution guidelines
- When onboarding new team members
- When establishing code review standards

**Key Sections**:

- TDD workflow requirements
- Branch naming and commit conventions
- Pull request process
- Code review expectations
- Quality standards

**TDD Integration**:

- Enforces failing test → minimal code → refactor cycle
- Requires test coverage for all contributions
- Links to testing commands and quality gates

---

### 3. PULL_REQUEST_TEMPLATE.md

**Location**: `claude/templates/PULL_REQUEST_TEMPLATE.md`

**Purpose**: Ensure consistent PR information and review process

**When to Use**:

- Automatically applied to all pull requests
- Should be customized per project needs
- Updated when adding new quality gates

**Key Sections**:

- Change description and type
- Testing verification checklist
- Security considerations
- Code quality checklist
- Related issues/ADRs

**TDD Integration**:

- Requires confirmation that TDD cycle was followed
- Validates test coverage requirements
- Links tests to specific changes

---

### 4. ADR_TEMPLATE.md

**Location**: `claude/templates/ADR_TEMPLATE.md`

**Purpose**: Document significant technical decisions

**When to Use**:

- New architecture decisions
- Technology selection choices
- Design pattern implementations
- Security architecture decisions
- Third-party library additions (required per CLAUDE_UNIVERSAL.md)

**Key Sections**:

- Context and problem statement
- Decision made with rationale
- Consequences (positive and negative)
- Alternatives considered

**TDD Integration**:

- Document how decisions affect testing strategy
- Reference test patterns that support the decision
- Link to architectural boundaries for testing

**Naming Convention**: `ADR-{id}-{kebab-case-title}.md`

---

### 5. ISSUE_TEMPLATE.md

**Location**: `claude/templates/ISSUE_TEMPLATE.md`

**Purpose**: Standardize issue reporting and feature requests

**When to Use**:

- Bug reports
- Feature requests
- Documentation updates
- Security concerns

**Key Sections**:

- Issue type classification
- Clear problem description
- Reproduction steps (for bugs)
- Requirement linkage
- Security considerations checklist

**TDD Integration**:

- Encourages test-first thinking in issue description
- Links issues to specific requirements
- Supports creation of failing tests from issue descriptions

---

### 6. LICENSE.md

**Location**: `claude/templates/LICENSE.md`

**Purpose**: Standard MIT license template

**When to Use**:

- Every new project
- When updating copyright information
- Legal compliance requirements

**Customization**:

- Update copyright year and holder name
- Ensure license compatibility with dependencies

---

## Template Usage Guidelines

### Creating New Files from Templates

1. **Copy the appropriate template**:

   ```bash
   cp claude/templates/README_TEMPLATE.md README.md
   ```

2. **Customize placeholders**:

   - Replace `{project-name}` with actual project name
   - Update `{language}` with programming language
   - Fill in `{package-manager}` and `{test-runner}` commands
   - Add project-specific sections

3. **Integrate with project workflow**:
   - Ensure templates reference correct paths
   - Update commands to match project setup
   - Link to project-specific documentation

### Template Customization Rules

#### Do Customize:

- Project-specific commands and paths
- Technology-specific sections
- Domain-specific requirements
- Team-specific processes

#### Don't Remove:

- TDD workflow requirements
- Security considerations
- Quality gate checklists
- Universal principles

### Repository Hygiene

Ensure these files exist from templates:

- [ ] `README.md` (from README_TEMPLATE.md)
- [ ] `CONTRIBUTING.md` (from CONTRIBUTING_TEMPLATE.md)
- [ ] `LICENSE` (from LICENSE.md)
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` (from PULL_REQUEST_TEMPLATE.md)
- [ ] `.github/ISSUE_TEMPLATE.md` (from ISSUE_TEMPLATE.md)

---

## Template Integration with Development Workflow

### Requirements to Documentation Flow

1. **Gather requirements** → Document in `docs/requirements/requirements.md`
2. **Make architecture decisions** → Create ADRs using ADR_TEMPLATE.md
3. **Create feature branches** → Follow CONTRIBUTING.md guidelines
4. **Open pull requests** → Use PR template for consistency
5. **Document issues** → Use issue template for clarity

### TDD Integration Points

#### README Integration:

- Task list supports TDD workflow
- Test commands for red-green-refactor cycle
- Coverage reporting instructions

#### ADR Integration:

- Document testing strategies for architectural decisions
- Reference test patterns and boundaries
- Link to test organization decisions

#### PR Integration:

- Verify TDD cycle was followed
- Confirm test coverage requirements
- Link tests to specific changes

### Quality Gate Integration

Templates enforce quality gates through:

- **Checklists**: Ensure nothing is forgotten
- **Required sections**: Force consideration of important aspects
- **Links**: Connect related documentation
- **Standards**: Maintain consistency across projects

---

## Project-Specific Template Adaptations

### CLI Applications

- Focus on command-line interface testing
- Include usage examples in README
- Emphasize input validation testing

### Web Applications

- Add accessibility testing requirements
- Include browser compatibility notes
- Security considerations for web threats

### Libraries/APIs

- API documentation standards
- Breaking change communication
- Backward compatibility testing

### Data Processing

- Data validation and schema testing
- Pipeline monitoring and alerting
- Performance testing requirements

---

## Template Maintenance

### Regular Updates

- Review templates quarterly
- Update for new security requirements
- Incorporate lessons learned from projects
- Keep consistent with universal guidelines

### Version Control

- Track template changes in git
- Document template evolution
- Maintain backward compatibility where possible
- Communicate template updates across projects

---

This guide ensures consistent use of templates while supporting the TDD workflow and quality standards defined in CLAUDE_UNIVERSAL.md and CLAUDE_WORKFLOW.md.
