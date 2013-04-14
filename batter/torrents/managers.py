from django.db.models.query import QuerySet
from django.db.models import Manager


class InheritingQuerySet(QuerySet):
    def iterator(self):
        for obj in super(InheritingQuerySet, self).iterator():
            yield obj.get_child_object()


class InheritingManager(Manager):
    def get_query_set(self):
        return InheritingQuerySet(self.model)
