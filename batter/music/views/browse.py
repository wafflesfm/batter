from __future__ import absolute_import, unicode_literals

import pprint
import urllib

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from .api.discogs import discog

def search(request, q):
    return HttpResponse(q)

def view_artist(request, artist_slug):
    artist_name = from_url(artist_slug)
    generated_artist_slug = to_url(artist_name)

    # Ensure a canonical resource url for each artist
    # E.g. /music/Avril Lavigne -> /music/Avril+Lavigne
    if generated_artist_slug != artist_slug:
        return redirect("music_view_artist", artist_slug=generated_artist_slug)

    results = discog.search(artist_name, search_type="artist")

    artist_result = None
    for result in results['results']:
        # Check if the current resource is the desired artist.
        if result['title'] == artist_name:
            artist_result = result
            break

    # If we don't have a title match, redirect to the search page
    if artist_result is None:
        return redirect('music_view_search', q=artist_url)

    # Otherwise, get is the desired artist from the returned ID.
    artist = discog.get_artist(artist_result['id'])

    return render(request, 'music/view_artist.html', {'artist': artist})

def view_master(request, artist_slug, master_slug):
    return HttpResponse(discog.search(master, search_type="master", artist=artist))

def to_url(string):
    return urllib.quote_plus(string)

def from_url(string):
    return urllib.unquote_plus(string)
