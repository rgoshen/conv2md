# Development Summary — 2026-08-01 (remove Claude workflow)

## [2026-08-01 16:05] Commit Summary

**Change Type:** Chore
**Scope:** CI workflows

**Summary:**
Removed `.github/workflows/claude.yml`, the last workflow invoking Claude from
CI. Its companion `claude-code-review.yml` (which ran automatically on every
pull request) was removed earlier today.

**Rationale:**
`claude.yml` was gated on an explicit `@claude` mention, so it never consumed
usage quota on its own. It was retained initially to preserve on-demand review.
In practice it produced a `claude` check reporting SKIPPED on effectively every
pull request, because its triggers include `pull_request_review` and
`pull_request_review_comment` — and every CodeRabbit review submission fires
those events, spawning a run whose job condition immediately evaluates false.

That skipped row was read as evidence the deleted auto-review workflow had come
back, which is precisely the kind of ambiguous CI signal that erodes trust in
the checks list. Review remains available on demand outside CI, so the workflow
was carrying noise without carrying value.

**Consequences:**
- No workflow in this repository invokes Claude. Usage quota cannot be consumed
  by CI under any trigger.
- The `CLAUDE_CODE_OAUTH_TOKEN` repository secret is now unreferenced. It was
  last set 2025-08-19 and had almost certainly expired; it can be deleted.
- `@claude` mentions in issues, pull requests, and review comments no longer do
  anything.

**Verification:**
- `.github/workflows/` retains auto-pr-to-main.yml, ci.yml, codeql.yml,
  security.yml — no remaining reference to claude-code-action
- 137 tests pass; black and flake8 exit 0 (no source changes)

**References:**
- Follows: removal of claude-code-review.yml (commit b02176c)
