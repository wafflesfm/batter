from django.db import models

from torrents.models import Upload, TorrentGroup


class BoringUpload(Upload):
    pass


class BoringGroup(TorrentGroup):
    pass


class ExcitingUpload(Upload):
    is_exciting = models.BooleanField(default=True)


class ExcitingGroup(TorrentGroup):
    is_exciting = models.BooleanField(default=True)
