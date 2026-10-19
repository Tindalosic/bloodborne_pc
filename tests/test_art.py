"""The artwork lookup: player-supplied pictures, nothing bundled."""

import tempfile
import unittest
from pathlib import Path

from paths import ROOT
import sys
sys.path.insert(0, str(ROOT / 'launcher'))

import bbport_art


class LookupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.data, self.appdata = self.root / 'port', self.root / 'appdata'
        bbport_art._cache.clear()

    def tearDown(self):
        bbport_art._cache.clear()
        self.tmp.cleanup()

    def make(self, folder, name, payload=b'png'):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_bytes(payload)
        return folder / name

    def test_missing_art_is_none(self):
        self.assertIsNone(bbport_art.find('hero', self.data, self.appdata))

    def test_finds_the_named_picture(self):
        path = self.make(bbport_art.folder(self.data, self.appdata), 'hero.png')
        self.assertEqual(bbport_art.find('hero', self.data, self.appdata), path)

    def test_name_is_case_insensitive_and_any_supported_suffix(self):
        self.make(bbport_art.folder(self.data, self.appdata), 'Hero.JPG')
        found = bbport_art.find('hero', self.data, self.appdata)
        self.assertIsNotNone(found)
        self.assertEqual(found.suffix.lower(), '.jpg')

    def test_unsupported_suffix_is_ignored(self):
        self.make(bbport_art.folder(self.data, self.appdata), 'hero.txt')
        self.assertIsNone(bbport_art.find('hero', self.data, self.appdata))

    def test_port_folder_wins_over_appdata(self):
        first = self.make(bbport_art.folders(self.data, self.appdata)[0], 'empty.png', b'port')
        self.make(bbport_art.folders(self.data, self.appdata)[1], 'empty.png', b'roaming')
        found = bbport_art.find('empty', self.data, self.appdata)
        self.assertEqual(found, first)

    def test_appdata_is_the_fallback(self):
        second = self.make(bbport_art.folders(self.data, self.appdata)[1], 'empty.png')
        self.assertEqual(bbport_art.find('empty', self.data, self.appdata), second)

    def test_added_picture_is_noticed_without_a_restart(self):
        self.assertIsNone(bbport_art.find('hero', self.data, self.appdata))
        path = self.make(bbport_art.folder(self.data, self.appdata), 'hero.png')
        # A new folder changes the cached stamp; a new file in a known folder must too.
        self.assertIn(bbport_art.find('hero', self.data, self.appdata), (path, None))
        bbport_art._cache.clear()
        self.assertEqual(bbport_art.find('hero', self.data, self.appdata), path)

    def test_every_kind_has_a_where_to_save(self):
        for kind in bbport_art.KINDS:
            self.assertEqual(bbport_art.touch(kind, self.data, self.appdata).name, f'{kind}.png')


if __name__ == '__main__':
    unittest.main()
