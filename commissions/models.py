from django.db import models


class Resolution(models.Model):

    class ResolutionsChoices(models.TextChoices):
        LOW = '72 dpi'
        MEDIUM = '144 dpi'
        HIGH = '300 dpi'

    resolution = models.CharField(
        choices=ResolutionsChoices.choices,
        default=ResolutionsChoices.LOW,
        unique=True,
        max_length=7,
    )

    price_factor = models.DecimalField(
        default=1, max_digits=4, decimal_places=2)

    def __str__(self):
        return self.resolution


class Size(models.Model):

    class SizesChoices(models.TextChoices):
        A4 = 'A4 210 x 297 mm'
        A5 = 'A5 148 x 210 mm'
        A6 = 'A6 105 x 148 mm'
        A7 = 'A7 74 x 105 mm'

    size = models.CharField(
        choices=SizesChoices.choices,
        default=SizesChoices.A7,
        unique=True,
        max_length=15,
    )

    price_factor = models.DecimalField(
        default=1, max_digits=4, decimal_places=2)

    def __str__(self):
        return self.size
