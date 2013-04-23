from django.contrib import admin

from music.models import MusicUpload, Artist, ArtistType, ArtistAlias, \
    Release, Edition, Label


admin.site.register(Artist)
admin.site.register(Release)
admin.site.register(MusicUpload)
admin.site.register(ArtistType)
admin.site.register(ArtistAlias)
admin.site.register(Edition)
admin.site.register(Label)
