#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Tests for locale packs: JSON files that translate launcher texts without editing Python."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

from paths import ROOT

sys.path.insert(0, str(ROOT / 'launcher'))
import bbport_locale  # noqa: E402


class LocalePackTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)

    def write(self, language, content):
        path = self.folder / f'{language}.json'
        path.write_text(json.dumps(content, ensure_ascii=False), encoding='utf-8')
        return path

    def test_pack_translates_known_keys(self):
        self.write('zh', {'Quit': '退出', 'Resume': '继续'})
        self.assertEqual(bbport_locale.pack('zh', [self.folder]), {'Quit': '退出', 'Resume': '继续'})

    def test_missing_pack_is_empty(self):
        self.assertEqual(bbport_locale.pack('ko', [self.folder]), {})

    def test_empty_and_non_string_values_are_ignored(self):
        # An empty value means "not translated yet", and a nested list would render as garbage.
        self.write('zh', {'Quit': '退出', 'Resume': '', 'Shaders': ['nope'], '_note': 'readme'})
        self.assertEqual(bbport_locale.pack('zh', [self.folder]), {'Quit': '退出'})

    def test_later_folder_wins(self):
        other = self.folder / 'overrides'
        other.mkdir()
        self.write('zh', {'Quit': '退出'})
        (other / 'zh.json').write_text(json.dumps({'Quit': '结束'}), encoding='utf-8')
        self.assertEqual(bbport_locale.pack('zh', [self.folder, other]), {'Quit': '结束'})

    def test_broken_pack_is_skipped(self):
        (self.folder / 'zh.json').write_text('{ "Quit": "退出",', encoding='utf-8')
        self.assertEqual(bbport_locale.pack('zh', [self.folder]), {})

    def test_merge_lays_pack_over_table(self):
        self.write('zh', {'Quit': '退出'})
        table = {'Quit': 'Quit', 'Resume': 'Resume'}
        self.assertEqual(bbport_locale.merge('zh', table, [self.folder]), {'Quit': '退出', 'Resume': 'Resume'})

    def test_merge_leaves_english_alone(self):
        # English is the key language: a pack would only shadow the source text.
        table = {'Quit': 'Quit'}
        self.assertIs(bbport_locale.merge('en', table, [self.folder]), table)
        self.assertIs(bbport_locale.merge('', table, [self.folder]), table)

    def test_template_lists_every_key(self):
        template = bbport_locale.template('de', {'Quit': 'Beenden'}, ['Quit', 'Resume'])
        self.assertEqual(template, {'Quit': 'Beenden', 'Resume': ''})


class ShippedTranslationsTest(unittest.TestCase):
    """The built-in tables still have to load: packs are laid over them, not instead of them."""

    def test_languages_load(self):
        import bbport_lang
        for language in ('zh', 'ja', 'ko', 'de', 'ru'):
            table = bbport_lang.table(language)
            # The upstream tables are partial (Russian covers 47 texts), so only require content.
            self.assertGreater(len(table), 20, language)
        self.assertGreater(len(bbport_lang.table('zh')), 100)

    def test_achievement_texts_are_localised(self):
        import bbport_trophies as trophies
        import bbport_trophy_text as trophy_text
        self.assertEqual(trophy_text.text(trophies.BY_ID[1], 'zh')[0], '亚南日出')
        self.assertEqual(trophy_text.text(trophies.BY_ID[1], 'en'), (trophies.BY_ID[1][1], trophies.BY_ID[1][2]))
        # A language without a pack keeps the English text rather than showing an empty row.
        self.assertEqual(trophy_text.text(trophies.BY_ID[1], 'ru'), (trophies.BY_ID[1][1], trophies.BY_ID[1][2]))


class TraditionalChineseTest(unittest.TestCase):
    """`zh-hant` is generated from the Simplified table, so it must cover exactly the same keys."""

    def test_traditional_covers_the_simplified_keys(self):
        import bbport_lang
        simplified = bbport_lang.table('zh')
        traditional = bbport_lang.table('zh-hant')
        self.assertGreater(len(traditional), 300)
        missing = [key for key, text in simplified.items() if isinstance(text, str) and text and key not in traditional]
        self.assertEqual(missing, [])

    def test_traditional_uses_traditional_characters(self):
        import bbport_lang
        table = bbport_lang.table('zh-hant')
        self.assertEqual(table['Text language'], '遊戲文字語言')
        self.assertEqual(table['Mouse look'], '滑鼠視角')
        # Simplified-only forms must not survive the conversion.
        for text in table.values():
            if isinstance(text, str):
                self.assertNotIn('鼠标', text)
                self.assertNotIn('游戏', text)

    def test_trophy_texts_are_traditional_too(self):
        import bbport_trophies as trophies
        import bbport_trophy_text as trophy_text
        self.assertIn('zh-hant', trophy_text.LANGUAGES)
        self.assertEqual(trophy_text.text(trophies.BY_ID[1], 'zh-hant')[0], '亞南日出')
        self.assertEqual(trophy_text.coverage('zh-hant'), (len(trophies.TROPHIES), len(trophies.TROPHIES)))
        self.assertEqual(trophy_text.group(trophies.DLC, 'zh-hant'), '老獵人')


if __name__ == '__main__':
    unittest.main()
