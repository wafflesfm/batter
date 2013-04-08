from django import forms


class TorrentUploadForm(forms.Form):
    torrentfile = forms.FileField(label="Torrent File")