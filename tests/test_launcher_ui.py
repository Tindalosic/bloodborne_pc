"""Launcher window checks: the text language list, the patch column and the achievement names.

The window is created withdrawn, so the tests need a display but never show anything. They run the
real Launcher against a scratch configuration directory, which is where the launcher would write
its own settings and trophy log, so the user's files are never touched.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from paths import ROOT

# The launcher resolves its folders when it is imported, so redirect them before the import.
_SCRATCH = Path(tempfile.mkdtemp(prefix='bbport-ui-'))
(_SCRATCH / 'data').mkdir()
(_SCRATCH / 'bbport-launcher').mkdir()
(_SCRATCH / 'bbport-launcher' / 'settings.json').write_text(json.dumps({
    'check_updates': False,
    'game_dir': '',
    # The repository's own folder, so the assertions see the shipped community list.
    'patches_dir': str(ROOT / 'patches'),
    'ui_language': 'zh',  # Chinese labels make the localisation path visible to the assertions
}))
os.environ['APPDATA'] = str(_SCRATCH)
os.environ['BB_DATA_DIR'] = str(_SCRATCH / 'data')
os.environ['BB_CONFIG'] = str(_SCRATCH / 'bbport.ini')
if str(ROOT / 'launcher') not in sys.path:
    sys.path.insert(0, str(ROOT / 'launcher'))


class LauncherWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import tkinter as tk
            from tkinter import filedialog, messagebox, ttk
            cls.root = tk.Tk()
        except Exception as error:  # a headless session should skip, not fail the suite
            raise unittest.SkipTest(f'no Tk display: {error}')
        cls.root.withdraw()
        import bbport_launcher_win as launcher
        cls.launcher = launcher
        cls.tk, cls.ttk = tk, ttk
        launcher.LANG = 'zh'  # main() would set this from the settings file
        cls.app = launcher.Launcher(cls.root, tk, ttk, filedialog, messagebox)
        cls.app.refresh_lists()
        cls.root.update()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def widgets(self, kind=None):
        found = []

        def walk(widget):
            for child in widget.winfo_children():
                if kind is None or isinstance(child, kind):
                    found.append(child)
                walk(child)

        walk(self.root)
        return found

    def test_text_language_offers_chinese_and_korean(self):
        boxes = [w for w in self.widgets(self.ttk.Combobox)]
        choices = [tuple(box.cget('values')) for box in boxes]
        lists = [values for values in choices if len(values) == len(self.launcher.LANGUAGES)]
        self.assertEqual(len(lists), 1, f'expected one text language list, got {len(lists)}')
        names = lists[0]
        for expected in ('简体中文', '繁體中文', '한국어'):
            self.assertIn(expected, names)
        self.assertEqual(len(set(names)), len(names), 'a language appears twice')

    def test_language_combobox_value_is_the_ps4_id(self):
        # The combobox shows a name; the variable holds the id the runtime passes to the game.
        self.assertEqual(self.app.vars['language'].get(), '1')
        codes = [code for code, _names in self.launcher.LANGUAGES]
        self.assertEqual(len(codes), len(set(codes)))
        self.assertLessEqual({'9', '10', '11'}, set(codes))

    def test_community_patches_are_listed_and_start_off(self):
        keys = list(self.app.patch_vars)
        self.assertGreaterEqual(len(keys), 55, f'only {len(keys)} patches listed')
        self.assertIn('shadps4-Bloodborne.xml/Unlock Game Region', keys)
        self.assertFalse([key for key, var in self.app.patch_vars.items() if var.get()],
                         'a bundled patch was ticked without the user asking')

    def test_conflicting_patches_are_named_once_per_pair(self):
        keys = [key for key in self.app.patch_vars if key.endswith(('/120 FPS++', '/30 FPS++'))]
        if len(keys) != 2:
            self.skipTest('the bundled list has no 120/30 FPS presets')
        for key in keys:
            self.app.patch_vars[key].set(True)
        self.app.update_patch_conflicts()
        lines = [line for line in self.app.patch_conflict_label.cget('text').splitlines() if line.strip()]
        self.assertEqual(len(lines), 1, 'the same pair was reported once per address')
        self.assertIn('120 FPS++', lines[0])
        self.assertIn('30 FPS++', lines[0])

    def test_achievement_names_follow_the_ui_language(self):
        self.app.render_trophies()  # the page fills itself once the unlocks are read
        self.root.update()
        labels = [w.cget('text') for w in self.widgets(self.tk.Label)]
        self.assertTrue(any('亚南日出' in text for text in labels),
                        'the achievement page did not use the Chinese names')


if __name__ == '__main__':
    unittest.main()
