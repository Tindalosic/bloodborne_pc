"""Release lookups when GitHub's API refuses (launcher/bbport_launcher_win.py).

The anonymous API allows 60 requests an hour for the whole address a player shares with their
household, so a released launcher can be told "rate limit exceeded" while doing nothing wrong.
These tests pin the fallback: the same versions and the same zip links come from github.com's
own pages, and a version is looked up once rather than on every click.
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

from paths import ROOT

if str(ROOT / 'launcher') not in sys.path:
    sys.path.insert(0, str(ROOT / 'launcher'))

import bbport_channels as channels  # noqa: E402
import bbport_launcher_win as launcher  # noqa: E402


FEED = b'''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>tag:github.com,2008:Repository/1/windows-v1.9.4</id>
    <link rel="alternate" type="text/html"
          href="https://github.com/Supermedo/bloodborne_pc/releases/tag/windows-v1.9.4"/>
  </entry>
  <entry>
    <id>tag:github.com,2008:Repository/1/windows-v1.9.3</id>
    <link rel="alternate" type="text/html"
          href="https://github.com/Supermedo/bloodborne_pc/releases/tag/windows-v1.9.3"/>
  </entry>
</feed>
'''

ASSETS = (b'<div><a href="/Supermedo/bloodborne_pc/releases/download/windows-v1.9.4/'
          b'Bloodborne-Windows.zip">Bloodborne-Windows.zip</a>'
          b'<a href="/Supermedo/bloodborne_pc/releases/download/windows-v1.9.4/'
          b'fsr4vk-v0.4.3-amdfix-src.zip">src</a></div>')


class Response:
    def __init__(self, body):
        self.body = body

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


def target(url):
    """The address behind a urlopen argument, which is a Request object for the API calls."""
    return getattr(url, 'full_url', url) or str(url)


def refusing(url, *_args, **_kwargs):
    """urlopen stand-in: the API is out of quota, the pages on github.com are not."""
    address = target(url)
    if 'api.github.com' in address:
        raise launcher.urllib.error.HTTPError(address, 403, 'rate limit exceeded', None, None)
    if 'releases.atom' in address:
        return Response(FEED)
    if 'expanded_assets' in address:
        return Response(ASSETS)
    raise AssertionError('unexpected URL %s' % address)


class FallbackTests(unittest.TestCase):
    def setUp(self):
        launcher.RELEASE_CACHE.clear()

    def tearDown(self):
        launcher.RELEASE_CACHE.clear()

    def test_the_newest_version_comes_from_the_feed_when_the_api_is_rate_limited(self):
        with mock.patch.object(launcher.urllib.request, 'urlopen', refusing):
            version, url, page = launcher.latest_release('upstream')
        self.assertEqual(version, '1.9.4')
        self.assertEqual(url, 'https://github.com/Supermedo/bloodborne_pc/releases/download/'
                              'windows-v1.9.4/Bloodborne-Windows.zip')
        self.assertTrue(page.endswith('/releases/tag/windows-v1.9.4'))

    def test_the_version_list_survives_a_rate_limit_and_skips_the_old_ones(self):
        with mock.patch.object(launcher.urllib.request, 'urlopen', refusing):
            found = launcher.installable_releases('upstream')
        self.assertEqual([item[0] for item in found], ['1.9.4', '1.9.3'])
        self.assertTrue(all(item[1].endswith('.zip') for item in found))

    def test_the_zip_link_is_the_first_zip_of_the_release_not_a_side_asset(self):
        with mock.patch.object(launcher.urllib.request, 'urlopen', refusing):
            url = launcher.web_assets(channels.of('upstream'), 'windows-v1.9.4')
        self.assertTrue(url.endswith('/windows-v1.9.4/Bloodborne-Windows.zip'))

    def test_a_channel_is_looked_up_once_and_then_remembered(self):
        calls = []

        def counting(url, *args, **kwargs):
            calls.append(target(url))
            return refusing(url, *args, **kwargs)

        with mock.patch.object(launcher.urllib.request, 'urlopen', counting):
            launcher.latest_release('upstream')
            launcher.latest_release('upstream')
        api_calls = [url for url in calls if 'api.github.com' in url]
        self.assertEqual(len(api_calls), 1)

    def test_the_feed_still_names_the_versions_when_a_release_has_no_zip(self):
        empty = b'<div>no assets here</div>'

        def without_assets(url, *_args, **_kwargs):
            if 'expanded_assets' in target(url):
                return Response(empty)
            return refusing(url)

        with mock.patch.object(launcher.urllib.request, 'urlopen', without_assets):
            self.assertIsNone(launcher.web_assets(channels.of('upstream'), 'windows-v1.9.4'))


if __name__ == '__main__':
    unittest.main()
