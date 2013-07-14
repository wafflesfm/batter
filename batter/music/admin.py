from django.contrib import admin

from music.models import Artist, Master, Release #, ArtistAlias, Label, MusicUpload


admin.site.register(Artist)
admin.site.register(Master)
admin.site.register(Release)
#~ admin.site.register(Label)
#~ admin.site.register(MusicUpload)
