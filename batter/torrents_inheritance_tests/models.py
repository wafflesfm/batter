from django.db import models

from torrents.models import Upload, UploadGroup, DescendingModel


class BoringUpload(Upload):
    pass


class BoringGroup(UploadGroup):
    pass


class ExcitingUpload(Upload):
    is_exciting = models.BooleanField(default=True)


class ExcitingGroup(UploadGroup):
    is_exciting = models.BooleanField(default=True)


class InbetweenerUpload(Upload):
    pass


class InbetweenerTweener(DescendingModel):
    parent = models.ForeignKey(
        'InbetweenerGroup', null=False, related_name='_children'
    )

    def get_child_model(self):
        return InbetweenerUpload


class InbetweenerGroup(UploadGroup):
    def get_child_model(self):
        return InbetweenerTweener
