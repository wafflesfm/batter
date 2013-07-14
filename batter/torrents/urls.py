from django.conf.urls import patterns, url

from .views import DownloadView

urlpatterns = patterns('torrents.views',
    url(r'upload/$', "upload_torrent", name="torrents_upload"),
    url(r'download/(?P<pk>\d+)/$', DownloadView.as_view(),
        name="torrents_torrent_download"),
)
