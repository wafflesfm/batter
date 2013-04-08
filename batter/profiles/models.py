import hashlib
import uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    trackerid = models.CharField(max_length=25, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        override save method to generate a trackerid for torrent tracker url generation
        """
        
        if not trackerid:
            trackerid = generate_trackerid()
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


#helpers
def generate_trackerid():
    """
    generate a uuid and check if it already exists in a profile
    """

    trackerid = uuid.uuid1().hex
    if Profile.objects.filter(trackerid=trackerid).exists():
        generate_trackerid()
    else:
        return trackerid