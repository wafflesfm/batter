from django.contrib import admin

from achievements.models import Achievement, AchievementOwnership


class AchievementAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }
    list_display = (
        'slug', 'title', 'description', 'secrecy_type'
    )


class AchievementOwnershipAdmin(admin.ModelAdmin):
    list_display = (
        'achievement', 'user', 'date_granted', 'grant_reason'
    )


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementOwnership, AchievementOwnershipAdmin)
