from django.db import models

from model_utils.models import TimeStampedModel

class Artist(TimeStampedModel):
    mbid = models.TextField()
    name = models.ForeignKey('ArtistName', related_name="artist_name")
    sort_name = models.ForeignKey('ArtistName', related_name="artist_sort_name")
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    type = models.ForeignKey('ArtistType')
    country = models.ForeignKey('ArtistCountry')
    gender = models.ForeignKey('ArtistGender')
    disambiguation = models.TextField()

    def __str__(self):
        return str(self.name)

class ArtistCountry(models.Model):
    name = models.TextField()
    code = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


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

