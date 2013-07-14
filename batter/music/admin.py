from django.contrib import admin

from music.models import Artist, Master, Release, MusicUpload


admin.site.register(Artist)
admin.site.register(Master)
admin.site.register(Release)
admin.site.register(MusicUpload)
