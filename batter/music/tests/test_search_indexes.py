from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from ..models import Artist
from ..search_indexes import ArtistIndex


class ArtistIndexTests(TestCase):
    def setUp(self):
        self.index = ArtistIndex()

    def test_get_model(self):
        self.assertEquals(self.index.get_model(), Artist)

    def test_index_queryset(self):
        # Querysets are covered by Django tests, so just make sure that the QS
        # model is the same as the index model.
        self.assertEquals(self.index.index_queryset().model,
                          self.index.get_model())
