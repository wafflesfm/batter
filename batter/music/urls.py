from django.conf.urls import patterns, url

from .views.upload import MusicUploadWizard, FORMS, CONDITIONS

urlpatterns = patterns(
    '',
    url(
        r'upload/$',
        # TODO: use form_list (see MusicUploadWizard definition)
        MusicUploadWizard.as_view(FORMS, condition_dict=CONDITIONS),
        name="upload_music"
    ),
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
        r'api/discogs/search/artist/$',
        'music.views.api.discogs.search_artist',
        name="discogs_search_artist"
    ),
    url(
        r'api/discogs/search/release/$',
        'music.views.api.discogs.search_release',
        name="discogs_search_releases"
    ),
    url(
        r'api/discogs/search/$',
        'music.views.api.discogs.search_discogs',
        name="discogs_search"
    ),
    url(
        r'search/(?P<q>[^/]+)',
        'music.views.browse.search',
        name="music_view_search"
    ),
    url(
        r'(?P<artist_slug>[^/]+)/(?P<master_slug>[^/]+)/$',
        'music.views.browse.view_master',
        name="music_view_master"
    ),
    url(
        r'(?P<artist_slug>[^/]+)/$',
        'music.views.browse.view_artist',
        name='music_view_artist'
    ),
)
