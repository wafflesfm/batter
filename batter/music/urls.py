from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(
        r'api/discogs/artist/(?P<artist_id>\d+)/$',
        'music.views.api.discogs.get_artist',
        name="discogs_get_artist"
    ),
    url(
        r'api/discogs/release/(?P<release_id>\d+)/$',
        'music.views.api.discogs.get_release',
        name="discogs_get_release"
    ),
    url(
        r'api/discogs/artist/(?P<artist_id>\d+)/releases/$',
        'music.views.api.discogs.get_artist_releases',
        name="discogs_get_artist_releases"
    ),
    url(
        r'api/discogs/search/artist/(?P<query>\w+)/$',
        'music.views.api.discogs.search_artist',
        name="discogs_search_artist"
    ),
    url(
        r'api/discogs/search/release/(?P<query>\w+)/$',
        'music.views.api.discogs.search_release',
        name="discogs_search_releases"
    ),
    url(
        r'api/discogs/search/(?P<query>\w+)/$',
        'music.views.api.discogs.search_discogs',
        name="discogs_get_artist"
    ),
)
