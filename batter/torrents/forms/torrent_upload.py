from django import forms


class TorrentUploadForm(forms.Form):
    torrent_file = forms.FileField(label="Torrent File")
