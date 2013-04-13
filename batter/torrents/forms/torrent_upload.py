from django import forms

from ..fields import TorrentField


class TorrentUploadForm(forms.Form):
    torrent = TorrentField(label="Torrent File")
