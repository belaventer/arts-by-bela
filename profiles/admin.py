from django.contrib import admin
from . import models


@admin.register(models.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'first_name',
        'last_name',
    )
