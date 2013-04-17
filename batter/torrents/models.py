from __future__ import absolute_import, unicode_literals

import binascii

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible, force_bytes
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import bencode
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

from . import managers


@python_2_unicode_compatible
class Torrent(models.Model):
    announce = models.URLField(help_text=_("The announce URL of the tracker."))
    announce_list = JSONField(blank=True, null=True)
    creation_date = models.PositiveIntegerField(
        blank=True, null=True,
        help_text=_("Torrent creation time in UNIX epoch format."))
    comment = models.TextField(
        blank=True, null=True,
        help_text=_("Free-form textual comment of the torrent author."))
    created_by = models.TextField(
        blank=True, null=True,
        help_text=_("Name and version of the program used to create the "
                    "torrent."))
    encoding = models.TextField(
        blank=True, null=True,
        help_text=_("Encoding used to generate the pieces part of the info "
                    "dictionary in the torrent metadata"))
    piece_length = models.PositiveIntegerField(
        blank=True, null=True,
        help_text=_("Number of bytes in each piece"))
    pieces = models.TextField(
        unique=True,
        help_text=_("A concatenation of all 20-byte SHA1 hash values of the "
                    "torrent's pieces"))
    is_private = models.BooleanField(
        help_text=_("Whether or not the client may obtain peer data from "
                    "other sources (PEX, DHT)."))
    name = models.TextField(
        help_text=_("The suggested name of the torrent file, if single-file "
                    "torrent, otherwise, the suggest name of the directory "
                    "in which to put the files"))
    length = models.PositiveIntegerField(
        blank=True, null=True,
        help_text=_("Length of the file contents in bytes, missing for "
                    "multi-file torrents."))
    md5sum = models.CharField(
        blank=True, null=True, max_length=32,
        help_text=_("MD5 hash of the file contents (single-file torrent "
                    " only)."))
    files = JSONField(
        blank=True, null=True,
        help_text=_("A list of {name, length, md5sum} dicts corresponding to "
                    "the files tracked by the torrent"))

    def get_absolute_url(self):
        return reverse('torrents_view', args=[self.pk])

    @classmethod
    def from_torrent_file(cls, torrent_file, *args, **kwargs):
        torrent_dict = bencode.bdecode(torrent_file.read())
        return cls.from_torrent_dict(torrent_dict, *args, **kwargs)

    @classmethod
    def from_torrent_dict(cls, torrent_dict, *args, **kwargs):
        info_dict = torrent_dict[b'info']
        return cls(
            announce=torrent_dict[b'announce'],
            announce_list=torrent_dict.get(b'announce-list'),
            creation_date=torrent_dict.get(b'creation date'),
            created_by=torrent_dict.get(b'created by'),
            comment=torrent_dict.get(b'comment'),
            encoding=torrent_dict.get(b'encoding'),
            piece_length=info_dict.get(b'piece length'),
            pieces=binascii.hexlify(info_dict.get(b'pieces')),
            is_private=info_dict.get(b'private', 0) == 1,
            name=info_dict.get(b'name'),
            length=info_dict.get(b'length'),
            md5sum=info_dict.get(b'md5sum'),
            files=info_dict.get(b'files'))

    @property
    def is_single_file(self):
        return self.files is None or len(self.files) <= 1

    def to_bencoded_string(self, *args, **kwargs):
        torrent = {
            'announce': self.announce,
            'announce-list': self.announce_list,
            'creation date': self.creation_date,
            'comment': self.comment,
            'created by': self.created_by,
            'encoding': self.encoding,
        }

        torrent['info'] = info_dict = {
            'piece length': self.piece_length,
            'pieces': binascii.unhexlify(self.pieces),
            'private': int(self.is_private),
            'name': self.name
        }
        if self.is_single_file:
            info_dict['length'] = self.length
            info_dict['md5sum'] = self.md5sum
        else:
            info_dict['files'] = self.files

        return bencode.bencode(
            recursive_force_bytes(recursive_drop_falsy(torrent)))

    def __str__(self):
        return self.name


class InheritingModel(models.Model):
    _subclass_name = models.CharField(max_length=100, editable=False)

    objects = managers.InheritingManager()
    base_objects = models.Manager()

    def save(self, *args, **kwargs):
        # NB: based on http://djangosnippets.org/snippets/1037/
        self._subclass_name = self.get_subclass_name()
        super(InheritingModel, self).save(*args, **kwargs)

    def get_subclass_name(self):
        if type(self) is self.get_superclass_model():
            return self._subclass_name
        return self.get_superclass_link().related_query_name()

    def get_subclass_object(self):
        return getattr(self, self.get_subclass_name())

    def get_superclass_link(self):
        return self._meta.parents[self.get_superclass_model()]

    def get_superclass_model(self):  # pragma: no cover
        # this method is excluded from coverage purely because it should never
        # be run. at all. it's only here so you know you have to override it.
        raise NotImplementedError

    def get_superclass_object(self):
        return getattr(self, self.get_superclass_link().name)

    class Meta:
        abstract = True


