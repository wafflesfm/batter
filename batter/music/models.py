from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext as _

from django_countries import CountryField
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

from torrents.models import Upload, UploadGroup, DescendingModel

from .types import FORMAT_TYPES, BITRATE_TYPES, MEDIA_TYPES, RELEASE_TYPES


class NamedTimeStampedModel(TimeStampedModel):
    name = models.TextField()
    slug = models.SlugField(max_length=255)

    class Meta:
        abstract = True


#~ @python_2_unicode_compatible
#~ class TaggableModel(models.Model):
    #~ tags = TaggableManager()
    #~ 
    #~ class Meta:
        #~ abstract = True

#~ @python_2_unicode_compatible
#~ class MusicUpload(Upload):
    #~ release = models.ForeignKey('Release')
    #~ release_format = models.TextField(choices=FORMAT_TYPES)
    #~ bitrate = models.TextField(choices=BITRATE_TYPES)
    #~ media = models.TextField(choices=MEDIA_TYPES)
    #~ logfile = models.TextField(blank=True, null=True)
    #~ parent = models.ForeignKey('Release', related_name='_children')
#~ 
    #~ class Meta:
        #~ verbose_name = _('music upload')
        #~ verbose_name_plural = _('music uploads')
#~ 
    #~ def __str__(self):
        #~ return "{0} / {1} / {2}".format(
            #~ self.master.release,
            #~ force_text(self.format),
            #~ force_text(self.bitrate)
        #~ )
#~ 


@python_2_unicode_compatible
class Artist(NamedTimeStampedModel):
#    discogs_id = models.PositiveIntegerField(unique=True)
#    slug = models.TextField()
#    realname = models.TextField()
#    profile = models.TextField(blank=True)

    class Meta:
        verbose_name = _('artist')
        verbose_name_plural = _('artists')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('music_artist_detail', kwargs={'pk': self.pk, 'slug': self.slug})

#~ 
#~ 
#~ @python_2_unicode_compatible
#~ class Release(DescendingModel, TimeStampedModel):
    #~ name = models.TextField()
    #~ discogs_id = models.PositiveIntegerField()
    #~ artist_credit = models.ManyToManyField('Artist')
    #~ comment = models.TextField()
    #~ label = models.ForeignKey('Label')
    #~ release_type = models.TextField(choices=RELEASE_TYPES)
    #~ country = CountryField()
    #~ date = models.DateField()
    #~ parent = models.ForeignKey('Master', related_name='_children')
#~ 
    #~ class Meta:
        #~ verbose_name = _('release')
        #~ verbose_name_plural = _('releases')
#~ 
    #~ def get_child_model(self):
        #~ return MusicUpload
#~ 
    #~ def __str__(self):
        #~ return force_text(self.name)


@python_2_unicode_compatible
class Master(NamedTimeStampedModel):
#    discogs_id = models.PositiveIntegerField()
    artists = models.ManyToManyField('Artist', blank=True, null=True)

    class Meta:
        verbose_name = _('master')
        verbose_name_plural = _('masters')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music_master_detail', kwargs={'pk': self.pk, 'slug': self.slug})


#~ @python_2_unicode_compatible
#~ class Label(TimeStampedModel):
    #~ name = models.TextField()
    #~ parent_label = models.ForeignKey('self', blank=True, null=True)
#~ 
    #~ class Meta:
        #~ verbose_name = _('master')
        #~ verbose_name_plural = _('masters')
#~ 
    #~ def is_vanity(self):
        #~ return bool(self.parent_label)
#~ 
    #~ def __str__(self):
        #~ return force_text(self.name)
