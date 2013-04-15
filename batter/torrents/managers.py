from django.db.models.query import QuerySet
from django.db.models import Manager


class InheritingQuerySet(QuerySet):
    def iterator(self):
        for obj in super(InheritingQuerySet, self).iterator():
            yield obj.get_child_object()


class InheritingManager(Manager):
    def get_query_set(self):
        # renamed to get_queryset in future versions of Django
        return InheritingQuerySet(self.model)


class DescendingManager(Manager):
    def has_child(self, child):
        # this basically just returns child.parent
        # with some additional validation

        # someone might want to contribute a has_descendant at some point
        if isinstance(child.parent, self.model):
            return self.get_query_set().get(pk=child.parent.id)
        else:
            raise self.model.DoesNotExist


class InheritingDescendingManager(DescendingManager, InheritingManager):
    pass
