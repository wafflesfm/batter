from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from batter.test import LoggedInTestCase
from ..models import Artist, Master, Release


class ArtistDetailTests(LoggedInTestCase):
    def setUp(self):
        self.artist = Artist(name="Okkervil River", slug="Okkervil-River")
        self.artist.save()
        self.url = reverse("music_artist_detail",
                           kwargs={
                                   'pk': self.artist.pk,
                                   'slug': self.artist.slug})
        super(ArtistDetailTests, self).setUp()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_slug_redirect(self):
        response = self.client.get(reverse("music_artist_detail",
                                           kwargs={
                                                   'pk': self.artist.pk,
                                                   'slug': 'wrong-slug'}))
        self.assertEquals(response.status_code, 301)


class MasterDetailTests(LoggedInTestCase):
    def setUp(self):
        self.artist = Artist(name="Okkervil River",
                             slug="Okkervil-River")
        self.artist.save()
        self.master = Master(name="Black Sheep Boy",
                             slug="Black-Sheep-Boy")
        self.master.save()
        self.release = Release(name="Original",
                               slug="Original",
                               master=self.master)
        self.release.save()
        self.master.artists.add(self.artist)
        self.master.main = self.release
        self.master.save()
        self.url = reverse("music_master_detail",
                           kwargs={
                                   'pk': self.master.pk,
                                   'slug': self.master.slug})
        super(MasterDetailTests, self).setUp()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
