from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel, Choices
from taggit.managers import TaggableManager()

from torrents.model import Torrent


class MusicUpload(TimeStampedModel):
    FORMATS = Choices(
        ('mp3', 'MP3'),
        ('flac', 'FLAC'),
        ('aac', 'AAC'),
        ('ac3', 'AC3'),
        ('dts', 'DTS'),
    )

    BITRATE = Choices(
        ('192', '192'),
        ('apsvbr', 'APS (VBR)'),
        ('v2vbr', 'V2 (VBR)'),
        ('v1vbr', 'V1 (VBR)'),
        ('256', '256'),
        ('apxvbr', 'APX (VBR)'),
        ('v0vbr', 'V0 (VBR)'),
        ('320', '320'),
        ('lossless', 'Lossless'),
        ('24bitlossless', '24Bit Losless'),
        ('v8vbr', 'V8 (VBR)'),
        ('other', 'Other'),

    )

    MEDIA = Choices(
        ('cd', 'CD'),
        ('dvd', 'DVD'),
        ('vinyl', 'Vinyl'),
        ('soundboard', 'Soundboard'),
        ('sacd', 'SACD'),
        ('dat', 'DAT'),
        ('cassette', 'Cassette'),
        ('web', 'WEB'),
        ('bluray', 'Blu-Ray'),
    )

    torrent = models.ForeignKey(Torrent)
    release = models.ForeignKey('Release')
    format = models.TextField(choices=FORMATS)
    bitrate = models.TextField(choices=BITRATE)
    media = models.TextField(choices=MEDIA)
    logfile = models.TextField(blank=True, null=True)
    uploader = models.ForeignKey(User)

    def __unicode__(self):
        return self.release.name


class Artist(TimeStampedModel):
    discogs_id = models.TextField()
    name = models.TextField()
    sort_name = models.SlugField()
    related_artists = models.ManyToManyField('self', related_name="artist_related_artists", blank=True, null=True)
    artist_type = models.ForeignKey('ArtistType')
    country = models.ForeignKey('Country')
    gender = models.TextField()
    disambiguation = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    birthdate = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return str(self.name)


class ArtistType(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class ArtistAlias(models.Model):
    alias = models.TextField()
    artist = models.ForeignKey('Artist')

    def __unicode__(self):
        return self.alias


class Country(models.Model):
    name = models.TextField()
    code = models.TextField()

    def __unicode__(self):
        return "{} ({})".format(self.name, self.code)


class Release(TimeStampedModel):
    RELEASE_TYPES = (
        ('album', 'Album'),
        ('soundtrack', 'Soundtrack'),
        ('ep', 'EP'),
        ('anthology', 'Anthology'),
        ('compilation', 'Compilation'),
        ('djmix', 'DJ Mix'),
        ('Single', 'single'),
        ('livealbum', 'Live Album'),
        ('remix', 'Remix'),
        ('bootleg','Bootleg'),
        ('interview', 'Interview'),
        ('mixtape', 'Mixtape'),
        ('unknown', 'Unknown')
    )

    discogs_id = models.TextField()
    name = models.TextField()
    artist_credit = models.ManyToManyField('Artist')
    country = models.ForeignKey('Country')
    date = models.DateField()
    barcode = models.TextField()
    comment = models.TextField()
    release_type = models.TextField(choices=RELEASE_TYPES)
    tags = TaggableManager()

    def __unicode__(self):
        return str(self.name)


class ReleaseGroup(TimeStampedModel):
    mbid = models.TextField()
    name = models.ForeignKey('ReleaseName')
    credit = models.ForeignKey('ArtistCredit')
    comment = models.TextField()

    def __unicode__(self):
        return str(self.name)
