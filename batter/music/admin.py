from django.contrib import admin

from music.models import Artist, ArtistAlias, Label, MusicUpload, \
    Release


admin.site.register(Artist)
admin.site.register(ArtistAlias)
admin.site.register(Label)
admin.site.register(MusicUpload)
admin.site.register(Release)
