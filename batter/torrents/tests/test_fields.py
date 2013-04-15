from __future__ import absolute_import, unicode_literals

import cStringIO as StringIO

from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File

from ..fields import TorrentField


class TorrentFieldTests(TestCase):
    def test_empty(self):
        field = TorrentField()
        self.assertRaises(ValidationError, field.clean, False)

    def test_creates_torrent(self):
        torrent_file_raw = open(settings.TEST_FILE_PATH, 'rb')
        torrent_data = torrent_file_raw.read()
        torrent_file_raw.seek(0)

        torrent_file = File(torrent_file_raw)
        field = TorrentField()
        torrent = field.clean(torrent_file)

        self.assertEquals(torrent_data, torrent.to_bencoded_string())

    def test_invalid_torrent(self):
        field = TorrentField()
        not_a_torrent = File(StringIO.StringIO(
            "this is clearly an invalid torrent"
        ))
        not_a_torrent.name = "invalid.torrent"
        self.assertRaises(ValidationError, field.clean, not_a_torrent)
