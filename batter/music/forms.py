from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from torrents.forms import TorrentUploadForm

SUPPORTED_TYPES = (
    ('music', _('Music')),
    ('applications', _('Applications')),
    ('ebooks', _('E-Books')),
    ('audiobooks', _('Audiobooks')),
    ('comedy', _('Comedy / Spoken Word')),
    ('comics', _('Comics')),
)

class TorrentTypeUploadForm(TorrentUploadForm):
    type = forms.ChoiceField(SUPPORTED_TYPES)

class MusicUploadForm(forms.Form):
    artist = forms.CharField()
    album = forms.CharField()
