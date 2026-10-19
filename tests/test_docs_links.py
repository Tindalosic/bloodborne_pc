"""The distributed documentation must point at the project, not at its Discord server.

The launcher still signs in with Discord for The Hunter's Dream (that is the account system the
backend uses), so only invite links are checked here, never the word itself.
"""
import unittest

from paths import ROOT

INVITE = 'discord.gg'
UPSTREAM = 'https://github.com/Supermedo/bloodborne_pc'


class DocumentationTests(unittest.TestCase):
    def texts(self):
        files = [ROOT / 'README.md', ROOT / 'packaging' / 'windows' / 'README-Windows.txt']
        files += sorted((ROOT / 'docs').glob('*.md'))
        for path in files:
            if path.is_file():
                yield path, path.read_text(encoding='utf-8')

    def test_no_discord_invite_in_the_documentation(self):
        found = [str(path.relative_to(ROOT)) for path, text in self.texts() if INVITE in text]
        self.assertEqual(found, [], f'still advertising the Discord server: {found}')

    def test_readme_points_at_the_upstream_project(self):
        self.assertIn(UPSTREAM, (ROOT / 'README.md').read_text(encoding='utf-8'))

    def test_launcher_about_page_uses_the_same_address(self):
        source = (ROOT / 'launcher' / 'bbport_launcher_win.py').read_text(encoding='utf-8')
        self.assertIn(f"PROJECT_URL = '{UPSTREAM}'", source)
        self.assertIn('build_about', source)


if __name__ == '__main__':
    unittest.main()
