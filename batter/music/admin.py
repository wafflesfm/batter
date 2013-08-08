from django.contrib import admin

from music.models import Artist, Label, Master, MusicUpload, Release


admin.site.register(Artist)
admin.site.register(Label)
admin.site.register(Master)
admin.site.register(MusicUpload)
admin.site.register(Release)
