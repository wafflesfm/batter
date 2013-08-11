from __future__ import absolute_import, unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from jsonfield import JSONField


# TODO: comparators and comparator list, field type validation
# for FieldRule values

class FieldRule(object):
    def __init__(self, field_name):
        # TODO: should take in field, cmparator, value
        self.field_name = field_name

    def to_dict(self):
        """ dictionary representation of the rule """
        pass

    def check_value(self, value):
        pass

    @classmethod
    def from_dict(cls, dictionary):
        """ restore a rule from a dict created with to_dict """
        pass

    @classmethod
    def validate_dict(cls, dictionary):
        """
        check if a dictionary repepresents a valid FieldRule.
        raises a ValidationError if the dictionary is invalid.

        """
        pass


@python_2_unicode_compatible
class ValidationRule(models.Model):
    name = models.CharField(blank=True, null=True, max_length=20)
    description = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType,
        help_text=_("Content Type of the model to which the rule applies"))
    trigger_condition = JSONField(blank=True, null=True,
        validators=(FieldRule.validate_dict,),
        help_text=_("Condition that triggers checking the "
                    "validation_condition. A null/empty value means always "
                    "check the rule."))
    validation_condition = JSONField(
        validators=(FieldRule.validate_dict,),
        help_text=_("The field level constraint to validate"))

    def __str__(self):
        return self.name
