import cStringIO as StringIO

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import View

from torrents.forms.torrent_upload import TorrentUploadForm
from torrents.models import Torrent


def upload_torrent(request):
    """
    Takes a torrent upload and parses/stores it
    """

    form = TorrentUploadForm()
    if request.method == 'POST':
        form = TorrentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            torrent = form.cleaned_data['torrent']
            try:
                torrent.save()
                return redirect(torrent)
            except:
                # We've already uploaded this torrent
                # (torrent.pieces is not unique in the database)
                pass
    return render(request, 'torrents/upload.html', {'form': form})


def view_torrent(request, pk):
    torrent = get_object_or_404(Torrent, pk=pk)

    return HttpResponse(
        "PK is " + str(torrent.pk) + "<br />name is " + torrent.name
    )


class TorrentGenerate(View):
    """
    View that is called when a request to download a torrent happens
    """

    def get(self, *args, **kwargs):
        torrent = get_object_or_404(Torrent, pk=kwargs.get('pk'))
        torrent_file = StringIO.StringIO(torrent.to_bencoded_string())

        response = HttpResponse(
            torrent_file.read(),
            content_type='application/x-bittorrent'
        )
        response['Content-Disposition'] = 'attachment; ' + \
                                          'filename=' + \
                                          slugify(torrent.name) + '.torrent'
        response['Content-Length'] = torrent_file.tell()

        return response
