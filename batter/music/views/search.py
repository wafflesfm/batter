from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


class SearchView(FacetedSearchView):
    def __init__(self, *args, **kwargs):
        sqs = SearchQuerySet().facet('degrees')
        kwargs.update({
            'searchqueryset': sqs
        })
        super(SearchView, self).__init__(*args, **kwargs)
