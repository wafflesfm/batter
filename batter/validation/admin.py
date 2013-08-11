from __future__ import unicode_literals

from django.contrib import admin

from validation.models import ValidationRule
from validation.forms import ValidationRuleForm


class ValidationRuleAdmin(admin.ModelAdmin):
    form = ValidationRuleForm

admin.site.register(ValidationRule, ValidationRuleAdmin)
