from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from profiles.models import UserProfile
from commissions import models


class TestViews(TestCase):

    def setUp(self):
        self.test_res = models.Resolution.objects.create(
            resolution="72 dpi", price_factor=1)
        self.test_size = models.Size.objects.create(
            size="A7 74 x 105 mm", price_factor=1)
        self.test_user = User.objects.create(
            username="TestUser", password="TestPass")
        self.test_user_profile = UserProfile.objects.create(
            user=self.test_user)
        image_path = f'./{settings.MEDIA_URL}logo.png'
        self.test_image = SimpleUploadedFile(
            'logo.png',
            content=open(image_path, 'rb').read(),
            content_type='image/png')

# New commission view
    def test_new_commission_no_login(self):
        response = self.client.get('/commission/new/')
        self.assertRedirects(
            response, '/accounts/login/?next=/commission/new/')

    def test_new_commission_login(self):
        self.client.force_login(user=self.test_user)
        response = self.client.get('/commission/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commissions/new_commission.html')

    def test_new_commission_invalid(self):
        self.client.force_login(user=self.test_user)
        response = self.client.post('/commission/new/', {
            'name': 'Create new commission with invalid form inputs \
                and verify it is not accepted',
            'description': 'Test commission created',
            'resolution_price': self.test_res,
            'size_price': self.test_size, 'number_characters': 2})
        self.assertEqual(response.status_code, 200)
        commissions = models.Commission.objects.count()

        self.assertEqual(commissions, 0)

    def test_new_commission_valid(self):
        self.client.force_login(user=self.test_user)
        response = self.client.post('/commission/new/', {
            'name': 'Valid commission',
            'description': 'Test commission created',
            'resolution_price': self.test_res,
            'size_price': self.test_size, 'number_characters': 2})
        test_commission = get_object_or_404(
            models.Commission, name='Valid commission')

        self.assertRedirects(
            response, f'/payment/{test_commission.id}/')

        self.assertEqual(test_commission.user_profile, self.test_user_profile)
        test_commission.delete()

