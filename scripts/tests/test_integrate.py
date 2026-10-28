import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('integrate', Path(__file__).resolve().parents[1] / 'integrate.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.git('init', '-b', 'dev')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        (self.root / 'README').write_text('base')
        self.git('add', 'README')
        self.git('commit', '-m', 'base')
        self.base = self.git('rev-parse', 'HEAD')
        self.git('switch', '-c', 'feature/test')
        (self.root / 'change').write_text('feature')
        self.git('add', 'change')
        self.git('commit', '-m', 'feature')
        self.feature = self.git('rev-parse', 'HEAD')
        self.git('switch', 'dev')

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return MODULE.git(self.root, *args)

    def test_verified_combined_candidate_advances_dev(self):
        observed = []
        result = MODULE.integrate(self.root, 'feature/test', lambda candidate: observed.append(candidate))
        self.assertEqual(self.git('rev-parse', 'dev'), result)
        self.assertEqual((observed[0] / 'change').read_text(), 'feature')
        self.assertTrue(observed[0].exists())

    def test_failed_gate_preserves_dev_and_candidate(self):
        with self.assertRaises(RuntimeError):
            MODULE.integrate(self.root, 'feature/test', lambda _: False)
        self.assertEqual(self.git('rev-parse', 'dev'), self.base)
        self.assertTrue(list(Path(str(self.root) + '-worktrees').glob('fix/integration-*')))

    def test_dirty_primary_is_rejected(self):
        (self.root / 'README').write_text('uncommitted')
        with self.assertRaises(RuntimeError):
            MODULE.integrate(self.root, 'feature/test', lambda _: True)
        self.assertEqual(self.git('rev-parse', 'dev'), self.base)

    def test_verifier_cannot_dirty_candidate(self):
        def dirty(candidate):
            (candidate / 'unexpected').write_text('uncommitted')
        with self.assertRaises(RuntimeError):
            MODULE.integrate(self.root, 'feature/test', dirty)
        self.assertEqual(self.git('rev-parse', 'dev'), self.base)

    def test_concurrent_feature_change_is_rejected(self):
        def change_ref(_):
            self.git('update-ref', 'refs/heads/feature/test', self.base)
        with self.assertRaises(RuntimeError):
            MODULE.integrate(self.root, 'feature/test', change_ref)
        self.assertEqual(self.git('rev-parse', 'dev'), self.base)

    def test_lock_excludes_other_integrators(self):
        common = self.root / '.git'
        with MODULE.lock(common, 0):
            code = 'import fcntl,sys; f=open(sys.argv[1],"a+"); fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)'
            result = subprocess.run(['python3', '-c', code, str(common / 'integration.lock')], capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
