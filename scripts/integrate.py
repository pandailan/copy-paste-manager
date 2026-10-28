#!/usr/bin/env python3
import argparse
import contextlib
import fcntl
import subprocess
import sys
import time
import uuid
from pathlib import Path


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], check=True, text=True, capture_output=True)
    return result.stdout.strip()


def clean(root):
    if git(root, 'status', '--porcelain', '--untracked-files=all'):
        raise RuntimeError(f'Checkout has uncommitted files: {root}')


@contextlib.contextmanager
def lock(common, timeout):
    with (common / 'integration.lock').open('a+') as handle:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RuntimeError('Another integration holds the shared lock') from None
                time.sleep(0.1)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def integrate(root, branch, verify=None, timeout=1800):
    root = Path(git(root, 'rev-parse', '--show-toplevel')).resolve()
    common = Path(git(root, 'rev-parse', '--git-common-dir'))
    if not common.is_absolute():
        common = root / common
    if branch == 'dev' or branch.startswith('-'):
        raise RuntimeError('Name a feature branch, not dev')
    git(root, 'check-ref-format', '--branch', branch)
    with lock(common.resolve(), timeout):
        feature = git(root, 'rev-parse', '--verify', f'refs/heads/{branch}')
        base = git(root, 'rev-parse', '--verify', 'refs/heads/dev')
        records = []
        for record in git(root, 'worktree', 'list', '--porcelain').split('\n\n'):
            records.append(dict(line.split(' ', 1) for line in record.splitlines() if ' ' in line))
        primaries = [Path(r['worktree']) for r in records if r.get('branch') == 'refs/heads/dev']
        if len(primaries) != 1:
            raise RuntimeError('Exactly one primary checkout on dev is required')
        primary = primaries[0]
        involved = {root, primary}
        involved.update(Path(r['worktree']) for r in records if r.get('branch') == f'refs/heads/{branch}')
        for checkout in involved:
            clean(checkout)
        name = f'fix/integration-{uuid.uuid4().hex[:12]}'
        candidate = Path(str(primary) + '-worktrees') / name
        candidate.parent.mkdir(parents=True, exist_ok=True)
        git(root, 'worktree', 'add', '-b', name, str(candidate), base)
        print(f'Retained candidate: {candidate}', flush=True)
        git(candidate, 'merge', '--no-edit', '--no-ff', feature)
        expected = git(candidate, 'rev-parse', 'HEAD')
        if verify is None:
            subprocess.run([sys.executable, str(candidate / 'scripts/verify.py')], cwd=candidate, check=True)
        elif verify(candidate) is False:
            raise RuntimeError('Candidate verification failed')
        clean(candidate)
        if git(candidate, 'rev-parse', 'HEAD') != expected:
            raise RuntimeError('Verifier changed the candidate commit')
        if git(root, 'rev-parse', 'refs/heads/dev') != base or git(root, 'rev-parse', f'refs/heads/{branch}') != feature:
            raise RuntimeError('A pinned branch changed during verification; retry')
        for checkout in involved:
            clean(checkout)
        if git(primary, 'symbolic-ref', 'HEAD') != 'refs/heads/dev':
            raise RuntimeError('Primary checkout changed branches')
        git(primary, 'merge', '--ff-only', expected)
        print(f'Integrated {branch}; dev is {expected}', flush=True)
        return expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('branch')
    parser.add_argument('--lock-timeout', type=float, default=1800)
    args = parser.parse_args()
    try:
        integrate(Path.cwd(), args.branch, timeout=max(0, args.lock_timeout))
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Integration stopped: {error}\n')


if __name__ == '__main__':
    main()
