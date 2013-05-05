from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from torrents.forms import TorrentUploadForm

from .types import UPLOAD_TYPES, FORMAT_TYPES

class TorrentTypeForm(TorrentUploadForm):
    type = forms.ChoiceField(UPLOAD_TYPES)

class ReleaseInfoForm(forms.Form):
    artist = forms.CharField()
    album = forms.CharField()
    year = forms.CharField()

class FileInfoForm(forms.Form):
    format = forms.ChoiceField(FORMAT_TYPES)
