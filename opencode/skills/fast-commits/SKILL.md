---
name: fast-commits
description: Writes concise, semantically grouped commit messages. Groups changed files by domain or function into small atomic commits.
---

## Description

Writes concise, semantically grouped commit messages. Groups changed files by domain or function into small atomic commits. Descriptions are minimal by default — prefix + short phrase, no body, no file lists.

## Trigger

- User says "commit", "write commits", "commit these changes", or "group commits"
- After code changes are staged and ready to commit
- User asks to split a large diff into smaller commits
- Before creating a PR and commits need to be organized

## Instructions

1. Run `git diff --cached --stat` and `git diff --cached` to see all staged changes.
2. Group files by semantic domain or function (e.g., auth logic, API routes, UI components, tests, config). Prefer 1–3 files per commit over monolithic commits.
3. For each group, write a commit using conventional format:
   - `feat: add login endpoint` (not "Added a new login endpoint to handle user authentication")
   - `fix: null check in user query` (not "Fixed a bug where the user query would crash when...")
   - `refactor: extract auth middleware` (not "Refactored the authentication logic into a separate middleware file")
4. Stage only files for that group, commit, repeat until all changes are committed.
5. If a file belongs to no clear group, create a `chore:` or `misc:` commit for leftovers.

## Rules

- Never write multi-line commit bodies unless user explicitly asks.
- Never list files in the commit message — `git log --stat` already does that.
- Never use past tense ("Added", "Fixed") — use imperative ("add", "fix").
- Prefix must match the change type: `feat`, `fix`, `refactor`, `chore`, `test`, `docs`, `style`, `perf`, `ci`, `build`.
- One logical change per commit. If a file touches two concerns, split it or pick the dominant one.
- Max 10 words in the subject line. Shorter is better.
- Never commit secrets, keys, or credentials. Check staged diffs before every commit.

## Examples

```
# Stage 1: auth files
git add src/auth/login.ts src/auth/middleware.ts
git commit -m "feat: add login and auth middleware"

# Stage 2: API route that uses auth
git add src/routes/api/users.ts
git commit -m "feat: add user API route"

# Stage 3: tests for auth
git commit -m "test: add auth unit tests"

# Stage 4: leftover config
git commit -m "chore: update env defaults"
```

Edge case — single file touches two concerns:
```
# File src/api/handler.ts adds endpoint AND fixes a bug
git add src/api/handler.ts
git commit -m "feat: add search endpoint"
# If the bug fix is critical and independent, user should be asked to split the staging
```

## Proactive Save Triggers

- After committing a non-obvious grouping decision
- When user specifies a preferred commit style or convention
- When discovering project-specific commit conventions from git log
