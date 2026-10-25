"""Which repository an installation follows, and where it keeps its data.

Two small text files next to Bloodborne.exe make an installation portable:

- ``channel.txt`` names the release channel (``fork`` or ``upstream``). It decides which GitHub
  repository the launcher asks for updates, so an upstream build never offers a fork release and
  a fork build never offers an upstream one, without either repository's code being edited.
- ``data-dir.txt`` holds the folder for saves, mods, patches, bbport.ini and the shader caches.
  Pointing two installations at the same folder lets them be switched between without moving
  anything: each keeps its own binaries and both read the same player data.

Both files are in the launcher's USER_FILES, so an update copies neither over nor away and a
channel choice survives it. Neither is required: without them an installation follows ``fork``
and keeps its data next to the executable, which is what unzipping a release gives.
"""
import os
from pathlib import Path

DEFAULT = 'fork'

CHANNELS = {
    'fork': {
        'label': 'This fork (Tindalosic)',
        'repo': 'Tindalosic/bloodborne_pc',
        'project': 'https://github.com/Tindalosic/bloodborne_pc',
        'api': 'https://api.github.com/repos/Tindalosic/bloodborne_pc/releases/latest',
        'list': 'https://api.github.com/repos/Tindalosic/bloodborne_pc/releases?per_page=100',
        'page': 'https://github.com/Tindalosic/bloodborne_pc/releases/latest',
        'oldest': '2.0.0',
    },
    'upstream': {
        'label': 'Upstream (Supermedo)',
        'repo': 'Supermedo/bloodborne_pc',
        'project': 'https://github.com/Supermedo/bloodborne_pc',
        'api': 'https://api.github.com/repos/Supermedo/bloodborne_pc/releases/latest',
        'list': 'https://api.github.com/repos/Supermedo/bloodborne_pc/releases?per_page=100',
        'page': 'https://github.com/Supermedo/bloodborne_pc/releases/latest',
        'oldest': '1.8.2',
    },
}

# In the order the Advanced page lists them: this build first.
ORDER = ('fork', 'upstream')


def of(name):
    """The release facts of one channel ({}, as a dict, for an unknown name)."""
    return CHANNELS.get(name) or CHANNELS[DEFAULT]


def other(name):
    """The channel a side-by-side installation would hold."""
    return 'upstream' if name == 'fork' else 'fork'


def channel_marker(port_dir):
    return Path(port_dir) / 'channel.txt'


def data_marker(port_dir):
    return Path(port_dir) / 'data-dir.txt'


def read(port_dir):
    """The channel this installation follows."""
    try:
        name = channel_marker(port_dir).read_text(encoding='utf-8').strip()
    except OSError:
        return DEFAULT
    return name if name in CHANNELS else DEFAULT


def save(port_dir, name):
    """Write the channel down and return it (the installer calls this for a new installation)."""
    if name not in CHANNELS:
        raise ValueError(name)
    path = channel_marker(port_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(name + '\n', encoding='utf-8')
    return name


def data_dir(port_dir):
    """Where saves, mods, patches and the ini live for this installation."""
    from_env = os.environ.get('BB_DATA_DIR')
    if from_env:
        return Path(from_env)
    try:
        written = data_marker(port_dir).read_text(encoding='utf-8').strip()
    except OSError:
        written = ''
    if written:
        folder = Path(os.path.expandvars(written)).expanduser()
        if folder.is_dir():
            return folder
    return Path(port_dir)


def save_data_dir(port_dir, folder):
    """Share `folder` with the other installations ('' restores the folder of this one)."""
    path = data_marker(port_dir)
    folder = str(folder or '').strip()
    if not folder:
        try:
            path.unlink()
        except OSError:
            pass
        return Path(port_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(folder + '\n', encoding='utf-8')
    return Path(folder)
