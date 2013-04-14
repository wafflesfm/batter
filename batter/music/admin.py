from django.contrib import admin

from music.models import MusicUpload, Artist, ArtistType, ArtistAlias, \
    Country, Release

                
admin.site.register(Artist)
admin.site.register(Release)
admin.site.register(MusicUpload)
admin.site.register(ArtistType)
admin.site.register(ArtistAlias)
admin.site.register(Country)
