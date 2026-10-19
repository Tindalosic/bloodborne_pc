#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Writes a locale pack template: every launcher text in English, with the translations we have.

    python scripts/export_locale.py zh                  # -> locale/zh.json
    python scripts/export_locale.py de --out my.json    # for a language we do not ship

The file is a valid pack as it stands: empty values are ignored, so it can be filled in a few
entries at a time and dropped into locale/ (or %APPDATA%/bbport-launcher/locale to override).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'launcher'))
import bbport_lang  # noqa: E402
import bbport_locale  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('language', help='launcher language code, e.g. zh, ja, de')
    parser.add_argument('--out', type=Path, help='file to write (default: locale/<language>.json)')
    arguments = parser.parse_args()
    keys = list(bbport_lang.KEYS) + list(bbport_lang.MORE_KEYS)
    table = bbport_lang.table(arguments.language)
    out = arguments.out or Path(__file__).resolve().parent.parent / 'locale' / f'{arguments.language}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    pack = bbport_locale.template(arguments.language, table, keys)
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    done = sum(1 for text in pack.values() if text)
    print(f'{out}: {done} of {len(keys)} texts translated')


if __name__ == '__main__':
    main()
