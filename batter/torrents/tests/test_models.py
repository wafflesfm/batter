from __future__ import absolute_import, unicode_literals

import hashlib

from django.test import TestCase

from .local_settings import TEST_FILE_PATH
from ..models import Torrent


sha1 = lambda data: hashlib.sha1(data).hexdigest()


class TorrentTests(TestCase):
    def test_from_torrent_file(self):
        with open(TEST_FILE_PATH, 'rb') as test_file:
            torrent = Torrent.from_torrent_file(test_file)
            test_file.seek(0)
            orig_torrent_str = test_file.read()

        self.assertEquals(torrent.name, "archlinux-2013.04.01-dual.iso")
        self.assertEquals(torrent.to_bencoded_string(), orig_torrent_str)
        # note that the torrent file is slightly modified
        # I've removed the url-list dictionary element
        # since we have no support for that

    def test_to_torrent_singlefile(self):
        torrent = Torrent()
        torrent.name = "my.little.pwnie.zip"
        torrent.announce = "http://example.com/announce"
        torrent.piece_length = 32768
        torrent.pieces = "09bc090d67579eaed539c883b956d265a7975096"
        torrent.is_private = True
        torrent.length = 32768
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(
            sha1(torrent_str), b"4d9e46d46fcbd23d89c7e1366646a1ca7052a2bb")

    def test_to_torrent_singlefile_with_md5sum(self):
        torrent = Torrent()
        torrent.name = "my.little.pwnie.zip"
        torrent.announce = "http://example.com/announce"
        torrent.piece_length = 32768
        torrent.pieces = "09bc090d67579eaed539c883b956d265a7975096"
        torrent.is_private = True
        torrent.length = 32768
        torrent.md5sum = "0b784b963828308665f509173676bbcd"
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(
            sha1(torrent_str), b"fe1fcf4a3c635445d6f998b0fdfab652465099f0")

    def test_to_torrent_multifile(self):
        torrent = Torrent()
        torrent.name = "my.little.pwnies"
        torrent.announce = "http://example.com/announce"
        torrent.announce_list = [
            u'http://example.com/announce',
            u'http://backup1.example.com/announce'
        ]
        torrent.piece_length = 32768
        torrent.pieces = b"09bc090d67579eaed539c883b956d265a7975096"
        torrent.is_private = False
        torrent.length = None
        torrent.encoding = 'hex'
        torrent.files = [
            {
                'length': 235,
                'md5sum': b"0b784b963828308665f509173676bbcd",
                'path': ['dir1', 'dir2', 'file.ext'],
            },
            {
                'length': 435,
                'md5sum': b"784b0b963828308665f509173676bbcd",
                'path': ['moop.dir'],
            }
        ]
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(
            sha1(torrent_str), b"41c49ebb8d4aa7a977b9642da9512331a9abfe10")

    def test_torrent_unicode(self):
        torrent = Torrent()
        torrent.name = "hi"
        self.assertEquals(unicode(torrent), torrent.name)

    def test_absolute_url(self):
        # just poke it
        torrent = Torrent()
        torrent.id = 9
        torrent.get_absolute_url()
