from torrents.models import DescendingMixin


class MockChild(object):
    parent = object  # space filler


class OrphanedChild(object):
    pass


class CustomNewMixin(object):
    def __new__(cls, was_set, *args, **kwargs):
        obj = object.__new__(cls)
        obj._was_set = was_set
        return obj

    @property
    def was_set(self):
        return hasattr(self, "_was_set") and self._was_set


class CustomNew(DescendingMixin, CustomNewMixin):
    _children = object  # space filler

    def get_child_model(self):
        return MockChild


class WithoutGFKOrChildren(DescendingMixin):
    def get_child_model(self):
        return MockChild


class WithoutParentOfChild(DescendingMixin):
    def get_child_model(self):
        return OrphanedChild
