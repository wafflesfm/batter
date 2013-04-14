import json

from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from music.helpers.discogs import DiscogsAPI


try:
    discog = DiscogsAPI(user_agent=settings.DISCOGS_USERAGENT)
except AttributeError:
    discog = DiscogsAPI()


def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json; charset=utf8")


def get_artist(request, artist_id):
    return json_response(discog.get_artist(artist_id))


def get_release(request, release_id):
    return json_response(discog.get_release(release_id))


def get_artist_releases(request, artist_id, page=1):
    return json_response(discog.get_releases(artist_id, page=page).next())


def search_artist(request, query, page=1):
    return json_response(discog.search_artist(query, page=page).next())


def search_release(request, query, page=1):
    return json_response(discog.search_release(query, page=page).next())


def search_discogs(request, query, page=1):
    return json_response(discog.search(query, page=page).next())