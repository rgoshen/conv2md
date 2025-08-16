# CLAUDE_WORKFLOW.md

Universal workflow guidelines for Claude Code across all projects. These cover branching, commits, pull requests, CI/CD, and release management.

---

## Branching Strategy

### Branch Naming Convention

- **Feature branches**: `feature/{requirement-title-kebab}`
- **Bug fixes**: `fix/{issue-description-kebab}`
- **Documentation**: `docs/{topic-kebab}`
- **Security fixes**: `security/{vulnerability-kebab}`

### Branch Management

- One branch per requirement or logical feature
- Branch from `main` (or `develop` if using Git Flow)
- Keep branches focused and short-lived
- Delete branches after successful merge

### Protected Branches

- `main` and `develop` require:
  - Pull request reviews
  - Passing CI checks
  - Up-to-date with target branch
  - No force pushes allowed

---

## Commit Guidelines

### Commit Message Format

Use **Conventional Commits** format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes
- `security`: Security-related changes

### Commit Best Practices

- One logical change per commit
- Write clear, descriptive commit messages
- Reference issues/requirements when applicable
- Do NOT reference code generation tools or co-authors
- Commit after each completed task
- Update `todo.md` and daily summary with each commit

### Example Commits

```text
feat(cli): add input validation for file types
fix(parser): handle malformed JSON conversations
docs(readme): update installation instructions
test(converter): add golden fixture for HTML parsing
security(auth): implement input sanitization
```

---

## Pull Request Process

### When to Open a PR

Open **one PR per requirement branch** only when:

- All tasks under the requirement are complete
- Documentation, ADRs, and diagrams are current
- Security notes and ASVS matrix updated
- Tests meet coverage/mutation thresholds
- Daily development summary finalized

### PR Requirements

- Use the PR template (see CLAUDE_TEMPLATES.md)
- Fill out all sections completely
- Link related issues and ADRs
- Include security considerations
- Verify all CI checks pass
- Self-review code before requesting review

### Review Process

- Require at least one approval
- Address all reviewer feedback
- Keep discussions professional and constructive
- Re-request review after significant changes
- Ensure final CI run passes before merge

### Merge Strategy

- Use "Squash and merge" for feature branches
- Preserve commit history for main branch
- Delete feature branch after merge
- Next requirement starts only after merge approval

---

## Continuous Integration (CI/CD)

### Required CI Pipeline Jobs

#### Code Quality

```yaml
jobs:
  - name: 'Lint and Format'
    commands:
      - format-check
      - lint-check
    fail_fast: true

  - name: 'Tests'
    commands:
      - unit-tests
      - integration-tests
      - coverage-report
    coverage_threshold: '{configured_value}%'
    mutation_threshold: '{configured_value}%'
```

#### Security Scanning

```yaml
- name: 'Security Scans'
  commands:
    - sast-scan # Static application security testing
    - dependency-scan # Vulnerable dependency detection
    - secrets-scan # Leaked secrets detection
    - iac-scan # Infrastructure as code scanning
  fail_on: 'medium' # Fail on medium+ severity findings

- name: 'SBOM Generation'
  commands:
    - generate-sbom # Software bill of materials
  artifacts:
    - sbom.json
```

### CI Configuration Location

- GitHub Actions: `.github/workflows/`
- GitLab CI: `.gitlab-ci.yml`
- Jenkins: `Jenkinsfile`
- Other platforms: Follow platform conventions

### Branch Protection Rules

- Require PR reviews before merge
- Require status checks to pass
- Require branches to be up-to-date
- Restrict force pushes
- Restrict deletions

---

## Quality Gates

### Pre-Commit Checks (Local)

- [ ] Code formatted correctly
- [ ] Lints pass without errors
- [ ] Tests pass locally
- [ ] No new security warnings

### PR Quality Gates (CI)

- [ ] All tests pass
- [ ] Coverage threshold met
- [ ] Mutation testing threshold met
- [ ] Security scans clean
- [ ] Documentation updated
- [ ] SBOM generated

### Release Quality Gates

- [ ] All integration tests pass
- [ ] Performance tests within limits
- [ ] Security review completed
- [ ] Deployment runbook updated
- [ ] Rollback plan documented

---

## Release Management

### Versioning Strategy

- Follow **Semantic Versioning (SemVer)**
- Format: `MAJOR.MINOR.PATCH`
- Tag releases as `v{version}` (e.g., `v1.2.3`)

### Version Increment Rules

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Process

1. **Prepare Release**

   - Update version numbers
   - Generate changelog from commits/PRs
   - Update documentation
   - Tag release commit

2. **Deploy Release**

   - Build artifacts
   - Run full test suite
   - Deploy to staging first
   - Validate in staging environment
   - Deploy to production

3. **Post-Release**
   - Monitor for issues
   - Update monitoring dashboards
   - Communicate release to stakeholders
   - Document any post-deployment steps

### Changelog Generation

- Auto-generate from conventional commits
- Rules documented in `docs/changelog_rules.md`
- Include breaking changes prominently
- Group by type (features, fixes, security)

---

## Environment Management

### Configuration Strategy

- Environment variables for runtime config
- Secrets management for sensitive data
- No environment-specific code paths
- Configuration validation on startup

### Environment Parity

- Development mirrors production
- Same deployment process across environments
- Infrastructure as code
- Consistent monitoring across environments

### Deployment Environments

1. **Development**: Local development
2. **Testing**: Automated test execution
3. **Staging**: Production-like validation
4. **Production**: Live environment

---

## Monitoring & Observability

### Required Monitoring

- Application health endpoints
- Performance metrics collection
- Error rate tracking
- Business metrics monitoring
- Security event logging

### Alerting Strategy

- Define SLIs/SLOs for critical paths
- Alert on threshold breaches
- Escalation procedures documented
- On-call rotation if applicable

### Incident Response

- Incident response procedures in runbook
- Post-incident review process
- Blameless culture for learning
- Documentation of lessons learned

---

## Backup & Disaster Recovery

### Backup Requirements (Data-bearing applications)

- Regular automated backups
- Backup validation procedures
- Cross-region backup storage
- Recovery time objectives (RTO) defined
- Recovery point objectives (RPO) defined

### Disaster Recovery

- Documented recovery procedures
- Regular DR testing
- Failover procedures
- Communication plans

---

## Compliance & Auditing

### Audit Trail

- All changes tracked in version control
- Deployment logs maintained
- Access logs for sensitive operations
- Security event logging

### Compliance Requirements

- License compliance checking
- Security compliance validation
- Regulatory requirement adherence
- Regular compliance audits

---

This workflow applies to all projects and ensures consistent, high-quality software delivery practices.
