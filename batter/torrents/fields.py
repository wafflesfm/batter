from BTL import BTFailure
from django import forms
from django.core.exceptions import ValidationError

from .models import Torrent


class TorrentField(forms.FileField):
    def to_python(self, data):
        data = super(TorrentField, self).to_python(data)
        if data is None:
            raise ValidationError(self.error_messages['empty'])

        try:
            return Torrent.from_torrent_file(data)
        except BTFailure as e:
            raise ValidationError(str(e))
