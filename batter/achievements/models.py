from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from model_utils import Choices

def random_image_name(instance, filename):
    import uuid
    import os.path

    # generate a random filename
    basename = uuid.uuid4().hex

    # now append the extension
    _, extension = os.path.splitext(filename)

    return "achievements/{}.{}".format(basename, extension)


@python_2_unicode_compatible
class AchievementOwnership(models.Model):
    GRANT_REASONS = Choices(
        ('condition_met', _('Met necessary conditions')),
        ('staff_granted', _('Granted achievement by staff'))
    )

    achievement = models.ForeignKey('Achievement')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    date_granted = models.DateTimeField(auto_now_add=True)
    grant_reason = models.CharField(
        max_length=32, choices=GRANT_REASONS
    )

    def __str__(self):
        return "{} owned by {}".format(self.achievement, self.user)

    class Meta:
        unique_together = (('achievement', 'user'))


@python_2_unicode_compatible
class Achievement(models.Model):
    SECRECY_TYPES = Choices(
        ('invisible', _('Invisible unless owned')),
        ('all_hidden', _('All information hidden unless owned')),
        ('image_desc_hidden', _('Image and description hidden unless owned')),
        ('description_hidden', _('Description hidden unless owned')),
        ('image_hidden', _('Image hidden unless owned')),
        ('public', _('All information visible'))
    )
    FIELD_TYPES = Choices(
        'achievement', 'image', 'title', 'description'
    )

    slug = models.SlugField(unique=True, blank=False, null=False)

    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    secrecy_type = models.CharField(
        max_length=32, choices=SECRECY_TYPES,
        blank=False, null=False,
        default=SECRECY_TYPES.public
    )

    image = models.ImageField(
        blank=True, null=False, upload_to=random_image_name
    )

    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='AchievementOwnership'
    )

    def _field_is_visible(self, to_user, field):
        SECRECY_TYPES = self.SECRECY_TYPES
        FIELD_TYPES = self.FIELD_TYPES

        if self.owned_by(to_user):  # if they own me...
            return True  # they can see me.

        if field == FIELD_TYPES.achievement:
            return self.secrecy_type != SECRECY_TYPES.invisible
        elif field == FIELD_TYPES.image:
            return self.secrecy_type in (
                SECRECY_TYPES.description_hidden,
                SECRECY_TYPES.public,
            )
        elif field == FIELD_TYPES.title:
            return self.secrecy_type in (
                SECRECY_TYPES.image_desc_hidden,
                SECRECY_TYPES.image_hidden,
                SECRECY_TYPES.description_hidden, 
                SECRECY_TYPES.public,
            )
        elif field == FIELD_TYPES.description:
            return self.secrecy_type in (
                SECRECY_TYPES.image_hidden,
                SECRECY_TYPES.public,
            )

        raise Exception("Unknown field type {}".format(field))

    def owned_by(self, to_user):
        return self.owners.filter(pk=to_user.pk).exists()

    def achievement_is_visible(self, to_user):
        return self._field_is_visible(to_user, self.FIELD_TYPES.achievement)

    def title_is_visible(self, to_user):
        return self._field_is_visible(to_user, self.FIELD_TYPES.title)

    def description_is_visible(self, to_user):
        return self._field_is_visible(to_user, self.FIELD_TYPES.description)

    def image_is_visible(self, to_user):
        return self._field_is_visible(to_user, self.FIELD_TYPES.image)

    def grant(self, user, reason):
        # this method does not send a notification
        AchievementOwnership(
            achievement=self, user=user, grant_reason=reason
        ).save()

    def __str__(self):
        return self.title
