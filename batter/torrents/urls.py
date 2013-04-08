from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from torrents.views.upload import upload_torrent, TorrentGenerate

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="torrents_browse"),
    url(r'upload/$', upload_torrent, name="torrents_upload"),
    url(r'download/(?P<pk>\d+)/$', TorrentGenerate.as_view(), name="torrents_generate"),   
)