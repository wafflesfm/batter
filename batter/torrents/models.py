import bencode
import binascii
import collections

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import EMPTY_VALUES
from django.conf import settings

from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from jsonfield import JSONField

from . import managers

optional = {'null': True, 'blank': True}


class Torrent(models.Model):
    """Django model for storing uploaded torrent info"""

    """The announce URL of the tracker (string)"""
    announce = models.TextField()
    """(optional) this is an extension to the official specification,
                  offering backwards-compatibility.
                  (list of lists of strings)."""
    announce_list = JSONField(**optional)
    """(optional) the creation time of the torrent,
                  in standard UNIX epoch format
                  (integer, seconds since 1-Jan-1970 00:00:00 UTC)"""
    creation_date = models.PositiveIntegerField(**optional)
    """(optional) free-form textual comments of the author (string)"""
    comment = models.TextField(**optional)
    """(optional) name and version of the program used to create
                  the .torrent (string)"""
    created_by = models.TextField(**optional)
    """(optional) the string encoding format used to generate the pieces part
                  of the info dictionary in the .torrent metafile (string)"""
    encoding = models.TextField(**optional)
    """(info/) number of bytes in each piece (integer)"""
    piece_length = models.PositiveIntegerField()
    """(info/) string consisting of the concatenation of all 20-byte SHA1
               hash values, one per piece (byte string, not urlencoded)"""
    pieces = models.TextField(unique=True)
    """(info/) whether or not the client may obtain peer data from other means
               e.g. PEX or DHT"""
    private = models.BooleanField()
    """(info/) The suggested name of the torrent file, if single-file torrent.
               Otherwise, the suggested name of the directory
               in which to put files"""
    name = models.TextField()
    """(info/single-file) length of the file in bytes.
                          None if the torrent is multi-file"""
    length = models.PositiveIntegerField(**optional)
    """(info/single-file, optional) a 32-character hexadecimal string
                                    corresponding to the file's MD5 sum"""
    md5sum = models.TextField(**optional)
    """(info/multi-file) a list of {name, length, md5sum} dicts
                         corresponding to the files tracked by the torrent"""
    files = JSONField(**optional)

    @classmethod
    def from_torrent_file(cls, torrent_file, *args, **kwargs):
        torrent_dict = bencode.bdecode(torrent_file.read())
        return cls.from_torrent_dict(torrent_dict, *args, **kwargs)

    @classmethod
    def from_torrent_dict(cls, torrent_dict, *args, **kwargs):
        info_dict = torrent_dict['info']
        torrent = cls()
        torrent.announce = torrent_dict['announce']
        torrent.announce_list = torrent_dict.get('announce-list')
        torrent.creation_date = torrent_dict.get('creation date')
        torrent.comment = torrent_dict.get('comment')
        torrent.created_by = torrent_dict.get('created by')
        torrent.encoding = torrent_dict.get('encoding')
        torrent.piece_length = info_dict.get('piece length')
        torrent.pieces = binascii.hexlify(info_dict.get('pieces'))
        torrent.private = True if info_dict.get('private', 0) == 1 else False
        torrent.name = info_dict.get('name')
        torrent.length = info_dict.get('length')
        torrent.md5sum = info_dict.get('md5sum')
        torrent.files = info_dict.get('files')
        return torrent

    def get_absolute_url(self):
        return reverse('torrents_view', args=[str(self.id)])

    def to_bencoded_string(self, *args, **kwargs):
        torrent = {}
        torrent['info'] = {}

        torrent['announce'] = convert(self.announce)
        if self.announce_list not in EMPTY_VALUES:
            torrent['announce-list'] = convert(self.announce_list)
        if self.creation_date not in EMPTY_VALUES:
            torrent['creation date'] = self.creation_date
        if self.comment not in EMPTY_VALUES:
            torrent['comment'] = convert(self.comment)
        if self.created_by not in EMPTY_VALUES:
            torrent['created by'] = convert(self.created_by)
        if self.encoding not in EMPTY_VALUES:
            torrent['encoding'] = convert(self.encoding)

        torrent['info']['piece length'] = self.piece_length
        torrent['info']['pieces'] = binascii.unhexlify(self.pieces)
        if self.private:
            torrent['info']['private'] = 1
        torrent['info']['name'] = convert(self.name)

        if self.files is not None and len(self.files) > 1:  # multi-file mode
            torrent['info']['files'] = convert(self.files)

        else:  # single file mode
            torrent['info']['length'] = self.length
            if self.md5sum is not None:
                torrent['info']['md5sum'] = convert(self.md5sum)

        return bencode.bencode(torrent)

    def __unicode__(self):
        return self.name


class InheritingModel(models.Model):
    _child_name = models.CharField(max_length=100, editable=False)

    objects = managers.InheritingManager()
    base_objects = models.Manager()

    def save(self, *args, **kwargs):
        # NB: based on http://djangosnippets.org/snippets/1037/
        self._child_name = self.get_child_name()
        super(InheritingModel, self).save(*args, **kwargs)

    def get_child_name(self):
        if type(self) is self.get_parent_model():
            return self._child_name
        return self.get_parent_link().related_query_name()

    def get_child_object(self):
        return getattr(self, self.get_child_name())

    def get_parent_link(self):
        return self._meta.parents[self.get_parent_model()]

    def get_parent_model(self):  # pragma: no cover
        # this method is excluded from coverage purely because it should never
        # be run. at all. it's only here so you know you have to override it.
        raise NotImplementedError

    def get_parent_object(self):
        return getattr(self, self.get_parent_link().name)

    class Meta:
        abstract = True


class Upload(InheritingModel, TimeStampedModel):
    torrent = models.OneToOneField(
        Torrent,
        related_name='upload',
        null=False
    )
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    parent = models.ForeignKey(
        'TorrentGroup',
        null=False,
        related_name='uploads'
    )

    def get_parent_model(self):
        return Upload


class TorrentGroup(InheritingModel, TimeStampedModel):
    tags = TaggableManager()

    def get_parent_model(self):
        return TorrentGroup


def convert(data):
    """ Converts unicode (or a dict/Mapping/Iterable containing unicode
    strings) to str. """
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
