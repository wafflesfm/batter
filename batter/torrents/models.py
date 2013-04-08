import base64
import json
import binascii

from bencode import *

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Torrent(models.Model):
    """
    Torrent :: Model
    Django model for storing uploaded torrent info

    notes:
    `files` is a textfield that stores the filetree/single file as a json string
    `pieces` is a sha1 bytestring ascii encoded. see `views.upload.parse_torrent`
    """

    uploader = models.ForeignKey(User)

    creation_date = models.PositiveIntegerField() #utc timestamp
    files = models.TextField()
    name = models.CharField(max_length=150)
    piece_length = models.PositiveIntegerField()
    pieces = models.TextField()
    client = models.CharField(max_length=200)
    encoding = models.CharField(max_length=20)

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