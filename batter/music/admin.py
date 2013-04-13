from django.contrib import admin

from . import models

admin.site.register(models.Artist)
admin.site.register(models.ArtistAlias)
admin.site.register(models.ArtistType)
admin.site.register(models.Country)
admin.site.register(models.Release)
admin.site.register(models.MusicUpload)
