from django.db import models

from model_utils.models import TimeStampedModel


class Artist(TimeStampedModel):
    mbid = models.TextField()
    name = models.ForeignKey(
        'ArtistName',
        related_name="artist_name"
    )
    sort_name = models.ForeignKey(
        'ArtistName',
        related_name="artist_sort_name"
    )
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    type = models.ForeignKey('ArtistType')
    country = models.ForeignKey('Country')
    gender = models.ForeignKey('ArtistGender')
    disambiguation = models.TextField()

    def __str__(self):
        return str(self.name)


class ArtistCredit(models.Model):
    name = models.ForeignKey('ArtistName')
    artists = models.ManyToManyField('Artist')

    def __str__(self):
        return str(self.name)


class ArtistGender(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class ArtistName(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class ArtistType(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.TextField()
    code = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


class Release(TimeStampedModel):
    mbid = models.TextField()
    name = models.ForeignKey('ReleaseName')
    artist_credit = models.ForeignKey('ArtistCredit')
    group = models.ForeignKey('ReleaseGroup')
#    status = models.ForeignKey('ReleaseStatus')
#    packaging = models.ForeignKey('ReleasePackaging')
    country = models.ForeignKey('Country')
    date = models.DateField()
    barcode = models.TextField()
    comment = models.TextField()

    def __str__(self):
        return str(self.name)


class ReleaseName(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


#class ReleasePackaging(models.Model):
#    name = models.TextField()


#class ReleaseStatus(models.Model):
#    name = models.TextField()


class ReleaseGroup(TimeStampedModel):
    mbid = models.TextField()
    name = models.ForeignKey('ReleaseName')
    credit = models.ForeignKey('ArtistCredit')
#    type = models.ForeignKey('ReleaseGroupPrimaryType')
    comment = models.TextField()

    def __str__(self):
        return str(self.name)


#class ReleaseGroupPrimaryType(models.Model):
#    name = models.TextField()
