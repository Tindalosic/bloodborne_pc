"""The launcher's colour, type and glyph helpers."""

import sys
import unittest

from paths import ROOT

sys.path.insert(0, str(ROOT / 'launcher'))

import bbport_theme as theme  # noqa: E402


class ColourTest(unittest.TestCase):
    def test_blend_reaches_both_ends(self):
        self.assertEqual(theme.blend('#000000', '#ffffff', 0), '#000000')
        self.assertEqual(theme.blend('#000000', '#ffffff', 1), '#ffffff')

    def test_blend_midpoint_is_half_way(self):
        self.assertEqual(theme.blend('#000000', '#ffffff', 0.5), '#808080')

    def test_blend_clamps_out_of_range_values(self):
        self.assertEqual(theme.blend('#102030', '#102030', -5), '#102030')
        self.assertEqual(theme.blend('#102030', '#102030', 5), '#102030')

    def test_gradient_keeps_both_ends(self):
        ramp = theme.gradient('#000000', '#ffffff', 5)
        self.assertEqual(len(ramp), 5)
        self.assertEqual(ramp[0], '#000000')
        self.assertEqual(ramp[-1], '#ffffff')

    def test_gradient_never_returns_nothing(self):
        self.assertEqual(theme.gradient('#000000', '#ffffff', 0), ['#000000'])

    def test_gradient_moves_one_way(self):
        values = [int(c[1:3], 16) for c in theme.gradient('#000000', '#ffffff', 9)]
        self.assertEqual(values, sorted(values))


class TypeTest(unittest.TestCase):
    def test_tracked_spaces_the_letters(self):
        self.assertEqual(theme.tracked('AB', 1), 'A B')
        self.assertEqual(theme.tracked('ABC', 2), 'A  B  C')

    def test_tracked_leaves_short_text_alone(self):
        self.assertEqual(theme.tracked('A', 1), 'A')
        self.assertEqual(theme.tracked('', 1), '')

    def test_pick_family_prefers_the_first_available(self):
        available = {'Georgia', 'Consolas'}
        self.assertEqual(theme.pick_family(available, theme.DISPLAY_FAMILIES, 'TkDefaultFont'), 'Georgia')
        self.assertEqual(theme.pick_family(available, theme.MONO_FAMILIES, 'TkFixedFont'), 'Consolas')

    def test_pick_family_falls_back_when_nothing_matches(self):
        self.assertEqual(theme.pick_family(set(), theme.MONO_FAMILIES, 'TkFixedFont'), 'TkFixedFont')

    def test_fonts_uses_the_cjk_family_for_chinese(self):
        families = theme.fonts(None, 'zh', available={'Microsoft YaHei UI', 'Georgia', 'Consolas'})
        self.assertTrue(families['cjk'])
        self.assertEqual(families['body'], 'Microsoft YaHei UI')
        self.assertEqual(families['display'], 'Georgia')

    def test_fonts_uses_the_latin_family_otherwise(self):
        families = theme.fonts(None, 'ru', available={'Segoe UI', 'Constantia'})
        self.assertFalse(families['cjk'])
        self.assertEqual(families['body'], 'Segoe UI')
        self.assertEqual(families['display'], 'Constantia')


class PaletteTest(unittest.TestCase):
    def test_every_colour_is_a_hex_triplet(self):
        for name in dir(theme):
            if name.isupper() and isinstance(getattr(theme, name), str):
                value = getattr(theme, name)
                if value.startswith('#') and len(value) == 7:
                    int(value[1:], 16)

    def test_the_window_still_shares_the_old_names(self):
        for name in ('BG', 'PANEL', 'CARD', 'LINE', 'TEXT', 'MUTED', 'GOLD',
                     'BLOOD', 'BLOOD_HI', 'NAV_HOVER', 'GOLD_HI', 'HAIRLINE'):
            self.assertTrue(hasattr(theme, name), name)


if __name__ == '__main__':
    unittest.main()
