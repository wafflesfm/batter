import json

from django.http import HttpResponse
from django.conf import settings

from music.helpers.discogs import DiscogsAPI


try:
    discog = DiscogsAPI(user_agent=settings.DISCOGS_USERAGENT)
except AttributeError:
    discog = DiscogsAPI()


def json_response(data):
    """helper function that returns a json response"""
    return HttpResponse(
        json.dumps(data),
        content_type="application/json; charset=utf8"
    )


def get_artist(request, artist_id):
    """Gets artist with id `artist_id` from discogs"""
    return json_response(discog.get_artist(artist_id))


def get_release(request, release_id):
    """Gets release with id `release_id` from discogs"""
    return json_response(discog.get_release(release_id))


def get_artist_releases(request, artist_id):
    """Gets all releases from artist with id `artist_id` from discogs
    Takes options get param `page` for discogs pagination
    """
    page = request.GET.get('page', 1)
    return json_response(discog.get_releases(artist_id, page=page))


def search_artist(request):
    """Does a search on discogs Artist search using query from get param `q`
    `page` get param is used for discogs pagination
    """
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    return json_response(discog.search(query, page=page, search_type="artist"))


def search_release(request):
    """searches for releases with get param `q`
    `page` get param is used for discogs pagination
    """
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    return json_response(discog.search(query, page=page, search_type="release"))


def search_discogs(request):
    """Does a general paginated search on discogs"""
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    return json_response(discog.search(query, page=page))
