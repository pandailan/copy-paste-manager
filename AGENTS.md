# Public distribution collaboration

The application source is private. This public repository contains release assets, the Homebrew cask, support information and distribution tooling only. Never copy application source, credentials or personal clipboard content here.

Keep the primary checkout on local `dev`; preserve `main` and shared history. Implement in an owned sibling `<repo>-worktrees/<branch>` worktree on `feature/app-xxx-description` or `fix/description`. Read `docs/working/status.md`, coordination and handoffs at task start and before integration. Commit coherent changes, merge latest local `dev` before each increment, and integrate only with `npm run integrate -- <branch>`. The helper holds a shared Git lock, verifies a retained candidate and fast-forwards clean `dev` only after checks pass. Merge `dev` back afterward. Never reset shared history or delete branches/worktrees.

Publish the exact ZIP and checksum before pointing the public cask at them. Keep release-candidate assets marked prerelease and update the exact prerelease allowlist with the cask. Never use `sha256 :no_check`, remove old assets/drafts, install over a user's application, or add a destructive zap stanza. Public `main` publication uses a normal fast-forward push of verified `dev`; concurrent updates must be reconciled and verified again.

Update status and an additive handoff with every integration. No secrets in repository files. Any installation check must use a separate temporary application directory, must not launch the app, and must preserve normal app data.