# Edit commission view
    def test_edit_commission_no_login(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        response = self.client.get(f'/commission/edit/{test_commission.id}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/commission/edit/{test_commission.id}/')
        test_commission.delete()

    def test_edit_wrong_user(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.create(
            user=test_user_two)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/commission/edit/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_user_two.delete()
        test_user_profile_two.delete()
        test_commission.delete()

    def test_redirect_wip_exists(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/edit/{test_commission.id}/')
        self.assertRedirects(
            response, f'/commission/wip/{test_commission.id}/')
        test_commission.delete()
        test_wip.delete()

    def test_redirect_artwork_exists(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/edit/{test_commission.id}/')
        self.assertRedirects(
            response, f'/commission/artwork/{test_commission.id}/')
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_edit_commission_login(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        response = self.client.get(f'/commission/edit/{test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commissions/edit_commission.html')
        test_commission.delete()

    def test_edit_commission_invalid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        response = self.client.post(
            f'/commission/edit/{test_commission.id}/', {
                'name': 'Edit commission with invalid form inputs \
                    and verify it is not accepted',
                'description': 'Test commission edited',
                'resolution_price': self.test_res,
                'size_price': self.test_size, 'number_characters': 2})
        self.assertEqual(response.status_code, 200)
        updated_commission = get_object_or_404(
            models.Commission, pk=test_commission.id)

        self.assertEqual(updated_commission.name, test_commission.name)
        test_commission.delete()

    def test_edit_commission_valid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        response = self.client.post(
            f'/commission/edit/{test_commission.id}/', {
                'name': 'Valid updated commission',
                'description': 'Test commission created',
                'resolution_price': self.test_res,
                'size_price': self.test_size, 'number_characters': 2})

        test_commission.refresh_from_db()
        self.assertRedirects(
            response, f'/payment/{test_commission.id}/')

        self.assertEqual(test_commission.name, 'Valid updated commission')
        test_commission.delete()

# Delete commission view
    def test_delete_commission_no_login(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        response = self.client.get(f'/commission/delete/{test_commission.id}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/commission/delete/{test_commission.id}/')
        test_commission.delete()

    def test_delete_wrong_user(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.create(
            user=test_user_two)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/commission/delete/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_user_two.delete()
        test_user_profile_two.delete()
        test_commission.delete()

    def test_delete_payment_exists(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/delete/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_commission.delete()
        test_wip.delete()

    def test_delete_success(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/delete/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        existing_commissions = models.Commission.objects.filter(
            id=test_commission.id)
        self.assertEqual(len(existing_commissions), 0)
        test_commission.delete()

# WIP commission view
    def test_wip_no_login(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        response = self.client.get(f'/commission/wip/{test_commission.id}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/commission/wip/{test_commission.id}/')
        test_commission.delete()
        test_wip.delete()

    def test_wip_wrong_user(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.create(
            user=test_user_two)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/commission/wip/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_user_two.delete()
        test_user_profile_two.delete()
        test_commission.delete()
        test_wip.delete()

    def test_redirect_no_wip(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/wip/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_commission.delete()

    def test_wip_redirect_artwork_exists(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/wip/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_wip.delete()
        test_wip.wip_illustration.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_wip_login(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        response = self.client.get(f'/commission/wip/{test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commissions/wip_details.html')
        test_commission.delete()
        test_wip.delete()

    def test_wip_login_superuser(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass", is_superuser=True)
        test_user_profile_two = UserProfile.objects.create(
            user=test_user_two)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        self.client.force_login(user=test_user_two)
        response = self.client.get(f'/commission/wip/{test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commissions/wip_details.html')
        test_user_two.delete()
        test_user_profile_two.delete()
        test_commission.delete()
        test_wip.delete()

    def test_wip_illustration_exists(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        image_one = SimpleUploadedFile(
            'one.png', b'',
            content_type='image/png')
        response = self.client.post(f'/commission/wip/{test_commission.id}/', {
            'illustration': image_one})

        self.assertRedirects(
            response, f'/commission/wip/{test_commission.id}/')

        updated_commission = get_object_or_404(
            models.WIP, pk=test_commission.id)

        self.assertEqual(test_wip, updated_commission)
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_commission.delete()

    def test_wip_illustration_invalid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        image_one = SimpleUploadedFile(
            'one.png', b'',
            content_type='image/png')
        response = self.client.post(f'/commission/wip/{test_commission.id}/', {
            'illustration': image_one})
        self.assertEqual(response.status_code, 200)
        updated_commission = get_object_or_404(
            models.WIP, pk=test_commission.id)

        self.assertEqual(test_wip, updated_commission)
        test_commission.delete()
        test_wip.wip_illustration.delete()
        test_wip.delete()

    def test_wip_illustration_valid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        response = self.client.post(f'/commission/wip/{test_commission.id}/', {
            'illustration': self.test_image})

        test_wip.refresh_from_db()
        self.assertRedirects(
            response, f'/commission/wip/{test_commission.id}/')

        self.assertEqual(
            test_wip.wip_illustration.name,
            f'{test_commission.order_number}/WIP/{self.test_image.name}')
        test_commission.delete()
        test_wip.wip_illustration.delete()
        test_wip.delete()

    def test_wip_comment_exists(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, client_comment='client test comment')
        response = self.client.post(f'/commission/wip/{test_commission.id}/', {
            'comment': 'test comment'})

        self.assertRedirects(
            response, f'/commission/wip/{test_commission.id}/')

        updated_commission = get_object_or_404(
            models.WIP, pk=test_commission.id)

        self.assertEqual(test_wip, updated_commission)
        test_wip.delete()
        test_commission.delete()

    def test_wip_comment_invalid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        response = self.client.post(f'/commission/wip/{test_commission.id}/', {
            'comment': ''})
        self.assertEqual(response.status_code, 200)
        updated_commission = get_object_or_404(
            models.WIP, pk=test_commission.id)

        self.assertEqual(test_wip, updated_commission)
        test_commission.delete()
        test_wip.delete()

    def test_wip_comment_valid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(commission=test_commission)
        response = self.client.post(f'/commission/wip/{test_commission.id}/', {
            'comment': 'updated comment text'})

        test_wip.refresh_from_db()
        self.assertRedirects(
            response, '/profile/')

        self.assertEqual(
            test_wip.client_comment, 'updated comment text')

        created_artwork = models.Artwork.objects.count()

        self.assertEqual(
            created_artwork, 1)
        test_commission.delete()
        test_wip.delete()

# Artwork commission view
    def test_artwork_no_login(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        response = self.client.get(
            f'/commission/artwork/{test_commission.id}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/commission/artwork/{test_commission.id}/')
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_wrong_user(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.create(
            user=test_user_two)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/commission/artwork/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_user_two.delete()
        test_user_profile_two.delete()
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_redirect_no_wip(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/artwork/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_commission.delete()

    def test_redirect_no_artwork(self):
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/commission/artwork/{test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_commission.delete()

    def test_artwork_login(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        response = self.client.get(
            f'/commission/artwork/{test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commissions/artwork_details.html')
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_login_superuser(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass", is_superuser=True)
        test_user_profile_two = UserProfile.objects.create(
            user=test_user_two)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/commission/artwork/{test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commissions/artwork_details.html')
        test_user_two.delete()
        test_user_profile_two.delete()
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_illustration_exists(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission, final_illustration=self.test_image)
        test_image = SimpleUploadedFile(
            'logo.png',
            content=open(f'./{settings.MEDIA_URL}logo.png', 'rb').read(),
            content_type='image/png')
        response = self.client.post(
            f'/commission/artwork/{test_commission.id}/', {
                'illustration': test_image})

        test_artwork.refresh_from_db()
        self.assertRedirects(
            response, f'/commission/artwork/{test_commission.id}/')

        updated_commission = get_object_or_404(
            models.Artwork, pk=test_commission.id)

        self.assertEqual(test_artwork, updated_commission)
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.final_illustration.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_illustration_invalid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        image_one = SimpleUploadedFile(
            'one.png', b'',
            content_type='image/png')
        response = self.client.post(
            f'/commission/artwork/{test_commission.id}/', {
                'illustration': image_one})
        self.assertEqual(response.status_code, 200)
        updated_commission = get_object_or_404(
            models.Artwork, pk=test_commission.id)

        self.assertEqual(test_artwork, updated_commission)
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_illustration_valid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        test_image = SimpleUploadedFile(
            'logo.png',
            content=open(f'./{settings.MEDIA_URL}logo.png', 'rb').read(),
            content_type='image/png')
        response = self.client.post(
            f'/commission/artwork/{test_commission.id}/', {
                'illustration': test_image})

        test_artwork.refresh_from_db()
        self.assertRedirects(
            response, f'/commission/artwork/{test_commission.id}/')

        self.assertEqual(
            test_artwork.final_illustration.name,
            f'{test_commission.order_number}/{self.test_image.name}')
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.final_illustration.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_comment_exists(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission, client_review="test review")
        response = self.client.post(
            f'/commission/artwork/{test_commission.id}/', {
                'comment': 'test comment'})

        self.assertRedirects(
            response, f'/commission/artwork/{test_commission.id}/')

        updated_commission = get_object_or_404(
            models.Artwork, pk=test_commission.id)

        self.assertEqual(test_artwork, updated_commission)
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_comment_invalid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        response = self.client.post(
            f'/commission/artwork/{test_commission.id}/', {
                'comment': ''})
        self.assertEqual(response.status_code, 200)
        updated_commission = get_object_or_404(
            models.Artwork, pk=test_commission.id)

        self.assertEqual(test_artwork, updated_commission)
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()

    def test_artwork_comment_valid(self):
        self.client.force_login(user=self.test_user)
        test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)
        test_wip = models.WIP.objects.create(
            commission=test_commission, wip_illustration=self.test_image)
        test_artwork = models.Artwork.objects.create(
            commission=test_commission)
        response = self.client.post(
            f'/commission/artwork/{test_commission.id}/', {
                'comment': 'updated review text'})

        test_artwork.refresh_from_db()
        self.assertRedirects(
            response, '/profile/')

        self.assertEqual(
            test_artwork.client_review, 'updated review text')
        test_wip.wip_illustration.delete()
        test_wip.delete()
        test_artwork.delete()
        test_commission.delete()
