from django.contrib import admin

from .models import Artist, ArtistCountry, ArtistGender, ArtistName, ArtistType

admin.site.register(Artist)
admin.site.register(ArtistCountry)
admin.site.register(ArtistGender)
admin.site.register(ArtistName)
admin.site.register(ArtistType)
