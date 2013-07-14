from __future__ import absolute_import, unicode_literals

import hashlib

from django.test import TestCase

from ..models import Artist, Master, Release


class ArtistTests(TestCase):
    def test_absolute_url(self):
        # Just poke it
        artist = Artist(name="Okkervil River", slug="Okkervil-River")
        artist.save()
        artist.get_absolute_url()


class MasterTests(TestCase):
    def test_absolute_url(self):
        # Just poke it
        master = Master(name="Black Sheep Boy", slug="Black-Sheep-Boy")
        master.save()
        master.get_absolute_url()
