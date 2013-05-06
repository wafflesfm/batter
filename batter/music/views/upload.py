from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.contrib.formtools.wizard.views import CookieWizardView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from ..forms import TorrentTypeForm, ReleaseInfoForm, FileInfoForm


def torrent_is_type(torrent_type):
    def check(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step('torrent_type') or {'type': 'none'}
        return cleaned_data['type'] == torrent_type
    return check

FORMS = [("torrent_type", TorrentTypeForm),
         ("release", ReleaseInfoForm),
         ("file", FileInfoForm),
]

TEMPLATES = {
    "default": "music/upload/base.html",
    "release": "music/upload/release.html",
}

CONDITIONS = {
    "release": torrent_is_type('music'),
    "file": torrent_is_type('music')
}

class MusicUploadWizard(CookieWizardView):
#    TODO: use form_list once support for this gets released
#          (currently in django dev version)
#    form_list = [MusicUploadForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))

    def get_template_names(self):
        try:
            return [TEMPLATES[self.steps.current]]
        except:
            return [TEMPLATES["default"]]

    def get_context_data(self, form, **kwargs):
        context = super(MusicUploadWizard, self).get_context_data(form=form, **kwargs)
        cleaned_data = self.get_cleaned_data_for_step("torrent_type") or {'torrent_file': None}
        if cleaned_data["torrent_file"]:
            context.update({'torrent_name': cleaned_data["torrent_file"].name})
        return context

    def done(self, form_list, **kwargs):
        return HttpResponse('done')
