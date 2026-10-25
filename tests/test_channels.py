"""Release channel and shared data folder checks (launcher/bbport_channels.py).

The two marker files are what let an upstream build and this fork's build sit side by side, follow
their own repository for updates and read the same saves, so the rules below are the contract:
defaults without markers, one channel per installation, a data folder that has to exist, and the
environment beating both files.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

from paths import ROOT

if str(ROOT / 'launcher') not in sys.path:
    sys.path.insert(0, str(ROOT / 'launcher'))

import bbport_channels as channels  # noqa: E402


class ChannelTests(unittest.TestCase):
    def setUp(self):
        self.port = Path(tempfile.mkdtemp(prefix='bbport-channel-'))
        self._saved = os.environ.pop('BB_DATA_DIR', None)

    def tearDown(self):
        if self._saved is not None:
            os.environ['BB_DATA_DIR'] = self._saved

    def test_an_untouched_installation_follows_the_fork_and_keeps_its_own_data(self):
        # Unzipping a release gives no markers: that must already be a working installation.
        self.assertEqual(channels.read(self.port), 'fork')
        self.assertEqual(channels.data_dir(self.port), self.port)

    def test_the_two_channels_point_at_different_repositories(self):
        fork, upstream = channels.of('fork'), channels.of('upstream')
        self.assertNotEqual(fork['repo'], upstream['repo'])
        self.assertNotEqual(fork['api'], upstream['api'])
        self.assertNotEqual(fork['list'], upstream['list'])
        # They never offer each other's releases, so their version series must not overlap.
        self.assertEqual(upstream['oldest'], '1.8.2')
        self.assertNotEqual(fork['oldest'], upstream['oldest'])

    def test_a_channel_survives_a_reopen_and_an_unknown_name_falls_back(self):
        channels.save(self.port, 'upstream')
        self.assertEqual(channels.read(self.port), 'upstream')
        (self.port / 'channel.txt').write_text('nonsense\n', encoding='utf-8')
        self.assertEqual(channels.read(self.port), 'fork')
        self.assertEqual(channels.of('nonsense')['repo'], channels.of('fork')['repo'])

    def test_save_refuses_a_name_that_is_not_a_channel(self):
        with self.assertRaises(ValueError):
            channels.save(self.port, 'somewhere-else')

    def test_other_returns_the_one_it_is_not(self):
        self.assertEqual(channels.other('fork'), 'upstream')
        self.assertEqual(channels.other('upstream'), 'fork')

    def test_a_shared_data_folder_applies_to_both_installations(self):
        shared = self.port / 'shared'
        shared.mkdir()
        other = self.port / 'second'
        other.mkdir()
        channels.save_data_dir(self.port, shared)
        channels.save_data_dir(other, shared)
        self.assertEqual(channels.data_dir(self.port), shared)
        self.assertEqual(channels.data_dir(other), shared)
        # Emptying the marker restores the installation's own folder.
        channels.save_data_dir(self.port, '')
        self.assertEqual(channels.data_dir(self.port), self.port)
        self.assertFalse((self.port / 'data-dir.txt').exists())

    def test_a_data_folder_that_was_deleted_or_renamed_is_not_used(self):
        # An unplugged drive must not silently become the data folder: fall back, do not crash.
        channels.save_data_dir(self.port, self.port / 'gone')
        self.assertEqual(channels.data_dir(self.port), self.port)

    def test_the_environment_beats_both_markers(self):
        shared = self.port / 'shared'
        shared.mkdir()
        channels.save_data_dir(self.port, shared)
        from_env = self.port / 'from-env'
        from_env.mkdir()
        os.environ['BB_DATA_DIR'] = str(from_env)
        self.assertEqual(channels.data_dir(self.port), from_env)


class WiringTests(unittest.TestCase):
    """The launcher takes its version and its repository links from the channel table.

    Keeping these apart is what lets an upstream release appear without editing this repository: the
    launcher reads the repository to ask from channel.txt, not from a constant. These checks catch the
    two ways that breaks - a version number that is not in the series the fork publishes, and links
    that drifted from the table."""

    @classmethod
    def setUpClass(cls):
        cls._saved = os.environ.pop('BB_DATA_DIR', None)
        import bbport_launcher_win as launcher
        cls.launcher = launcher

    @classmethod
    def tearDownClass(cls):
        if cls._saved is not None:
            os.environ['BB_DATA_DIR'] = cls._saved

    def test_the_fork_publishes_above_its_oldest_installable_version(self):
        # An older VERSION would be filtered out of its own "Other versions" list and shown as not
        # installed in a window that is running it.
        fork = channels.of('fork')
        self.assertGreaterEqual(self.launcher.version_tuple(self.launcher.VERSION),
                                self.launcher.version_tuple(fork['oldest']))

    def test_a_fork_version_never_looks_like_an_upstream_one(self):
        # The two series must be told apart by number alone, or a switch compares releases of
        # different repositories and offers a downgrade that is really an upgrade.
        fork = channels.of('fork')['oldest']
        upstream = channels.of('upstream')['oldest']
        self.assertGreater(self.launcher.version_tuple(fork), self.launcher.version_tuple(upstream))

    def test_the_links_come_from_the_channel_table(self):
        self.assertEqual(self.launcher.PROJECT_URL, channels.of('upstream')['project'])
        self.assertEqual(self.launcher.FORK_URL, channels.of('fork')['project'])
        self.assertEqual(self.launcher.UPSTREAM_RELEASES_PAGE, channels.of('upstream')['page'])

    def test_this_build_is_based_on_a_named_upstream_release(self):
        # The About page names it, and it must be a release the upstream repository has published.
        self.assertEqual(self.launcher.UPSTREAM_BASE, '1.9.2')

    def test_a_release_tag_becomes_the_version_that_is_compared(self):
        self.assertEqual(self.launcher.version_tuple('windows-v2.0.1'), (2, 0, 1))
        self.assertGreater(self.launcher.version_tuple('windows-v2.0.1'),
                           self.launcher.version_tuple('windows-v1.9.4'))


if __name__ == '__main__':
    unittest.main()
