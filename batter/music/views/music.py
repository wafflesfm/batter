from ..models import Artist, Master
from .generic import EnforcingSlugDetailView


class ArtistView(EnforcingSlugDetailView):
    model = Artist


class MasterView(EnforcingSlugDetailView):
    model = Master
