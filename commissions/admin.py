from django.contrib import admin
from . import models


@admin.register(models.Resolution, models.Size)
class PriceAdmin(admin.ModelAdmin):
    """
    Admin Class for Resolution and Size models
    """
    list_display = (
        '__str__',
        'price_factor'
    )

    ordering = ('price_factor',)


@admin.register(models.Commission)
class CommissionAdmin(admin.ModelAdmin):
    """
    Admin Class for Commission model
    """
    list_display = (
        '__str__',
        'description',
        'order_total'
    )

    readonly_fields = ('order_total',)


@admin.register(models.WIP)
class WIPAdmin(admin.ModelAdmin):
    """
    Admin Class for WIP model
    """
    list_display = (
        '__str__',
        'client_comment',
    )


@admin.register(models.Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    """
    Admin Class for Artwork model
    """
    list_display = (
        '__str__',
        'final_illustration',
        'client_review',
    )
