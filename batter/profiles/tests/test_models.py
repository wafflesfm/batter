from django.test import TestCase
from django.contrib.auth.models import User

from .. import models


class ProfileTests(TestCase):
    def setUp(self):
        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.profile = models.Profile(user=self.samantha)

    def test_trackerid_generation(self):
        profile = self.profile
        self.assertIsNone(profile.trackerid)
        profile.save()
        self.assertEquals(len(profile.trackerid), 32)

    def test_unicode(self):
        self.assertEquals(unicode(self.profile), "samantha")


class HelperTests(TestCase):
    def test_generate_trackerid(self):
        trackerid = models.generate_trackerid()
        self.assertEquals(len(trackerid), 32)
