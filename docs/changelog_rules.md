# Changelog Generation Rules

## Overview

This document defines the rules for generating changelogs from conventional commits for the conv2md project.

## Commit Types and Changelog Sections

### Breaking Changes

- **Trigger**: Commits with `BREAKING CHANGE:` in footer or `!` after type
- **Section**: "⚠️ BREAKING CHANGES"
- **Visibility**: Prominently displayed at top of release notes

### Features

- **Trigger**: `feat:` type commits
- **Section**: "✨ Features"
- **Format**: `- **scope**: description (commit-hash)`

### Bug Fixes

- **Trigger**: `fix:` type commits
- **Section**: "🐛 Bug Fixes"
- **Format**: `- **scope**: description (commit-hash)`

### Security

- **Trigger**: `security:` type commits
- **Section**: "🔒 Security"
- **Format**: `- **scope**: description (commit-hash)`
- **Visibility**: Highlighted section, always included

### Documentation

- **Trigger**: `docs:` type commits
- **Section**: "📚 Documentation"
- **Format**: `- **scope**: description (commit-hash)`

### Performance

- **Trigger**: `perf:` type commits
- **Section**: "⚡ Performance"
- **Format**: `- **scope**: description (commit-hash)`

### Excluded from Changelog

- `chore:` - Build process, maintenance
- `style:` - Code formatting changes
- `test:` - Test additions/modifications
- `refactor:` - Code restructuring without feature changes

## Scope Guidelines

### Valid Scopes

- `cli` - Command-line interface changes
- `json` - JSON conversation processing
- `html` - HTML/website processing
- `markdown` - Markdown generation
- `images` - Image processing functionality
- `plugins` - Plugin system
- `security` - Security-related changes
- `docs` - Documentation updates

### Scope Formatting

- Use lowercase
- Use hyphens for multi-word scopes
- Be specific but concise

## Version Increment Rules

### Major Version (X.0.0)

- Breaking changes that affect public API
- Changes requiring user action for upgrade
- Architectural changes affecting compatibility

### Minor Version (0.X.0)

- New features (backward compatible)
- New CLI options or functionality
- Plugin API additions

### Patch Version (0.0.X)

- Bug fixes
- Security patches
- Documentation improvements
- Performance improvements (non-breaking)

## Changelog Format Template

```markdown
# Changelog

## [X.Y.Z] - YYYY-MM-DD

### ⚠️ BREAKING CHANGES

- **scope**: description of breaking change (hash)

### ✨ Features

- **scope**: description of new feature (hash)

### 🐛 Bug Fixes

- **scope**: description of bug fix (hash)

### 🔒 Security

- **scope**: description of security improvement (hash)

### ⚡ Performance

- **scope**: description of performance improvement (hash)

### 📚 Documentation

- **scope**: description of documentation change (hash)

## [Previous Version] - YYYY-MM-DD

...
```

## Automation Rules

### Auto-Generation Triggers

- Generate changelog on version tag creation
- Include all commits since last version tag
- Group commits by type and scope
- Sort by scope alphabetically within each type

### Manual Review Required

- Breaking changes must be manually verified
- Security changes require security team review
- Major version releases need stakeholder approval

## Examples

### Good Commit Messages for Changelog

```
feat(cli): add timezone configuration option
fix(json): handle malformed timestamp formats
security(html): prevent XSS in content extraction
docs(readme): update installation instructions
```

### Resulting Changelog Entries

```markdown
### ✨ Features

- **cli**: add timezone configuration option (abc123)

### 🐛 Bug Fixes

- **json**: handle malformed timestamp formats (def456)

### 🔒 Security

- **html**: prevent XSS in content extraction (ghi789)

### 📚 Documentation

- **readme**: update installation instructions (jkl012)
```

## Quality Standards

### Required Information

- All entries must include scope
- Descriptions should be user-facing (not implementation details)
- Security fixes must include severity if applicable
- Breaking changes must include migration guidance

### Review Process

- Changelog reviewed before release
- Breaking changes verified by maintainers
- Security entries reviewed by security team
- User-facing language validated for clarity
