"""The Third-party patches list: which files count, what starts enabled, and what conflicts."""
from paths import ROOT
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from patches import conflicts, external_patches, external_selection, file_digest

sys.path.insert(0, str(ROOT / 'launcher'))
import bbport_patches  # noqa: E402

XML = ROOT / 'patches/Bloodborne.xml'
CATALOGUE = ROOT / 'patches/shadps4-Bloodborne.xml'
VERSION = '01.09'


class ThirdPartyListTests(unittest.TestCase):
    def setUp(self):
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory, True)

    def test_built_in_file_is_not_a_third_party_patch(self):
        # A copy under another name: an unpacked app keeps patches/ outside the scripts folder,
        # so the built-in file is recognised by content and never applied twice.
        shutil.copy(XML, self.directory / 'my-patches.xml')
        self.assertEqual(external_patches(self.directory, VERSION), [])

    def test_catalogue_is_listed_and_starts_off(self):
        found = external_patches(self.directory.parent / 'bloodborne_pc' / 'patches', VERSION) \
            if False else external_patches(CATALOGUE.parent, VERSION)
        self.assertGreater(len(found), 60)
        names = {meta.get('Name') for _key, path, meta in found if path.name == CATALOGUE.name}
        self.assertIn('Unlock Game Region', names)
        self.assertTrue(all(meta.get('isEnabled', 'false').lower() != 'true'
                            for _key, _path, meta in found if _path.name == CATALOGUE.name))
        self.assertFalse([_key for _key, path, _meta in found if file_digest(path) == file_digest(XML)])

    def test_selection_needs_an_explicit_tick(self):
        found = external_patches(CATALOGUE.parent, VERSION)
        config = self.directory / 'patches.json'
        self.assertEqual(external_selection(found, config), [])
        key = f'{CATALOGUE.name}/Unlock Game Region'
        config.write_text('{"enabled": ["%s"], "disabled": []}' % key, encoding='utf-8')
        selected = external_selection(found, config)
        self.assertEqual([item[0] for item in selected], [key])

    def test_conflicts_pairs_the_two_writers(self):
        def meta(address, data):
            node = ET.Element('Metadata')
            ET.SubElement(node, 'Line', Address=hex(address), Type='bytes', Value=data)
            return node
        same = [('a.xml/one', Path('a.xml'), meta(0x401000, '9090')),
                ('b.xml/two', Path('b.xml'), meta(0x401001, '90'))]
        self.assertEqual(conflicts(same), [])
        differ = [('a.xml/one', Path('a.xml'), meta(0x401000, '9090')),
                  ('b.xml/two', Path('b.xml'), meta(0x401001, '91'))]
        self.assertEqual(conflicts(differ), [('a.xml/one', 'b.xml/two', 0x401001)])


class CatalogueDownloadTests(unittest.TestCase):
    def setUp(self):
        self.directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.directory, True)

    def test_install_keeps_the_previous_file(self):
        first = CATALOGUE.read_bytes()
        path, count, backup = bbport_patches.install(self.directory, first)
        self.assertEqual(path, bbport_patches.catalogue_path(self.directory))
        self.assertIsNone(backup)
        self.assertGreater(count, 60)
        path2, count2, backup2 = bbport_patches.install(self.directory, first)
        self.assertEqual(path2, path)
        self.assertIsNotNone(backup2)
        self.assertTrue(backup2.is_file())
        self.assertEqual(bbport_patches.describe(path)[0], count)

    def test_a_bad_download_never_replaces_the_file(self):
        bbport_patches.install(self.directory, CATALOGUE.read_bytes())
        before = bbport_patches.catalogue_path(self.directory).read_bytes()
        for bad in (b'not xml at all', b'<Patches><Metadata Name="x" AppVer="01.09"/></Patches>'):
            with self.assertRaises(ValueError):
                bbport_patches.install(self.directory, bad)
        self.assertEqual(bbport_patches.catalogue_path(self.directory).read_bytes(), before)

    def test_check_rejects_another_game(self):
        data = (b'<Patches><ID>CUSA99999</ID>'
                + b''.join(b'<Metadata Name="p%d" AppVer="01.09"><Line Address="0x401000" '
                           b'Type="bytes" Value="90"/></Metadata>' % i for i in range(12))
                + b'</Patches>')
        with self.assertRaises(ValueError):
            bbport_patches.check(data)


if __name__ == '__main__':
    unittest.main()
