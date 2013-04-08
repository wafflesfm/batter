from django.contrib import admin

from .models import Artist, ArtistCredit, ArtistGender, ArtistName
from .models import ArtistType, Country, Release, ReleaseName
from .models import ReleaseGroup

admin.site.register(Artist)
admin.site.register(ArtistCredit)
admin.site.register(ArtistGender)
admin.site.register(ArtistName)
admin.site.register(ArtistType)
admin.site.register(Country)
admin.site.register(Release)
admin.site.register(ReleaseName)
admin.site.register(ReleaseGroup)
