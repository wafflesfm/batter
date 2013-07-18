from django.conf.urls import patterns, url

from .views import SearchView, ArtistView, MasterView
from .views.upload import MusicUploadWizard, FORMS, CONDITIONS

urlpatterns = patterns(
    '',
    url(r'^search/$',
        SearchView(),
        name='music_search'),
    url(r'^upload/$',
        # TODO: use form_list (see MusicUploadWizard definition)
        MusicUploadWizard.as_view(FORMS, condition_dict=CONDITIONS),
        name="upload_music"),
    url(r'^(?P<slug>[-\w]+)-(?P<pk>\d+)/$',
        ArtistView.as_view(),
        name="music_artist_detail"),
    url(r'^album/(?P<slug>[-\w]+)-(?P<pk>\d+)/$',
        MasterView.as_view(),
        name="music_master_detail"),
)
