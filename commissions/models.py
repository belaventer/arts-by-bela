from django.db import models


class Resolution(models.Model):
    LOW = 72
    MEDIUM = 144
    HIGH = 300
    RESOLUTIONS_CHOICES = [
        (LOW, '72 dpi'),
        (MEDIUM, '144 dpi'),
        (HIGH, '300 dpi'),
    ]
    resolution = models.IntegerField(
        choices=RESOLUTIONS_CHOICES,
        default=HIGH,
        unique=True
    )

    price_factor = models.DecimalField(
        default=1, max_digits=4, decimal_places=2)

    def __str__(self, RESOLUTIONS_CHOICES=RESOLUTIONS_CHOICES):
        for choice in RESOLUTIONS_CHOICES:
            if self.resolution == choice[0]:
                return choice[1]


class Size(models.Model):
    A4 = '210 x 297 mm'
    A5 = '148 x 210 mm'
    A6 = '105 x 148 mm'
    A7 = '74 x 105 mm'
    SIZES_CHOICES = [
        (A4, 'A4'),
        (A5, 'A5'),
        (A6, 'A6'),
        (A7, 'A7'),
    ]
    size = models.CharField(
        choices=SIZES_CHOICES,
        default=A6,
        unique=True,
        max_length=12,
    )

    price_factor = models.DecimalField(
        default=1, max_digits=4, decimal_places=2)

    def __str__(self, SIZES_CHOICES=SIZES_CHOICES):
        for choice in SIZES_CHOICES:
            if self.size == choice[0]:
                return choice[1]