class DescendingMixin(object):
    def __new__(cls, *args, **kwargs):
        superme = super(DescendingMixin, cls)
        if superme.__new__ is object.__new__:  # object.__new__ takes no params
            obj = superme.__new__(cls)
        else:
            obj = superme.__new__(cls, *args, **kwargs)

        child_model = obj.get_child_model()
        if not hasattr(child_model, 'parent'):
            raise AttributeError("Classes using DescendingMixin must have a " +
                                 "GenericForeignKey or ForeignKey named " +
                                 "'parent' on their child model")

        if not isinstance(child_model.parent, generic.GenericForeignKey) \
                and not hasattr(cls, '_children'):
            raise AttributeError("Classes using DescendingMixin must have a " +
                                 "GenericForeignKey on their child model " +
                                 "or must have a ForeignKey with a " +
                                 "related_name of '_children' on their " +
                                 "child model")
        return obj

    @property
    def children(self):
        child_model = self.get_child_model()
        if isinstance(child_model.parent, generic.GenericForeignKey):
            self_type = ContentType.objects.get_for_model(self)
            return child_model.objects.filter(
                parent_content_type__pk=self_type.id,
                parent_object_id=self.id
            )
        else:
            return self._children

    def get_child_model(self):  # pragma: no cover
        """
        Override this on a per-subclass basis if you want your UploadGroup
        to have different child classes. See the Upload class comments above
        for more information on why this might be the case.
        """
        raise NotImplementedError


class InheritingDescendingModel(DescendingMixin, InheritingModel):
    objects = managers.InheritingDescendingManager()
    base_objects = managers.DescendingManager()

    class Meta:
        abstract = True


class DescendingModel(DescendingMixin, models.Model):
    objects = managers.DescendingManager()

    class Meta:
        abstract = True


class Upload(InheritingModel, TimeStampedModel):
    torrent = models.OneToOneField(
        Torrent,
        related_name='upload',
        null=False
    )
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)

    # we use a GenericForeignKey to handle the case that you might have
    # a model that goes between "Upload" and "UploadGroup" - e.g.
    # a Waffles-style "Release"
    #
    # an example implementation of this can be found in
    # torrents_inheritance_tests
    #
    # if you do not use this in your site, you may wish to replace this
    # with the simpler:
    # parent = models.ForeignKey(
    #     'UploadGroup', null=False, related_name='children'
    # )
    parent_content_type = models.ForeignKey(ContentType)
    parent_object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey(
        'parent_content_type', 'parent_object_id'
    )

    # this is used for quickly getting to all the uploads associated with
    # an UploadGroup
    upload_group = models.ForeignKey('UploadGroup', related_name='uploads')

    def save(self, *args, **kwargs):
        # rewrite my upload_group
        current = self
        while not isinstance(current, UploadGroup):
            current = current.parent
        self.upload_group = current

        super(Upload, self).save(*args, **kwargs)

    @staticmethod
    def get_superclass_model():
        return Upload


class UploadGroup(InheritingDescendingModel, TimeStampedModel):
    tags = TaggableManager()

    @staticmethod
    def get_child_model():
        return Upload

    @staticmethod
    def get_superclass_model():
        return UploadGroup


def recursive_drop_falsy(d):
    """Recursively drops falsy values from a given data structure."""
    if isinstance(d, dict):
        return dict((k, recursive_drop_falsy(v)) for k, v in d.items() if v)
    elif isinstance(d, list):
        return map(recursive_drop_falsy, d)
    elif isinstance(d, basestring):
        return force_bytes(d)
    else:
        return d


def recursive_force_bytes(d):
    """Recursively walks a given data structure and coerces all string-like
    values to :class:`bytes`."""
    if isinstance(d, dict):
        # Note(superbobry): 'bencode' forces us to use byte keys.
        return dict((force_bytes(k), recursive_force_bytes(v))
                    for k, v in d.items() if v)
    elif isinstance(d, list):
        return map(recursive_force_bytes, d)
    elif isinstance(d, basestring):
        return force_bytes(d)
    else:
        return d
