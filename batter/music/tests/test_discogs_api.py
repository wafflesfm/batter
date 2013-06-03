import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from music.helpers.discogs import DiscogsAPI


class TestDiscogsAPI(TestCase):
    fixtures = ['test_user.json', ]

    def setUp(self):
        self.client.login(username='vagrant', password='vagrant')
        self.discogs = DiscogsAPI()

    def test_get_artist(self):
        resp = json.loads(
            self.client.get(
                reverse('discogs_get_artist', kwargs={'artist_id': 42})
            ).content
        )
        self.assertEqual(str(resp['id']), '42')

    def test_get_release(self):
        resp = json.loads(
            self.client.get(
                reverse('discogs_get_release', kwargs={'release_id': 42})
            ).content
        )
        self.assertEqual(str(resp['id']), '42')

    def test_get_artist_releases(self):
        resp = json.loads(
            self.client.get(
                reverse('discogs_get_artist_releases',
                        kwargs={'artist_id': 42})
            ).content
        )
        self.assertEqual(resp['releases'][0]['type'], 'release')

    def test_search(self):
        resp = self.client.get(
            reverse('discogs_search'), {'q': 'radio head'}
        ).status_code
        self.assertEqual(resp, 200)

    def test_release_search(self):
        resp = self.client.get(
            reverse('discogs_search_releases'), {'q': 'radio head'}
        ).status_code
        self.assertEqual(resp, 200)

    def test_artist_search(self):
        resp = self.client.get(
            reverse('discogs_search_artist'), {'q': 'radio head'}
        ).status_code
        self.assertEqual(resp, 200)

    def test_search_pagination(self):
        resp = self.client.get(
            reverse('discogs_search'), {'q': 'radio head', 'page': 3}
        ).status_code
        self.assertEqual(resp, 200)

    def test_releases_pagination(self):
        resp = self.client.get(
            reverse('discogs_get_artist_releases',
                    kwargs={'artist_id': 99731}),
            {'page': 3}
        ).status_code
        self.assertEqual(resp, 200)
