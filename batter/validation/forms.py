from __future__ import absolute_import, unicode_literals

from django import forms


class FieldRuleWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.Select(), # field_name # TODO: choices from content type (if possible)
                   forms.Select(choices=[]), # comparator # TODO: choices
                   forms.TextInput(),) # value
        super(FieldRuleWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        # take in a dict representing a fieldrule, turn into list
        # TODO: the necessary
        pass


class FieldRuleFormfield(forms.MultiValueField):
    widget = FieldRuleWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.ChoiceField(), # field_name # TODO choices from content_type (if possible)
            forms.ChoiceField(), # comparator # TODO choices
            forms.CharField(), # value #TODO dynamic fieldtype from contenttype
        )
        super(FieldRuleFormfield, self).__init__(fields, *args, **kwargs)

    def compress(self, values):
        # take in values list from
        # turn into dict and
        # check the validate_dict on FieldRule
        pass


class ValidationRuleForm(forms.ModelForm):
    trigger_condition = FieldRuleFormfield()
    validation_condition = FieldRuleFormfield()

    def clean(self):
        cleaned_data = super(ValidationRuleForm, self).clean()
        # TODO: check that the data in the conditions fits the ContentTypes
        # cooresponding field type, and that the field type exists
        return cleaned_data
