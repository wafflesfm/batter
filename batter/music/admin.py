from django.contrib import admin

from music.models import Artist, Master #, ArtistAlias, Label, MusicUpload, \
#    Release


admin.site.register(Artist)
admin.site.register(Master)
#~ admin.site.register(Label)
#~ admin.site.register(MusicUpload)
#~ admin.site.register(Release)
