from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from torrents.forms import TorrentUploadForm

from .types import UPLOAD_TYPES, FORMAT_TYPES, BITRATE_TYPES, RELEASE_TYPES
from .types import MEDIA_TYPES


class TorrentTypeForm(TorrentUploadForm):
    type = forms.ChoiceField(UPLOAD_TYPES)


class ReleaseInfoForm(forms.Form):
    artist = forms.CharField()
    album = forms.CharField()
    year = forms.CharField()


class FileInfoForm(forms.Form):
    format = forms.ChoiceField(FORMAT_TYPES)
    bitrate = forms.ChoiceField(BITRATE_TYPES)
    release = forms.ChoiceField(RELEASE_TYPES)
    media = forms.ChoiceField(MEDIA_TYPES)
