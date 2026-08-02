# Development Summary — 2026-08-01 (dependency floor bumps)

## [2026-08-01 14:40] Commit Summary

**Change Type:** Chore
**Scope:** pyproject.toml dependency declarations

**Summary:**
Consolidated five Dependabot PRs (GH-9 through GH-13) into a single change,
raising the declared minimum for five development and plugin dependencies:

| Package | Old floor | New floor | Extra |
|---|---|---|---|
| safety | >=2.0.0 | >=3.7.0 | dev |
| bandit[toml] | >=1.7.0 | >=1.9.4 | dev |
| requests | >=2.28.0 | >=2.33.1 | plugins |
| beautifulsoup4 | >=4.11.0 | >=4.14.3 | plugins |
| pytesseract | >=0.3.10 | >=0.3.13 | plugins |

**Rationale:**
Consolidated rather than merged individually because all five modify adjacent
lines of the same file: merging them one at a time would require Dependabot to
rebase the remaining four after each merge, costing five CI runs to land five
one-line changes. Dependabot closes its own PRs once it observes the
requirements updated.

**What this does and does not change:**
Nothing about what CI actually installs. Because every requirement is an
unpinned `>=` range, `pip install -e ".[dev]"` already resolves to the newest
release: the environment was verified to be running bandit 1.9.4, safety 3.8.1
and requests 2.34.2 — at or above every proposed floor — *before* this change.

The bump therefore only raises the documented minimum. That still matters: it
records the baseline the project is actually tested against, and stops a
resolver working from an old cache or a constrained environment from silently
selecting a years-old release.

Note this is a symptom of the unpinned-dependency debt already recorded in
`summary/2026-08-01-development-summary.md`. Raising a floor is not a substitute
for pinning; CI remains non-deterministic across days until versions are pinned
per CLAUDE.md section 6.

**Verification:**
- `pip install --dry-run -e ".[dev,plugins]"` resolves with all five floors,
  confirming no conflict between the plugin and dev dependency sets
- `pip-audit` reports no known vulnerabilities in the resolved environment
- 113 tests pass (108 unit, 4 integration, 1 contract); black and flake8 exit 0

**References:**
- Supersedes: GH-9, GH-10, GH-11, GH-12, GH-13
