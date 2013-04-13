import bencode


def test_parse_torrent(torrentFile):
    t = bencode.bdecode(open(torrentFile, 'rb').read())
    return t


if __name__ == '__main__':
    print test_parse_torrent('test.torrent')
