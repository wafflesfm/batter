from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse

from batter.test import LoggedInTestCase

from .local_settings import TEST_FILE_PATH
from ..models import Torrent


class UploadTorrentTests(LoggedInTestCase):
    def setUp(self):
        self.url = reverse("torrents_upload")
        super(UploadTorrentTests, self).setUp()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_valid_torrent(self):
        with open(TEST_FILE_PATH, 'rb') as fp:
            response = self.client.post(self.url, {'torrent_file': fp})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Torrent.objects.count(), 1)

    def test_post_duplicate_torrent(self):
        with open(TEST_FILE_PATH, 'rb') as fp:
            self.client.post(self.url, {'torrent_file': fp})
            fp.seek(0)
            response = self.client.post(self.url, {'torrent_file': fp})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Torrent.objects.count(), 1)

    def test_logged_out(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)


class ViewTorrentTests(LoggedInTestCase):
    def setUp(self):
        with open(TEST_FILE_PATH, 'rb') as test_file:
            self.torrent = Torrent.from_torrent_file(test_file)

        self.torrent.save()
        self.torrent_url = reverse("torrents_view", kwargs={
            'pk': self.torrent.pk
        })
        super(ViewTorrentTests, self).setUp()

    def test_existing_torrent(self):
        response = self.client.get(self.torrent_url)
        self.assertEquals(response.status_code, 200)

    def test_nonexisting_torrent(self):
        response = self.client.get(reverse("torrents_view", kwargs={
            'pk': 9001
        }))
        self.assertEquals(response.status_code, 404)


class GenerateTorrentTests(LoggedInTestCase):
    def setUp(self):
        with open(TEST_FILE_PATH, 'rb') as test_file:
            self.torrent = Torrent.from_torrent_file(test_file)
            self.torrent_size = test_file.tell()
            test_file.seek(0)
            self.raw_torrent = test_file.read()
        self.torrent.save()
        self.torrent_url = reverse("torrents_generate", kwargs={
            'pk': self.torrent.pk
        })
        super(GenerateTorrentTests, self).setUp()

    def test_existing_torrent(self):
        response = self.client.get(self.torrent_url)
        self.assertEquals(
            int(response['Content-Length']),
            int(self.torrent_size)
        )
        self.assertEquals(
            response['Content-Disposition'],
            'attachment; filename=archlinux-20130401-dualiso.torrent'
        )
        self.assertEquals(response.content, self.raw_torrent)

    def test_nonexisting_torrent(self):
        response = self.client.get(reverse("torrents_generate", kwargs={
            'pk': 9001
        }))
        self.assertEquals(response.status_code, 404)
