"""Artwork the window shows, and where it comes from.

The repository ships no pictures: the banner is the player's own dump
(``sce_sys/pic1.png``), and anything else is whatever the player drops into the
``art`` folder. SteamGridDB is a good place to look for a Bloodborne hero or
grid image — save it as ``hero.png`` (banner) or ``empty.png`` (empty states)
and it is picked up on the next launch. Nothing is bundled and nothing is
uploaded, so the GPL repository never carries someone else's artwork.
"""

from __future__ import annotations

import os
from pathlib import Path

# Names the launcher looks for, in order of preference.
KINDS = ('hero', 'empty')
SUFFIXES = ('.png', '.jpg', '.jpeg', '.webp')
GALLERY = 'https://www.steamgriddb.com/search/grids?term=bloodborne'

_cache: dict[tuple[str, str], tuple[int, Path | None]] = {}


def folders(data_dir: str | os.PathLike[str] | None = None,
            appdata: str | os.PathLike[str] | None = None) -> list[Path]:
    """Where artwork is looked for, most specific first."""
    if data_dir is None:
        data_dir = os.environ.get('BB_DATA_DIR') or Path(__file__).resolve().parent.parent
    if appdata is None:
        appdata = os.environ.get('APPDATA') or Path.home()
    return [Path(data_dir) / 'art', Path(appdata) / 'bbport-launcher' / 'art']


def find(kind: str, data_dir=None, appdata=None) -> Path | None:
    """The first picture called ``kind`` in any artwork folder, or None."""
    for folder in folders(data_dir, appdata):
        try:
            stamp = folder.stat().st_mtime_ns
        except OSError:
            continue
        key = (str(folder), kind)
        cached = _cache.get(key)
        if cached and cached[0] == stamp:
            found = cached[1]
            if found and found.exists():
                return found
            if not found:
                continue
        match = None
        for entry in sorted(folder.iterdir()):
            if entry.is_file() and entry.stem.lower() == kind and entry.suffix.lower() in SUFFIXES:
                match = entry
                break
        _cache[key] = (stamp, match)
        if match:
            return match
    return None


def touch(kind: str, data_dir=None, appdata=None) -> Path:
    """The path a player should save ``kind`` to (the most specific folder)."""
    folder = folders(data_dir, appdata)[0]
    return folder / f'{kind}.png'


def folder(data_dir=None, appdata=None) -> Path:
    """The folder the launcher reads first; shown in the window so it is findable."""
    return folders(data_dir, appdata)[0]
