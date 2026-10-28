# Coordination

Follow AGENTS.md. The release owner reserves the cask, exact-version audit allowlist, public README and distribution workflow together. Other agents communicate through additive handoffs. Read status and handoffs before integration and do not modify another agent's checkout.

The shared integration lock is in the common Git directory. Candidate worktrees and their branches are retained on success or failure. Verification runs Python tooling tests, Homebrew style and the real online Homebrew cask audit. Verification creates only a unique temporary tap link, removes that link afterward, and uses process-only Homebrew developer/no-update/no-analytics values. At most one lightweight verification stage runs at a time; no native builds are part of this repository.
