import json
import binascii
import cStringIO as StringIO

from bencode import *

from django.views.generic import View, FormView
from django.shortcuts import render
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

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
            torrent_file = request.FILES['torrent_file']
            torrent = Torrent.from_torrent_file(torrent_file)
            torrent.save()

    return render(request, 'torrents/upload.html', {'form': form})


class TorrentGenerate(View):
    """
    View that is called when a request to download a torrent happens
    """

    def get(self, *args, **kwargs):
        try:
            torrent = Torrent.objects.get(pk=self.kwargs['pk'])
        except:
            return HttpResponse('torrent doesnt exist. REPLACE ME')

        torrent_file = StringIO.StringIO(torrent.generate_torrent())

        response = HttpResponse(torrent_file.read(), content_type='application/x-bittorrent')
        response['Content-Disposition'] = 'attachment; filename=' + torrent.name + '.torrent'
        response['Content-Length'] = torrent_file.tell()

        return response 

