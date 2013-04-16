from django.test import TestCase

from .. import mixins


class DescendingMixinTests(TestCase):
    def test_custom_new(self):
        custom_new = mixins.CustomNew(was_set=True)
        self.assertTrue(custom_new.was_set)

    def test_without_gfk_or_children(self):
        with self.assertRaises(AttributeError):
            mixins.WithoutGFKOrChildren()

    def test_without_parent_of_child(self):
        with self.assertRaises(AttributeError):
            mixins.WithoutParentOfChild()
