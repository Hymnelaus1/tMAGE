# Third-party skills

The skill folders in this directory (except `karpathy-guidelines`'s origin,
noted below) are vendored, unmodified, from:

- **brainstorming, diagnosing-superpowers, dispatching-parallel-agents,
  executing-plans, finishing-a-development-branch, receiving-code-review,
  requesting-code-review, subagent-driven-development, systematic-debugging,
  test-driven-development, using-git-worktrees, using-superpowers,
  verification-before-completion, writing-plans, writing-skills**
  Source: https://github.com/obra/superpowers
  Commit: 22f0b463e7a5e579904dd6211a520321035526f7
  License: MIT (c) 2025 Jesse Vincent

- **karpathy-guidelines**
  Source: https://github.com/multica-ai/andrej-karpathy-skills
  Commit: 2c606141936f1eeef17fa3043a72095b4765b9c2
  License: MIT

Reviewed by hand before vendoring (no network calls, no eval/exec of
obfuscated code, no credential access) since both repos' `.claude/skills`
layout runs with the same trust as any other project code once Claude Code
loads it. Update by re-copying from the source repo's `skills/` directory at
a newer commit, keeping this file's commit hashes current.
