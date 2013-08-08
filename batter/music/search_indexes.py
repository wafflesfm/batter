from haystack import indexes

from .models import Artist, Master


class ArtistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class MasterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Master

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
