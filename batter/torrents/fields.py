from BTL import BTFailure

from django import forms
from django.core.exceptions import ValidationError

from .models import Torrent

class TorrentField(forms.FileField):
    def to_python(self, value):
        try:
            return Torrent.from_torrent_file(value)
        except BTFailure as e:
            raise ValidationError(str(e))
