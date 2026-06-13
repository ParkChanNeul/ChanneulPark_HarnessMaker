import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PathSafetyTests(unittest.TestCase):
    def test_destination_paths_cannot_escape_root(self):
        from scripts.install_harness import safe_join
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                safe_join(root, '../escape.txt')
            with self.assertRaises(ValueError):
                safe_join(root, '/tmp/escape.txt')

    def test_existing_destination_symlink_fails(self):
        from scripts.install_harness import install
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'target'
            target.mkdir()
            dest = target / '.agents' / 'skills' / 'harness'
            dest.mkdir(parents=True)
            link = dest / 'SKILL.md'
            try:
                link.symlink_to(Path(tmp) / 'outside.txt')
            except (OSError, NotImplementedError):
                self.skipTest('symlink not supported on this filesystem')
            result = install(scope='project', target=target, repo_root=ROOT)
            self.assertFalse(result.ok)
            self.assertIn('symlink', '\n'.join(result.messages).lower())


if __name__ == '__main__':
    unittest.main()
