from django.conf.urls import patterns, url

from .views import DownloadView, TorrentView

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/$', TorrentView.as_view(),
        name="torrents_torrent_view"),
    url(r'upload/$', "torrents.views.upload_torrent",
        name="torrents_torrent_upload"),
    url(r'(?P<pk>\d+)/download/$', DownloadView.as_view(),
        name="torrents_torrent_download"),
)
