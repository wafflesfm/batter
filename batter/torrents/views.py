from __future__ import absolute_import, unicode_literals

import cStringIO as StringIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.views.generic.detail import DetailView

from .forms import TorrentUploadForm
from .models import Torrent


def upload_torrent(request):
    form = TorrentUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        torrent = form.cleaned_data['torrent_file']
        try:
            torrent.save()
            return redirect(torrent)
        except Exception:
            resp = HttpResponse()
            resp.status_code = 409
            return resp

    return render(request, 'torrents/upload.html', {'form': form})


class TorrentView(DetailView):
    model = Torrent


class DownloadView(DetailView):
    model = Torrent

    def get(self, request, *args, **kwargs):
        torrent = self.get_object()
        torrent_file = StringIO.StringIO(torrent.as_bencoded_string())

        response = HttpResponse(
            torrent_file.read(), content_type='application/x-bittorrent')
        response['Content-Length'] = torrent_file.tell()
        response['Content-Disposition'] = \
            'attachment; filename={0}.torrent'.format(slugify(torrent.name))
        return response
