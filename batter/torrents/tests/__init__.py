from __future__ import unicode_literals

import os.path
from unittest import TestLoader

from django.conf import settings


def suite():   
    return TestLoader().discover("torrents.tests", pattern="*.py")


settings.TEST_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'archlinux-2013.04.01-dual.iso.torrent'
)
