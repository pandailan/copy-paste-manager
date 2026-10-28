#!/usr/bin/env python3
import json
import os
import re
import subprocess
import uuid
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', HOMEBREW_NO_AUTO_UPDATE='1',
                       HOMEBREW_NO_ANALYTICS='1', HOMEBREW_DEVELOPER='1')
    cask = root / 'Casks/copy-paste-manager.rb'
    version = re.search(r'^  version "([^"]+)"$', cask.read_text(), re.M).group(1)
    exceptions = json.loads((root / 'audit_exceptions/github_prerelease_allowlist.json').read_text())
    if exceptions != {'copy-paste-manager': version}:
        raise RuntimeError('Prerelease allowlist must match the exact candidate version')
    subprocess.run(['python3', '-W', 'error', '-m', 'unittest', 'discover', '-s', 'scripts/tests'],
                   cwd=root, env=environment, check=True)
    subprocess.run(['brew', 'style', str(cask)], cwd=root, env=environment, check=True)
    repository = Path(subprocess.check_output(['brew', '--repository'], text=True).strip())
    owner = repository / 'Library/Taps/codex'
    owner.mkdir(parents=True, exist_ok=True)
    tap = 'cpm-release-check-' + uuid.uuid4().hex[:12]
    link = owner / ('homebrew-' + tap)
    link.symlink_to(root, target_is_directory=True)
    try:
        subprocess.run(['brew', 'audit', '--cask', '--online', f'codex/{tap}/copy-paste-manager'],
                       cwd=root, env=environment, check=True)
    finally:
        link.unlink()
    print('Public distribution tooling, Homebrew style and online audit passed.')


if __name__ == '__main__':
    main()
