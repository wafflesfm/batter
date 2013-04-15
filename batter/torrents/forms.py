from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from .fields import TorrentField


class TorrentUploadForm(forms.Form):
    torrent_file = TorrentField(label=_("torrent file"))
