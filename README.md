# Copy Paste Manager

Public support and feedback repository for **Copy Paste Manager**, a macOS clipboard manager for people who copy, paste, reuse, clean up, and organize information all day.

The application source code is private. This repository is used for:

- Bug reports
- Feature requests
- Support questions
- Public roadmap discussion

Website: https://copypastemanager.com/

## What is Copy Paste Manager?

Copy Paste Manager is a native macOS utility that helps you keep your clipboard under control.

Core features include:

- Clipboard history
- Fast search
- Collections and categories
- Paste Queue for preparing multiple paste actions
- Copy Target for collecting copied content into a chosen destination
- Advanced Paste for text cleanup and formatting workflows
- Privacy exclusions for apps or contexts where clipboard capture should be avoided
- Local-first storage without accounts or cloud sync

## Report a bug

Open a new issue here:

https://github.com/pandailan/copy-paste-manager/issues/new

Please include:

- macOS version
- App version
- What you expected
- What happened instead
- Steps to reproduce
- Screenshots, if useful

Do **not** post sensitive clipboard content, passwords, private documents, license details, or crash logs containing personal paths unless you have reviewed and cleaned them first.

## Request a feature

Feature requests are welcome. Good requests explain:

- The workflow you are trying to improve
- What currently feels slow or annoying
- What outcome would make the feature useful

## Privacy note

Clipboard tools handle sensitive data by nature. Copy Paste Manager is designed around local-first usage and privacy controls. Please avoid sharing private clipboard content in public issues.

## Support status

This repository is for public product support and feedback. The app source code is not published here.

## Install with Homebrew

The Homebrew channel currently installs the signed, notarized **2.0.5 (3) release candidate** for macOS 14 Sonoma or later (Apple Silicon and Intel).

```sh
brew tap pandailan/copy-paste-manager https://github.com/pandailan/copy-paste-manager.git
brew install --cask pandailan/copy-paste-manager/copy-paste-manager
```

Or download the ZIP from [Releases](https://github.com/pandailan/copy-paste-manager/releases).

Start at Login is off until you explicitly enable it. Accessibility is optional: without it, select a clip and press ⌘V in the destination app. You can choose Enable Direct Paste to see an explanation and open macOS settings.

The direct and App Store versions share the same app identity and local history; install one distribution at a time. Updates use `brew update` and `brew upgrade --cask copy-paste-manager`. Normal Homebrew uninstall preserves local history; turn off Start at Login in Preferences before uninstalling.

This is a release candidate. Clean-account reboot checks and the visual permission demonstration are still pending, and App Store review has not been completed.
