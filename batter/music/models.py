from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext as _

from django_countries import CountryField
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

from torrents.models import Torrent


FORMAT_TYPES = (
    ('mp3', 'MP3'),
    ('flac', 'FLAC'),
    ('aac', 'AAC'),
    ('ac3', 'AC3'),
    ('dts', 'DTS'),
)

BITRATE_TYPES = (
    ('192', '192'),
    ('apsvbr', 'APS (VBR)'),
    ('v2vbr', 'V2 (VBR)'),
    ('v1vbr', 'V1 (VBR)'),
    ('256', '256'),
    ('apxvbr', 'APX (VBR)'),
    ('v0vbr', 'V0 (VBR)'),
    ('320', '320'),
    ('lossless', _('Lossless')),
    ('24bitlossless', _('24Bit Losless')),
    ('v8vbr', 'V8 (VBR)'),
    ('other', _('Other')),

)

MEDIA_TYPES = (
    ('cd', 'CD'),
    ('dvd', 'DVD'),
    ('vinyl', _('Vinyl')),
    ('soundboard', _('Soundboard')),
    ('sacd', 'SACD'),
    ('dat', 'DAT'),
    ('cassette', _('Cassette')),
    ('web', 'WEB'),
    ('bluray', 'Blu-Ray'),
)

RELEASE_TYPES = (
    ('album', _('Album')),
    ('soundtrack', _('Soundtrack')),
    ('ep', _('EP')),
    ('anthology', _('Anthology')),
    ('compilation', _('Compilation')),
    ('djmix', _('DJ Mix')),
    ('single', _('Single')),
    ('livealbum', _('Live Album')),
    ('remix', _('Remix')),
    ('bootleg', _('Bootleg')),
    ('interview', _('Interview')),
    ('mixtape', _('Mixtape')),
    ('unknown', _('Unknown'))
)


@python_2_unicode_compatible
class MusicUpload(TimeStampedModel):
    torrent = models.ForeignKey(Torrent)
    edition = models.ForeignKey('Edition')
    format = models.TextField(choices=FORMAT_TYPES)
    bitrate = models.TextField(choices=BITRATE_TYPES)
    media = models.TextField(choices=MEDIA_TYPES)
    logfile = models.TextField(blank=True, null=True)
    uploader = models.ForeignKey(User)

    def __str__(self):
        return "{0} / {1} / {2}".format(
            self.edition.release,
            force_text(self.format),
            force_text(self.bitrate)
        )


@python_2_unicode_compatible
class Artist(TimeStampedModel):
    discogs_id = models.TextField()
    name = models.TextField()
    sort_name = models.SlugField()
    related_artists = models.ManyToManyField(
        'self',
        related_name="artist_related_artists",
        blank=True,
        null=True
    )
    artist_type = models.ForeignKey('ArtistType')
    country = CountryField()
    gender = models.TextField()
    disambiguation = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    birthdate = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return force_text(self.name)


@python_2_unicode_compatible
class ArtistType(models.Model):
    name = models.TextField()

    def __str__(self):
        return force_text(self.name)


@python_2_unicode_compatible
class ArtistAlias(models.Model):
    alias = models.TextField()
    artist = models.ForeignKey('Artist')

    def __str__(self):
        return force_text(self.alias)


@python_2_unicode_compatible
class Release(TimeStampedModel):
    discogs_id = models.TextField()
    name = models.TextField()
    artist_credit = models.ManyToManyField('Artist')
    comment = models.TextField()
    release_type = models.TextField(choices=RELEASE_TYPES)
    tags = TaggableManager()

    def __str__(self):
        return force_text(self.name)


@python_2_unicode_compatible
class Edition(TimeStampedModel):
    name = models.TextField()
    release = models.ForeignKey('Release')
    country = CountryField()
    label = models.TextField()
    date = models.DateField()
    barcode = models.TextField()

    def __str__(self):
        return force_text(self.name)


@python_2_unicode_compatible
class Label(TimeStampedModel):
    name = models.TextField()
    is_vanity = models.BooleanField()

    def __str__(self):
        return force_text(self.name)
