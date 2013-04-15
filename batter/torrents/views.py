from __future__ import absolute_import, unicode_literals

import cStringIO as StringIO

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from .forms import TorrentUploadForm
from .models import Torrent


def upload_torrent(request):
    form = TorrentUploadForm(request.POST, request.FILES)
    if form.is_valid():
        torrent = form.cleaned_data['torrent']
        import pdb; pdb.set_trace()
        try:
            torrent.save()
            return redirect(torrent)
        except Exception:
            # We've already uploaded this torrent
            # (torrent.pieces is not unique in the database)
            pass
        
    return render(request, 'torrents/upload.html', {'form': form})


def view_torrent(request, pk):
    torrent = get_object_or_404(Torrent, pk=pk)
    return HttpResponse("Torrent '{0}' with pk = {0.pk}.".format(torrent))


def download_torrent(request, pk):
    torrent = get_object_or_404(Torrent, pk=pk)
    torrent_file = StringIO.StringIO(torrent.to_bencoded_string())

    response = HttpResponse(
        torrent_file.read(), content_type='application/x-bittorrent')
    response['Content-Length'] = torrent_file.tell()
    response['Content-Disposition'] = \
        'attachment; filename={0}.torrent'.format(slugify(torrent.name))
    return response
