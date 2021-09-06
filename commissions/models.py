import uuid

from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator)

from profiles.models import UserProfile


class Resolution(models.Model):
    """
    A Resolution model for maintaining the
    resolution options of a illustration.
    """

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
    """
    A Size model for maintaining the
    size options of a illustration.
    """

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
    """
    A Commission model for maintaining the
    new illustration request information.
    """

    order_number = models.CharField(
        max_length=32, null=False, editable=False,
        unique=True)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT,
        null=False, blank=False,
        related_name="commissions")
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
        default=0, null=False, blank=False,
        validators=[MaxValueValidator(
            6, message='Please enter a number below 6'),
            MinValueValidator(
            0, message='Please enter a number above 0')])
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

    def _correct_path(self, path, name):
        if name.split('/')[0] == path:
            file_name = name.split('/')[-1]
            return f'{path}/{file_name}'
        else:
            return f'{path}/{name}'

    def _define_file_name(self):
        path = f'{self.order_number}'

        if self.reference_image_one:
            self.reference_image_one.name = self._correct_path(
                path, self.reference_image_one.name)
        if self.reference_image_two:
            self.reference_image_two.name = self._correct_path(
                path, self.reference_image_two.name)
        if self.reference_image_three:
            self.reference_image_three.name = self._correct_path(
                path, self.reference_image_three.name)
        if self.reference_image_four:
            self.reference_image_four.name = self._correct_path(
                path, self.reference_image_four.name)
        if self.reference_image_five:
            self.reference_image_five.name = self._correct_path(
                path, self.reference_image_five.name)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        self._define_file_name()
        self._calculate_order_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_number}: {self.name}'


class WIP(models.Model):
    """
    A Work in Progress (WIP) model
    to link to the Commission once paid
    and hold the WIP illustration and client comment
    """
    commission = models.OneToOneField(
        Commission, on_delete=models.CASCADE,
        related_name="wip")
    client_comment = models.TextField(null=True, blank=True)
    wip_illustration = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.commission.order_number}: {self.commission.name}'
