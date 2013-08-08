from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeStampedModel

optional = {'blank': True, 'null': True}


@python_2_unicode_compatible
class MusicBaseModel(TimeStampedModel):
    name = models.TextField()
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to="music_image", **optional)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class MusicUpload(TimeStampedModel):
    release = models.ForeignKey('Release')
    torrent = models.OneToOneField('torrents.Torrent')
#    release_format = models.TextField(choices=FORMAT_TYPES)
#    bitrate = models.TextField(choices=BITRATE_TYPES)
#    media = models.TextField(choices=MEDIA_TYPES)
#    logfile = models.TextField(blank=True, null=True)
#    parent = models.ForeignKey('Release', related_name='_children')

    class Meta:
        verbose_name = _('Music Upload')
        verbose_name_plural = _('Music Uploads')

    def __str__(self):
        return "{} - {}".format(self.release, self.torrent)


class Artist(MusicBaseModel):
    summary = models.TextField(blank=True)
    # TODO: Add more types of url (last.fm, spotify, etc)?
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')

    def get_absolute_url(self):
        return reverse('music_artist_detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})


@python_2_unicode_compatible
class Master(MusicBaseModel):
    artists = models.ManyToManyField('Artist', **optional)
    main = models.ForeignKey('Release', related_name='+', **optional)

    class Meta:
        verbose_name = _('Master')
        verbose_name_plural = _('Masters')

    def get_absolute_url(self):
        return reverse('music_master_detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return "{} - {}".format(", ".join(artist.name
                                          for artist
                                          in self.artists.all()),
                                self.name)


@python_2_unicode_compatible
class Release(TimeStampedModel):
    master = models.ForeignKey('Master')
    label = models.ForeignKey('Label', **optional)
    release_type = Choices(('album', _('Album')),
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
                           ('concertrecording', _('Concert Recording')),
                           ('demo', _('Demo')),
                           ('unknown', _('Unknown')))
    year = models.PositiveIntegerField(**optional)
    catalog_num = models.TextField(blank=True)
    name = models.TextField(blank=True)
    scene = models.BooleanField()

    class Meta:
        verbose_name = _('Release')
        verbose_name_plural = _('Releases')

    def __str__(self):
        return "{} ({})".format(self.master, self.name)


@python_2_unicode_compatible
class Label(TimeStampedModel):
    name = models.TextField()
    parent_label = models.ForeignKey('self', **optional)

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    def __str__(self):
        return "{}".format(self.name)
