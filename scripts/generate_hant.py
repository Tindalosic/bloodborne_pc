"""Write launcher/bbport_lang_hant.py: the Chinese table converted to Traditional.

The launcher's tables are parallel arrays of 195 + 47 English keys plus the
extra texts; hand-maintaining a second Chinese column would rot the moment
someone edits the Simplified one. This script converts whatever `bbport_lang`
holds for `zh` with OpenCC's Taiwan phrase table and writes a flat
English -> Traditional dictionary, which `bbport_lang.table('zh-hant')` layers
over the English texts.

    python scripts/generate_hant.py [--check]

`--check` exits 1 when the file on disk differs from what the tables produce,
so a test can keep it honest.
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'launcher'))

import bbport_lang  # noqa: E402

OUT = ROOT / 'launcher' / 'bbport_lang_hant.py'
TROPHY_OUT = ROOT / 'launcher' / 'bbport_trophy_text_hant.py'

HEADER = '''"""Traditional Chinese texts, generated from the Chinese table.

Do not edit by hand: run `python scripts/generate_hant.py` after changing the
Simplified texts (OpenCC s2twp keeps the Taiwan wording, e.g. 記憶卡 / 網路).
"""

TEXT = {
'''

TROPHY_HEADER = '''"""Traditional Chinese trophy texts, generated from the Simplified table.

Do not edit by hand: run `python scripts/generate_hant.py` after changing
`bbport_trophy_text.TEXT['zh']`.
"""

TEXT = {
'''

# OpenCC picks Taiwan wording, which is usually right, but a few phrases mean
# something else in this launcher (an exit "code" is an error number, not source).
OVERRIDES = (
    ('程式碼', '代碼'),
)


def convert(converter, value):
    text = converter.convert(value)
    for source, target in OVERRIDES:
        text = text.replace(source, target)
    return text


def table():
    from opencc import OpenCC

    converter = OpenCC('s2twp')
    source = bbport_lang.table('zh')
    rows = []
    for key in sorted(source):
        value = source[key]
        if not isinstance(value, str) or not value:
            continue
        converted = convert(converter, value)
        rows.append('    %r: %r,' % (key, converted))
    return HEADER + '\n'.join(rows) + '\n}\n'


def trophy_table():
    """`launcher/bbport_trophy_text_hant.py`: the trophy names and descriptions in Traditional."""
    from opencc import OpenCC

    import bbport_trophies as trophies
    import bbport_trophy_text as trophy_text

    converter = OpenCC('s2twp')
    rows = []
    for trophy_id in sorted(trophy_text.TEXT['zh']):
        name, text = trophy_text.TEXT['zh'][trophy_id]
        rows.append('    %d: (%r, %r),' % (trophy_id, convert(converter, name), convert(converter, text)))
    groups = []
    for name, text in sorted(trophy_text.GROUP_NAMES['zh'].items()):
        groups.append('    %r: %r,' % (name, convert(converter, text)))
    assert trophies.BASE in trophy_text.GROUP_NAMES['zh'], 'group names must cover both groups'
    return (TROPHY_HEADER + '\n'.join(rows) + '\n}\n\nGROUP_NAMES = {\n'
            + '\n'.join(groups) + '\n}\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = table()
    trophies = trophy_table()
    if args.check:
        stale = [path for path, expected in ((OUT, text), (TROPHY_OUT, trophies))
                 if (path.read_text(encoding='utf-8') if path.exists() else '') != expected]
        if stale:
            print('stale: %s (run python scripts/generate_hant.py)' % ', '.join(p.name for p in stale))
            return 1
        print('%d Traditional Chinese texts up to date' % text.count('\n    '))
        return 0
    OUT.write_text(text, encoding='utf-8')
    TROPHY_OUT.write_text(trophies, encoding='utf-8')
    print('wrote %s (%d texts)' % (OUT, text.count('\n    ')))
    print('wrote %s (%d trophies)' % (TROPHY_OUT, trophies.count('\n    ')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
