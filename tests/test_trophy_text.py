from paths import ROOT
import sys
import unittest

if str(ROOT / 'launcher') not in sys.path:
    sys.path.insert(0, str(ROOT / 'launcher'))
import bbport_trophies as trophies
import bbport_trophy_text as trophy_text


class TrophyTextTests(unittest.TestCase):
    def test_chinese_covers_every_trophy(self):
        self.assertEqual(set(trophy_text.TEXT['zh']), set(trophies.BY_ID))
        for trophy in trophies.TROPHIES:
            name, description = trophy_text.text(trophy, 'zh')
            self.assertTrue(name.strip(), trophy[0])
            self.assertTrue(description.strip(), trophy[0])
            if trophy[0] != trophies.PLATINUM_ID:
                # The platinum keeps its English name, as the console does; everything else is translated.
                self.assertNotEqual(name, trophy[1], trophy[0])

    def test_unknown_language_falls_back_to_english(self):
        trophy = trophies.BY_ID[14]
        self.assertEqual(trophy_text.text(trophy, 'de'), (trophy[1], trophy[2]))
        self.assertEqual(trophy_text.text(trophy, ''), (trophy[1], trophy[2]))

    def test_partial_translation_falls_back_per_trophy(self):
        # A language may translate one trophy and leave the rest: the interface is per id.
        saved = trophy_text.TEXT.get('de')
        trophy_text.TEXT['de'] = {14: ('Gascoigne', 'Der Priester')}
        try:
            self.assertEqual(trophy_text.text(trophies.BY_ID[14], 'de'), ('Gascoigne', 'Der Priester'))
            self.assertEqual(trophy_text.text(trophies.BY_ID[15], 'de'),
                             (trophies.BY_ID[15][1], trophies.BY_ID[15][2]))
        finally:
            if saved is None:
                del trophy_text.TEXT['de']
            else:
                trophy_text.TEXT['de'] = saved

    def test_group_names(self):
        self.assertEqual(trophy_text.group(trophies.BASE, 'zh'), '血源诅咒')
        self.assertEqual(trophy_text.group(trophies.DLC, 'zh'), '老猎人')
        self.assertEqual(trophy_text.group(trophies.DLC, 'ru'), trophies.DLC)

    def test_coverage(self):
        self.assertEqual(trophy_text.coverage('zh'), (len(trophies.TROPHIES), len(trophies.TROPHIES)))
        self.assertEqual(trophy_text.coverage('de'), (0, len(trophies.TROPHIES)))
        # Traditional Chinese is generated from the Simplified table, so both are complete.
        self.assertEqual(trophy_text.LANGUAGES, ('zh', 'zh-hant'))


if __name__ == '__main__':
    unittest.main()
