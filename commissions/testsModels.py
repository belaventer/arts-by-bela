from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from profiles.models import UserProfile
from commissions import models


class TestModels(TestCase):

    def test_resolution_defaults_and_string(self):
        test_res = models.Resolution.objects.create()

        self.assertEqual(test_res.resolution, '72 dpi')
        self.assertEqual(test_res.price_factor, 1)
        self.assertEqual(str(test_res), test_res.resolution)

    def test_size_defaults_and_string(self):
        test_size = models.Size.objects.create()

        self.assertEqual(test_size.size, 'A7 74 x 105 mm')
        self.assertEqual(test_size.price_factor, 1)
        self.assertEqual(str(test_size), test_size.size)

    def test_commission_model(self):
        # Create test file solution found in
        # https://stackoverflow.com/questions/11170425/
        # how-to-unit-test-file-upload-in-django
        image_one = SimpleUploadedFile(
            'one.png', b'file_content', content_type='image/png')
        image_two = SimpleUploadedFile(
            'two.png', b'file_content', content_type='image/png')
        image_three = SimpleUploadedFile(
            'three.png', b'file_content', content_type='image/png')
        image_four = SimpleUploadedFile(
            'four.png', b'file_content', content_type='image/png')
        image_five = SimpleUploadedFile(
            'five.png', b'file_content', content_type='image/png')

        test_res = models.Resolution.objects.create(
            resolution='72 dpi', price_factor=1)
        test_size = models.Size.objects.create(
            size='A7 74 x 105 mm', price_factor=1)
        test_user = User.objects.create(
            username='TestUser', password='TestPass')
        test_user_profile = UserProfile.objects.create(
            user=test_user)
        test_commission = models.Commission.objects.create(
            user_profile=test_user_profile, name='Test',
            description='Test', resolution_price=test_res,
            size_price=test_size, number_characters=2,
            reference_image_one=image_one,
            reference_image_two=image_two,
            reference_image_three=image_three,
            reference_image_four=image_four,
            reference_image_five=image_five)

        self.assertEqual(
            str(test_commission),
            f'{test_commission.order_number}: {test_commission.name}')
        self.assertEqual(
            test_commission.order_total,
            5*test_size.price_factor*test_res.price_factor +
            2*test_commission.number_characters)

        self.assertEqual(
            test_commission.reference_image_one.name,
            f'{test_commission.order_number}/references/one.png')
        self.assertEqual(
            test_commission.reference_image_two.name,
            f'{test_commission.order_number}/references/two.png')
        self.assertEqual(
            test_commission.reference_image_three.name,
            f'{test_commission.order_number}/references/three.png')
        self.assertEqual(
            test_commission.reference_image_four.name,
            f'{test_commission.order_number}/references/four.png')
        self.assertEqual(
            test_commission.reference_image_five.name,
            f'{test_commission.order_number}/references/five.png')

        test_commission.reference_image_one.delete(save=True)
        test_commission.reference_image_two.delete(save=True)
        test_commission.reference_image_three.delete(save=True)
        test_commission.reference_image_four.delete(save=True)
        test_commission.reference_image_five.delete(save=True)
        test_commission.delete()

    def test_commission_file_reupload(self):
        image_one = SimpleUploadedFile(
            'one.png', b'file_content',
            content_type='image/png')
        test_res = models.Resolution.objects.create(
            resolution='72 dpi', price_factor=1)
        test_size = models.Size.objects.create(
            size='A7 74 x 105 mm', price_factor=1)
        test_user = User.objects.create(
            username='TestUser', password='TestPass')
        test_user_profile = UserProfile.objects.create(
            user=test_user)
        test_commission = models.Commission.objects.create(
            user_profile=test_user_profile, name='Test',
            description='Test', resolution_price=test_res,
            size_price=test_size, number_characters=2,
            reference_image_one=image_one)

        test_commission.reference_image_one = \
            test_commission.reference_image_one

        test_commission.save()

        self.assertEqual(
            test_commission.reference_image_one.name,
            f'{test_commission.order_number}/references/one.png')

        test_commission.reference_image_one.delete(save=True)

    def test_wip_model(self):
        test_res = models.Resolution.objects.create(
            resolution='72 dpi', price_factor=1)
        test_size = models.Size.objects.create(
            size='A7 74 x 105 mm', price_factor=1)
        test_user = User.objects.create(
            username='TestUser', password='TestPass')
        test_user_profile = UserProfile.objects.create(
            user=test_user)
        test_commission = models.Commission.objects.create(
            user_profile=test_user_profile, name='Test',
            description='Test', resolution_price=test_res,
            size_price=test_size, number_characters=2)
        image_one = SimpleUploadedFile(
            'one.png', b'file_content',
            content_type='image/png')
        wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=image_one)

        self.assertEqual(
            str(wip),
            f'{wip.commission.order_number}: {wip.commission.name}')

        self.assertEqual(
            wip.wip_illustration.name,
            f'{test_commission.order_number}/WIP/one.png')

        wip.wip_illustration = wip.wip_illustration
        wip.save()

        self.assertEqual(
            wip.wip_illustration.name,
            f'{test_commission.order_number}/WIP/one.png')
        wip.wip_illustration.delete()

    def test_artwork_model(self):
        test_res = models.Resolution.objects.create(
            resolution='72 dpi', price_factor=1)
        test_size = models.Size.objects.create(
            size='A7 74 x 105 mm', price_factor=1)
        test_user = User.objects.create(
            username='TestUser', password='TestPass')
        test_user_profile = UserProfile.objects.create(
            user=test_user)
        test_commission = models.Commission.objects.create(
            user_profile=test_user_profile, name='Test',
            description='Test', resolution_price=test_res,
            size_price=test_size, number_characters=2)
        image_one = SimpleUploadedFile(
            'one.png', b'file_content',
            content_type='image/png')
        artwork = models.Artwork.objects.create(
            commission=test_commission, final_illustration=image_one)

        self.assertEqual(
            str(artwork),
            f'{artwork.commission.order_number}: {artwork.commission.name}')

        self.assertEqual(
            artwork.final_illustration.name,
            f'{test_commission.order_number}/one.png')

        artwork.final_illustration = artwork.final_illustration
        artwork.save()

        self.assertEqual(
            artwork.final_illustration.name,
            f'{test_commission.order_number}/one.png')
        artwork.final_illustration.delete()
