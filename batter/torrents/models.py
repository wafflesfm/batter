import base64
import bencode
import binascii
import json

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from jsonfield import JSONField

optional = {'null': True, 'blank': True}

class Torrent(models.Model):
    """Django model for storing uploaded torrent info"""

    """The announce URL of the tracker (string)"""
    announce = models.TextField()
    """(optional) this is an extention to the official specification, offering backwards-compatibility. (list of lists of strings)."""
    announce_list = JSONField()
    """(optional) the creation time of the torrent, in standard UNIX epoch format (integer, seconds since 1-Jan-1970 00:00:00 UTC)"""
    creation_date = models.PositiveIntegerField(**optional) # UTC timestamp
    """(optional) free-form textual comments of the author (string)"""
    comment = models.TextField(**optional)
    """(optional) name and version of the program used to create the .torrent (string)"""
    created_by = models.TextField(**optional)
    """(optional) the string encoding format used to generate the pieces part of the info dictionary in the .torrent metafile (string)"""
    encoding = models.TextField(**optional)
    """(info/) number of bytes in each piece (integer)"""
    piece_length = models.PositiveIntegerField()
    """(info/) string consisting of the concatenation of all 20-byte SHA1 hash values, one per piece (byte string, i.e. not urlencoded)"""
    pieces = models.TextField(unique=True)
    """(info/) whether or not the client may obtain peer data from other means; e.g. PEX or DHT"""
    private = models.BooleanField()
    """(info/) The suggested name of the torrent file, if the torrent is single-file. Otherwise, the suggested name of the directory in which to put files"""
    name = models.TextField()
    """(info/single-file) length of the file in bytes. None if the torrent is multi-file"""
    length = models.PositiveIntegerField(**optional)
    """(info/single-file, optional) a 32-character hexadecimal string corresponding to the MD5 sum of the file"""
    md5sum = models.TextField(**optional)
    """(info/multi-file) a list of {name, length, md5sum} dicts corresponding to the files tracked by the torrent"""
    files = JSONField(**optional)

    @classmethod
    def from_torrent_file(cls, torrent_file, *args, **kwargs):
        torrent_dict = bencode.bdecode(torrent_file.read())
        
        torrent = cls()
        torrent.announce = torrent_dict['announce']
        torrent.announce_list = torrent_dict.get('announce-list')
        torrent.creation_date = torrent_dict.get('creation date')
        torrent.comment = torrent_dict.get('comment')
        torrent.created_by = torrent_dict.get('created by')
        torrent.encoding = torrent_dict.get('encoding')
        torrent.piece_length = torrent_dict['info'].get('piece length')
        torrent.pieces = binascii.hexlify(torrent_dict['info'].get('pieces'))
        torrent.private = True if torrent_dict['info'].get('private', 0) == 1 else False
        torrent.name = torrent_dict['info'].get('name')
        torrent.length = torrent_dict['info'].get('length')
        torrent.md5sum = torrent_dict['info'].get('md5sum')
        torrent.files = torrent_dict['info'].get('files')
        return torrent

    def generate_torrent(self, *args, **kwargs):
        torrent = {}
        torrent['info'] = {}

        torrent['creation date'] = self.creation_date
        torrent['announce'] = settings.TRACKERURL
        torrent['created by'] = self.client.encode('utf-8', 'ignore')
        torrent['encoding'] = self.encoding.encode('utf-8', 'ignore')

        print self.files
        files = json.loads(self.files.replace("'", '"'), object_hook=_decode_dict)

        torrent['info']['piece length'] = self.piece_length
        torrent['info']['pieces'] = binascii.unhexlify(self.pieces)
        torrent['info']['private'] = 1

        if len(files) > 1: #multi-file mode
            torrent['info']['files'] = files
            torrent['info']['name'] = self.name.encode('utf-8', 'ignore')

        else: #single file mode
            torrent['info']['name'] = self.name.encode('utf-8', 'ignore')
            torrent['info']['length'] = files[0]['length']
        
        return bencode(torrent)

    def __unicode__(self):
        return self.name


#helper functions so our json returns python strings and not unicode
def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
           key = key.encode('utf-8')
        if isinstance(value, unicode):
           value = value.encode('utf-8')
        elif isinstance(value, list):
           value = _decode_list(value)
        elif isinstance(value, dict):
           value = _decode_dict(value)
        rv[key] = value
    return rv
