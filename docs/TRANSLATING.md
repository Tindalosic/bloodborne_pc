# Translating the launcher

The launcher's own interface is translated in two layers:

1. **Built-in tables** in `launcher/bbport_lang.py` and `launcher/bbport_lang_more.py`. Each
   language is a list that must be exactly as long as `KEYS`, in the same order. Editing those
   is how a language is added to `LANGUAGE_NAMES`.
2. **Locale packs** in `locale/<code>.json` — a flat JSON object from the English text to the
   translation. This is the layer to use for corrections, new strings and languages we do not
   ship; it needs no rebuild and no knowledge of key order.

Packs are laid over the built-in tables, so a pack entry wins and a missing entry falls back to
what the tables already have. Search order (later wins):

| Folder | Use |
| --- | --- |
| `locale/` next to the launcher (`launcher/locale/` in a source checkout) | ships with the app |
| `%APPDATA%\bbport-launcher\locale` | your own corrections; survives updates |

`en` is the key language and ignores packs — the English text is the key, so a pack for it would
only shadow the source.

## Writing a pack

```json
{
  "Quit": "退出",
  "Third-party patches": "第三方补丁"
}
```

Values must be non-empty strings. Empty values, other types and keys starting with `_` are
ignored, so a pack can be filled in a few entries at a time and comments can be written as
`"_note": "..."`. A file that does not parse is skipped: a broken pack never stops the launcher
from opening.

Packs are re-read when the file changes, so edits apply on the next window or language switch —
no restart, no rebuild.

## Getting the full list of texts

```sh
python scripts/export_locale.py zh              # locale/zh.json, with what we already have
python scripts/export_locale.py de --out de.json
```

The template contains every key, filled with the current translation where there is one. Fill the
empty ones, copy the file into `locale/`, done.

## Achievement texts

Trophy names and descriptions are not in the launcher tables: they are the game's own text, so
they live in `launcher/bbport_trophy_text.py` as `TEXT[language][trophy id] = (name, description)`.
Simplified Chinese covers all 40 trophies (names as the PS4 release shows them, descriptions from
the official Chinese release). A language that is missing, or that has not translated a given
trophy, falls back to English per trophy — there is no all-or-nothing requirement.

## Traditional Chinese is generated

`zh-hant` is not maintained by hand: it is the Simplified table converted with OpenCC's `s2twp`
phrase table (Taiwan wording) plus a small override list, written to `launcher/bbport_lang_hant.py`
and `launcher/bbport_trophy_text_hant.py`. After editing any Simplified text:

```sh
python scripts/generate_hant.py           # rewrite both generated files
python scripts/generate_hant.py --check   # CI-style check that they are not stale
```

OpenCC is a build-time dependency only (`pip install opencc`); the launcher reads the generated
dictionaries, so players never need it. Editing `bbport_lang_hant.py` by hand is pointless — the
next generation overwrites it.
