from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('torrents.views',
    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name="torrents_browse"),
    url(r'upload/$', "upload_torrent", name="torrents_upload"),
    url(r'(?P<pk>\d+)/$', "view_torrent", name="torrents_view"),
    url(r'(?P<pk>\d+)/download/$', "download_torrent",
        name="torrents_generate"),
)
