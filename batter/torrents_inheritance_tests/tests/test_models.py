from django.test import TestCase
from django.contrib.auth.models import User

from torrents.models import Torrent, TorrentGroup, Upload
from torrents.tests.local_settings import TEST_FILE_PATH

from .. import models


class BaseTestCase(TestCase):
    def setUp(self):
        with open(TEST_FILE_PATH, 'rb') as fp:
            self.ex_torrent = Torrent.from_torrent_file(fp)
            fp.seek(0)
            self.ex_torrent2 = Torrent.from_torrent_file(fp)
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
        u = Upload.base_objects.get(torrent=self.ex_torrent)
        u2 = Upload.base_objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(u, Upload)
        self.assertIsInstance(u2, Upload)
        self.assertNotIsInstance(u, models.BoringUpload)
        self.assertNotIsInstance(u2, models.ExcitingUpload)

    def test_gets_boring(self):
        bu = Upload.objects.get(torrent=self.ex_torrent)
        self.assertIsInstance(bu, models.BoringUpload)
        self.assertEquals(bu, self.boring_upload)

    def test_gets_exciting(self):
        eu = Upload.objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(eu, models.ExcitingUpload)
        self.assertEquals(eu, self.exciting_upload)
        self.assertEquals(eu.is_exciting, False)

    def test_modifies_exciting(self):
        self.exciting_upload.is_exciting = True
        self.exciting_upload.save()
        eu = Upload.objects.get(torrent=self.ex_torrent2)
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
        eu = Upload.objects.get(torrent=self.ex_torrent2)
        self.assertIsInstance(eu, models.ExcitingUpload)
        eu_parent = eu.get_parent_object()
        self.assertIsInstance(eu_parent, Upload)


class TorrentGroupTests(BaseTestCase):
    def test_can_get_parent(self):
        t = TorrentGroup.base_objects.get(
            uploads=self.boring_upload
        )
        t2 = TorrentGroup.base_objects.get(
            uploads=self.exciting_upload
        )
        self.assertIsInstance(t, TorrentGroup)
        self.assertIsInstance(t2, TorrentGroup)
        self.assertNotIsInstance(t, models.BoringGroup)
        self.assertNotIsInstance(t2, models.ExcitingGroup)

    def test_gets_boring(self):
        bg = TorrentGroup.objects.get(
            uploads=self.boring_upload
        )
        self.assertIsInstance(bg, models.BoringGroup)
        self.assertEquals(bg, self.boring_group)
        self.assertEquals(bg.uploads.all()[0], self.boring_upload)

    def test_gets_exciting(self):
        eg = TorrentGroup.objects.get(
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
        eg = TorrentGroup.objects.get(
            uploads=self.exciting_upload
        )
        self.assertIsInstance(eg, models.ExcitingGroup)
        eg_parent = eg.get_parent_object()
        self.assertIsInstance(eg_parent, TorrentGroup)
