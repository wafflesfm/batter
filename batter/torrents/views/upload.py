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


def parse_torrent(torrent):
    """
    multi-file torrent:
        {
            "creation date": 1365250898, 
            "announce": "http://tracker.url/announce/",
            "created by": "Transmission/2.77 (14031)", 
            "encoding": "UTF-8",
            "info": { 
                "files" : [ 
                    { 
                        "length" : 23579528,
                        "path" : [ "01 - The Disappearance of the Girl.flac" ]
                    },
                    { 
                        "length" : 23558427,
                        "path" : [ "02 - Storm Song.flac" ]
                    },
                    { 
                        "length" : 17405523,
                        "path" : [ "03 - Mistakes.flac" ]
                    },
                    ...
                ],
                "name" : "Phildel - The Disappearance of the Girl (2013) FLAC",
                "piece length" : 131072,
                "pieces": "4b4102a28f776c9954b165cc09378e41dbadecdc0a0c1f13c9d020ef388b3554479eee441fad915b7c6114a9d67b91b2a1728d0ac5554d24e236cf984dcae4"
                "private" : 1
            }
        }

    single-file torrent:
        { 
            "announce" : "http://test.com/",
            "created by" : "uTorrent/1800",
            "creation date" : 1365367491,
            "encoding" : "UTF-8",
            "info": { 
                "length" : 5,
                "name" : "test.txt",
                "piece length" : 16384,
                "pieces" : "4e1243bd22c66e76c2ba9eddc1f91394e57f9f83",
                "private" : 1
            }
        }
    """
    t = bdecode(torrent.read())

    s = binascii.hexlify(t['info']['pieces'])
    stest = binascii.unhexlify(s)
    assert stest == t['info']['pieces']

    t['info']['pieces'] = binascii.hexlify(t['info']['pieces'])

    return t


def upload_torrent(request):
    """
    Takes a torrent upload and parses/stores it
    """

    if request.method == 'POST':
        form = TorrentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            torrent_file = parse_torrent(request.FILES['torrent_file'])

            if Torrent.objects.filter(pieces=torrent_file['info']['pieces']).exists():
                return HttpResponse('torrent already exists in database')
            else:
                torrent = Torrent()

                if torrent_file['info'].get('files', None):
                   torrent.files = json.dumps(torrent_file['info']['files'])

                else:
                    files = []
                    ffile = {}
                    ffile["length"] = torrent_file['info']['length']
                    ffile["path"] = [torrent_file['info']['name'].encode('utf-8', 'ignore')]
                    files.append(ffile)
                    torrent.files = files

                torrent.name = torrent_file["info"]["name"]
                torrent.creation_date = torrent_file['creation date']
                torrent.client = torrent_file['created by']
                torrent.encoding = torrent_file.get('encoding', 'UTF-8')
                torrent.piece_length = torrent_file['info']['piece length']
                torrent.pieces = torrent_file['info']['pieces']
                torrent.uploader = request.user

                torrent.save()

    else:
        form = TorrentUploadForm()

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

