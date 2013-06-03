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

    response = discog.search(artist_name, search_type="artist")

    artist_result = None
    for result in response['results']:
        # Check if the current resource is the desired artist.
        if result['title'] == artist_name:
            artist_result = result
            break

    # If we don't have a title match, redirect to the search page
    if artist_result is None:
        return redirect('music_view_search', q=artist_url)

    # Otherwise, get the desired artist from the returned ID.
    artist = discog.get_artist(artist_result['id'])

    return render(request, 'music/view_artist.html', {'artist': artist})


def view_master(request, artist_slug, master_slug):
    artist_name = from_url(artist_slug)
    generated_artist_slug = to_url(artist_name)

    master_name = from_url(master_slug)
    generated_master_slug = to_url(master_slug)

    # Ensure a canonical resource url for each artist
    # E.g. /music/Avril Lavigne/Let Go
    #      -> /music/Avril+Lavigne/Let+Go
    if (generated_artist_slug != artist_slug or
       generated_master_slug != generated_master_slug):
        return redirect("music_view_master",
                        artist_slug=generated_artist_slug,
                        master_slug=generated_master_slug)

    query = "{0} - {1}".format(artist_name, master_name)
    response = discog.search(query, search_type="master")

    master_result = None
    for result in response['results']:
        # Check if the current resource is the desired master.
        if result['title'] == query:
            master_result = result
            break

    # If we don't have a title match, redirect to the search page
    if master_result is None:
        return redirect('music_view_search', q=query)

    # Otherwise, get the desired master from the returned ID.
    master = discog.get_master(master_result['id'])

    return render(request, 'music/view_master.html', {'master': master})


def to_url(string):
    return urllib.quote_plus(string)


def from_url(string):
    return urllib.unquote_plus(string)
