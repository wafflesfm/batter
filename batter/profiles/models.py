import uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    trackerid = models.CharField(max_length=32, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        override save method to generate a trackerid
        for torrent tracker url generation
        """

        if not self.trackerid:
            self.trackerid = generate_trackerid()
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


# helpers
def generate_trackerid():
    """
    generate a uuid and check if it already exists in a profile
    """

    trackerid = None
    while trackerid is None or \
            Profile.objects.filter(trackerid=trackerid).exists():
        trackerid = uuid.uuid4().hex
    return trackerid
