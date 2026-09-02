---
description: Resolve a CrewAI implementer branch in an isolated merge worktree
agent: crew-merge
subtask: true
---

Resolve a completed implementer branch safely.

Arguments:
- `$1`: source branch, for example `codeops/20260805-133739-614851`.
- Optional `$2`: project path. If absent, resolve it with `git rev-parse --show-toplevel 2>/dev/null || pwd`.

Execute this workflow:
1. Verify the source branch exists and the project is clean enough to create a merge worktree. Do not discard user changes.
2. Create a unique sibling worktree and branch from the current base HEAD.
3. Run `git merge --no-commit --no-ff <SOURCE_BRANCH>` in that worktree.
4. If conflicts exist, inspect all three versions and resolve only deterministic conflicts. Preserve business behavior from both branches where compatible.
5. Run focused tests and the project's normal validation.
6. If validation passes, commit the merge in the merge worktree only.
7. Report the worktree, merge branch, conflict files, validation, and this manual command:
   `git -C <PROJECT> merge <MERGE_BRANCH>`

Never run the final merge into `<PROJECT>` automatically. If intent is ambiguous, stop and ask one focused question.
