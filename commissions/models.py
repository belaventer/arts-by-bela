import uuid

from django.db import models

from profiles.models import UserProfile


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


class Commission(models.Model):

    order_number = models.CharField(
        max_length=32, null=False, editable=False,
        unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT,
                                     null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField()
    resolution_price = models.ForeignKey(
        'Resolution', on_delete=models.PROTECT,
        null=False, blank=False,
    )
    size_price = models.ForeignKey(
        'Size', on_delete=models.PROTECT,
        null=False, blank=False,
    )
    number_characters = models.SmallIntegerField(
        default=0, null=False, blank=False)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=False, default=0)
    reference_image_one = models.ImageField(null=True, blank=True)
    reference_image_two = models.ImageField(null=True, blank=True)
    reference_image_three = models.ImageField(null=True, blank=True)
    reference_image_four = models.ImageField(null=True, blank=True)
    reference_image_five = models.ImageField(null=True, blank=True)

    def _generate_order_number(self):
        """
        Generate a random, unique commission number using UUID
        """
        return uuid.uuid4().hex.upper()

    def _calculate_order_total(self):
        """
        Calculate commission cost
        """
        self.order_total = (
            5*self.resolution_price.price_factor*self.size_price.price_factor
            + 2*self.number_characters)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        self._calculate_order_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_number}: {self.name}'
