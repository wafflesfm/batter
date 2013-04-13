import os.path
import hashlib

from django.test import TestCase

from .. import models

Torrent = models.Torrent


class TorrentTests(TestCase):
    def sha1(self, data):
        sha = hashlib.sha1()
        sha.update(data)
        return sha.hexdigest()

    def test_from_torrent_file(self):
        with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'archlinux-2013.04.01-dual.iso.torrent'
            ),
            'rb'
        ) as test_file:
            torrent = Torrent.from_torrent_file(test_file)
            test_file.seek(0)
            orig_torrent_str = test_file.read()
        self.assertEquals(torrent.name, "archlinux-2013.04.01-dual.iso")
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(torrent_str, orig_torrent_str)
        # note that the torrent file is slightly modified
        # I've removed the url-list dictionary element
        # since we have no support for that

    def test_to_torrent_singlefile(self):
        torrent = Torrent()
        torrent.name = u"my.little.pwnie.zip"
        torrent.announce = u"http://example.com/announce"
        torrent.piece_length = 32768
        torrent.pieces = u"09bc090d67579eaed539c883b956d265a7975096"
        torrent.private = True
        torrent.length = 32768
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(
            self.sha1(torrent_str),
            "4d9e46d46fcbd23d89c7e1366646a1ca7052a2bb"
        )

    def test_to_torrent_singlefile_with_md5sum(self):
        torrent = Torrent()
        torrent.name = u"my.little.pwnie.zip"
        torrent.announce = u"http://example.com/announce"
        torrent.piece_length = 32768
        torrent.pieces = u"09bc090d67579eaed539c883b956d265a7975096"
        torrent.private = True
        torrent.length = 32768
        torrent.md5sum = "0b784b963828308665f509173676bbcd"
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(
            self.sha1(torrent_str),
            "fe1fcf4a3c635445d6f998b0fdfab652465099f0"
        )

    def test_to_torrent_multifile(self):
        torrent = Torrent()
        torrent.name = u"my.little.pwnies"
        torrent.announce = u"http://example.com/announce"
        torrent.announce_list = [
            u'http://example.com/announce',
            u'http://backup1.example.com/announce'
        ]
        torrent.piece_length = 32768
        torrent.pieces = u"09bc090d67579eaed539c883b956d265a7975096"
        torrent.private = False
        torrent.length = None
        torrent.encoding = 'hex'
        torrent.files = [
            {
                'length': 235,
                'md5sum': "0b784b963828308665f509173676bbcd",
                'path': ['dir1', 'dir2', 'file.ext'],
            },
            {
                'length': 435,
                'md5sum': "784b0b963828308665f509173676bbcd",
                'path': ['moop.dir'],
            }
        ]
        torrent_str = torrent.to_bencoded_string()  # this shouldn't throw
        self.assertEquals(
            self.sha1(torrent_str),
            "41c49ebb8d4aa7a977b9642da9512331a9abfe10"
        )

    def test_torrent_unicode(self):
        torrent = Torrent()
        torrent.name = u"hi"
        self.assertEquals(unicode(torrent), torrent.name)

    def test_absolute_url(self):
        # just poke it
        torrent = Torrent()
        torrent.id = 9
        torrent.get_absolute_url()


class ConvertHelperTest(TestCase):
    def test_str(self):
        self.assertIsInstance(models.convert("hi"), str)

    def test_unicode(self):
        self.assertIsInstance(models.convert(u"hi"), str)
        self.assertNotIsInstance(models.convert(u"hi"), unicode)

    def test_list(self):
        converted = models.convert([u"hi", "zoop"])
        for converted_str in converted:
            self.assertIsInstance(converted_str, str)

    def test_dictionary(self):
        converted = models.convert({
            u"uu": u"uudata",
            u"us": "usdata",
            "su": u"sudata",
            "ss": "ssdata"
        })
        for converted_key, converted_value in converted.items():
            self.assertIsInstance(converted_key, str)
            self.assertIsInstance(converted_value, str)
