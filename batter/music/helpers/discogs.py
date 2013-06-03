import requests


class DiscogsAPI(object):
    base_url = 'http://api.discogs.com'
    user_agent = "WaffleBatter/0.1 +https://github.com/wafflesfm/batter"

    def make_request(self, path, **kwargs):
        """sets user-agent for discogs request and returns a python dict
        from the json response
        """
        url = self.base_url + path
        headers = {
            'User-Agent': self.user_agent
        }
        params = {
            'per_page': 25
        }
        params.update(kwargs)
        request = requests.get(url, params=params, headers=headers)
        return request.json()

    def search(self, query, search_type=None, page=1, **kwargs):
        """uses make_request to return a generator of paginated responses
        from discogs
        """
        params = {'q': query}

        if search_type is not None:
            params['type'] = search_type

        return self.make_request('/database/search', **params)

    def get_artist(self, artist_id):
        return self.make_request('/artists/{0}'.format(artist_id))

    def get_master(self, master_id):
        return self.make_request('/masters/{0}'.format(master_id))

    def get_release(self, release_id):
        return self.make_request('/releases/{0}'.format(release_id))

    def get_releases(self, artist_id, page=1):
        """Generator to fetch all releases for given `artist_id`

        ``get_releases(45).next()`` returns a generator for all
        pages of releases

        takes options page argument for starting page
        """
        page = int(page)
        page += 1

        releases = self.make_request('/artists/{0}/releases'.format(artist_id))
        yield releases

        while page < releases['pagination']['pages']:
            params = {'page': page}
            yield self.make_request(
                '/artists/{0}/releases'.format(artist_id),
                **params
            )
            page += 1
