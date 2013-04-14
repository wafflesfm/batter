from django.test import TestCase
from django.contrib.auth.models import User

import torrents.models
import torrents.tests

from .. import models


class BaseTestCase(TestCase):
    def setUp(self):
        with open(torrents.tests.TEST_FILE_PATH, 'rb') as fp:
            self.ex_torrent = torrents.models.Torrent.from_torrent_file(fp)
            fp.seek(0)
            self.ex_torrent2 = torrents.models.Torrent.from_torrent_file(fp)
            self.ex_torrent2.pieces += 'q'  # or not unique
        self.ex_torrent.save()
        self.ex_torrent2.save()

        self.boring_group = models.BoringGroup()
        self.boring_group.save()
        self.exciting_group = models.ExcitingGroup()
        self.exciting_group.save()

        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )

        self.boring_upload = models.BoringUpload(
            uploader=self.samantha,
            torrent=self.ex_torrent,
            parent=self.boring_group
        )
        self.boring_upload.save()

        self.exciting_upload = models.ExcitingUpload(
            uploader=self.samantha,
            torrent=self.ex_torrent2,
            parent=self.exciting_group,
            is_exciting=False
        )
        self.exciting_upload.save()


class UploadTests(BaseTestCase):
    def test_can_get_parent(self):
        u = torrents.models.Upload.base_objects.get(torrent=self.ex_torrent)
        u2 = torrents.models.Upload.base_objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(u, torrents.models.Upload)
        self.assertIsInstance(u2, torrents.models.Upload)
        self.assertNotIsInstance(u, models.BoringUpload)
        self.assertNotIsInstance(u2, models.ExcitingUpload)

    def test_gets_boring(self):
        bu = torrents.models.Upload.objects.get(torrent=self.ex_torrent)
        self.assertIsInstance(bu, models.BoringUpload)
        self.assertEquals(bu, self.boring_upload)

    def test_gets_exciting(self):
        eu = torrents.models.Upload.objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(eu, models.ExcitingUpload)
        self.assertEquals(eu, self.exciting_upload)
        self.assertEquals(eu.is_exciting, False)

    def test_modifies_exciting(self):
        self.exciting_upload.is_exciting = True
        self.exciting_upload.save()
        eu = torrents.models.Upload.objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(eu, models.ExcitingUpload)
        self.assertEquals(eu, self.exciting_upload)
        self.assertEquals(eu.is_exciting, True)

    def test_get_from_torrent(self):
        self.assertEquals(self.ex_torrent.upload, self.boring_upload)
        self.assertEquals(self.ex_torrent2.upload, self.exciting_upload)

    def test_set_from_torrent(self):
        self.ex_torrent2.upload.is_exciting = True
        self.ex_torrent2.upload.save()

        eu = models.ExcitingUpload.objects.get(torrent=self.ex_torrent2)
        self.assertEquals(eu.is_exciting, True)

    def test_subclass_to_parent(self):
        eu = torrents.models.Upload.objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(eu, models.ExcitingUpload)
        eu_parent = eu.get_parent_object()
        self.assertIsInstance(eu_parent, torrents.models.Upload)


class TorrentGroupTests(BaseTestCase):
    def test_can_get_parent(self):
        t = torrents.models.TorrentGroup.base_objects.get(
            uploads=self.boring_upload
        )
        t2 = torrents.models.TorrentGroup.base_objects.get(
            uploads=self.exciting_upload
        )
        self.assertIsInstance(t, torrents.models.TorrentGroup)
        self.assertIsInstance(t2, torrents.models.TorrentGroup)
        self.assertNotIsInstance(t, models.BoringGroup)
        self.assertNotIsInstance(t2, models.ExcitingGroup)

    def test_gets_boring(self):
        bg = torrents.models.TorrentGroup.objects.get(
            uploads=self.boring_upload
        )
        self.assertIsInstance(bg, models.BoringGroup)
        self.assertEquals(bg, self.boring_group)
        self.assertEquals(bg.uploads.all()[0], self.boring_upload)

    def test_gets_exciting(self):
        eg = torrents.models.TorrentGroup.objects.get(
            uploads=self.exciting_group
        )
        self.assertIsInstance(eg, models.ExcitingGroup)
        self.assertEquals(eg, self.exciting_group)
        self.assertEquals(eg.uploads.all()[0], self.exciting_upload)

    def test_get_from_torrent(self):
        self.assertEquals(
            self.ex_torrent.upload.parent,
            self.boring_group
        )
        self.assertEquals(
            self.ex_torrent2.upload.parent,
            self.exciting_group
        )

    def test_set_from_torrent(self):
        self.ex_torrent2.upload.parent.is_exciting = True
        self.ex_torrent2.upload.save()

        eg = models.ExcitingGroup.objects.get(
            uploads__torrent=self.ex_torrent2
        )
        self.assertEquals(eg.is_exciting, True)

    def test_subclass_to_parent(self):
        eg = torrents.models.TorrentGroup.objects.get(
            uploads=self.exciting_upload
        )
        self.assertIsInstance(eg, models.ExcitingGroup)
        eg_parent = eg.get_parent_object()
        self.assertIsInstance(eg_parent, torrents.models.TorrentGroup)
