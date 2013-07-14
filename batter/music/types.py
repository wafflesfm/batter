from django.utils.translation import ugettext as _

UPLOAD_TYPES = (
    ('music', _('Music')),
    ('applications', _('Applications')),
    ('ebooks', _('E-Books')),
    ('audiobooks', _('Audiobooks')),
    ('comedy', _('Comedy / Spoken Word')),
    ('comics', _('Comics')),
)

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
    ('24bitlossless', _('24Bit Lossless')),
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
