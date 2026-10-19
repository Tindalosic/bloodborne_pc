"""The community patch catalogue (shadPS4 / GoldHEN XML) behind the launcher's Third-party patches
list.

The catalogue file ships next to the game's own patches, so a fresh install already lists every
community patch and cheat with nothing to download. Refreshing it replaces that file with the
current list from shadps4-emu/ps4_cheats, keeping the previous copy next to it as a .bak, and
leaves the user's own XML files and their selections alone.
"""
import base64
import json
import shutil
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import patches

REPO = 'shadps4-emu/ps4_cheats'
REPO_PATH = 'PATCHES/Bloodborne.xml'
API_URL = f'https://api.github.com/repos/{REPO}/contents/{REPO_PATH}?ref=main'
RAW_URL = f'https://raw.githubusercontent.com/{REPO}/main/{REPO_PATH}'
# The file the launcher lists first: shipped with the app, replaced by refresh().
CATALOGUE = 'shadps4-Bloodborne.xml'
USER_AGENT = 'bloodborne-pc-launcher'


def catalogue_path(patches_dir):
    return Path(patches_dir) / CATALOGUE


def _get(url, timeout=20):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch(timeout=20):
    """(bytes, source) of the newest community file: the contents API, then the raw file."""
    errors = []
    for url in (API_URL, RAW_URL):
        try:
            data = _get(url, timeout)
        except OSError as error:
            errors.append(f'{url}: {error}')
            continue
        if url == API_URL:
            try:
                data = base64.b64decode(json.loads(data)['content'])
            except (ValueError, KeyError, TypeError):
                errors.append(f'{url}: not a file payload')
                continue
        return data, url
    raise RuntimeError('download failed: ' + '; '.join(errors))


def check(data):
    """Number of Bloodborne 1.09 patches in data; ValueError when it is not that file."""
    from patches import BLOODBORNE_IDS, xml_body
    try:
        root = ET.fromstring(xml_body(data))
    except ET.ParseError as error:
        raise ValueError(f'not an XML file: {error}')
    ids = {e.text.strip() for e in root.iter('ID') if e.text}
    if ids and not ids & BLOODBORNE_IDS:
        raise ValueError('the file is for another game: ' + ', '.join(sorted(ids)[:3]))
    names = [m.get('Name') for m in root.iter('Metadata') if m.get('AppVer') == '01.09']
    if len(names) < 10:
        raise ValueError(f'only {len(names)} patches for version 1.09')
    return len(names)


def install(patches_dir, data=None):
    """Replaces the catalogue file; returns (path, patch count, backup or None).

    A bad download never touches the file that is already there: the bytes are validated first.
    """
    path = catalogue_path(patches_dir)
    data = fetch()[0] if data is None else data
    count = check(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if path.is_file():
        backup = path.with_suffix(f'.xml.bak-{time.strftime("%Y%m%d-%H%M%S")}')
        shutil.copy2(path, backup)
    temporary = path.with_suffix('.xml.part')
    temporary.write_bytes(b'<?xml version="1.0" encoding="utf-8"?>\n'
                          + patches.xml_body(data))
    temporary.replace(path)
    return path, count, backup


def describe(path):
    """(patch count, file mtime or None) of the catalogue on disk, without raising."""
    path = Path(path)
    try:
        root = ET.fromstring(patches.xml_body(path.read_bytes()))
    except (OSError, ET.ParseError):
        return 0, None
    names = [m.get('Name') for m in root.iter('Metadata') if m.get('AppVer') == '01.09']
    return len(names), path.stat().st_mtime
