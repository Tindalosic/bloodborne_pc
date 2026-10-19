# SPDX-License-Identifier: GPL-2.0-or-later
"""Locale packs: launcher texts translated without touching the Python tables.

bbport_lang ships a translation for each launcher language as a list that has to stay the same
length as KEYS. A pack lifts that restriction: it is a JSON object in <folder>/<code>.json that
maps the English text to the translation, so anyone can add or correct strings by dropping one
file next to the launcher - no build, no key order, no complete list required.

Folders are read in order and the later one wins:
    1. locale/ next to the launcher (or launcher/locale/ in a source checkout) - ships with the app
    2. %APPDATA%/bbport-launcher/locale - the user's own corrections

Packs are re-read when the file changes, and a pack that does not parse is skipped: a broken
translation must never stop the launcher from opening.
"""
import json
import os
from pathlib import Path

PACK_SUFFIX = '.json'
_app = Path(__file__).resolve().parent


def folders():
    """The directories searched for packs, lowest priority first."""
    appdata = Path(os.environ.get('APPDATA') or Path.home())
    return (_app / 'locale', _app.parent / 'locale', appdata / 'bbport-launcher' / 'locale')


_cache = {}


def pack(language, search=None):
    """English text -> translation from <language>.json, {} when there is no usable pack."""
    merged = {}
    for folder in (folders() if search is None else search):
        path = folder / f'{language}{PACK_SUFFIX}'
        try:
            info = path.stat()
        except OSError:
            continue
        stamp = (str(path), info.st_mtime_ns, info.st_size)
        if stamp not in _cache:
            try:
                loaded = json.loads(path.read_text(encoding='utf-8'))
                # Only plain string pairs: a stray list or number would render as garbage.
                _cache[stamp] = {str(key): text for key, text in loaded.items()
                                 if isinstance(text, str) and text and not str(key).startswith('_')}
            except (OSError, ValueError, AttributeError):
                _cache[stamp] = {}
        merged.update(_cache[stamp])
    return merged


def merge(language, table, search=None):
    """The launcher's own table with the packs of this language laid over it."""
    if language in ('', 'en'):
        return table
    overlay = pack(language, search)
    return {**table, **overlay} if overlay else table


def template(language, table, keys):
    """A pack for the translator: every known key, with what is already translated.

    Keys without a translation stay empty, which pack() ignores, so an unfinished file is still
    a valid pack and can be filled in a few entries at a time.
    """
    return {key: table.get(key, '') for key in keys}
