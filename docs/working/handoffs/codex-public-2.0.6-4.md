# Codex — public 2.0.6 (4) release candidate

## 2026-10-28 — publication and workflow setup

- Acknowledged clean public main `3649b76` and the user's authorization to publish the matching v2.0.6-4 release candidate and public Homebrew cask. Older deferral is superseded. Private application code is not copied here.
- Branch/worktree: `feature/app-001-release-candidate`, `/Users/pandailan/Development/Apps/copy-paste-manager-worktrees/feature/app-001-release-candidate`; primary is `/Users/pandailan/Development/Apps/copy-paste-manager` on dev. Existing installed Homebrew tap remains separate.
- Owns cask, exact prerelease allowlist, README and new public workflow tooling/docs. Cask and checksum come from the verified clean candidate; SHA-256 is `040c3345ff0ebbe346415a1fabf4321272f7da1479b72817213fba1045f47f20`.
- Establishing the missing dev/helper workflow is an explicit setup step. Candidate checks use only public distribution tooling and actual Homebrew style/online audit. Shared-lock/ref/clean-tree protections preserve history and retain candidate worktrees.
- Environment: GitHub connector advertised metadata but returned Unknown tool, so existing gh CLI is used. Homebrew audit help enabled developer mode automatically; it was immediately restored off. All subsequent developer settings are process-only. A unique verification tap link will be removed after checking; normal installed app/data are untouched.
- Release publication precedes cask publication. Old assets/drafts remain. Final URLs, integration commit, remote state, checks and any gaps are reported after execution; no stable promotion or App Store claim.
