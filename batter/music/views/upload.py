from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.contrib.formtools.wizard.views import CookieWizardView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from ..forms import TorrentTypeUploadForm, MusicUploadForm

def torrent_is_type(torrent_type):
    def check(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('torrenttype') or {'type': 'none'}
        return cleaned_data['type'] == torrent_type
    return check

FORMS = [("torrenttype", TorrentTypeUploadForm),
         ("artist", MusicUploadForm)]

CONDITIONS = {
    "artist": torrent_is_type('music'),
}

class MusicUploadWizard(CookieWizardView):
#    TODO: use form_list once support for this gets released
#          (currently in django dev version)
#    form_list = [MusicUploadForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))

    def done(self, form_list, **kwargs):
        return HttpResponse('done')
