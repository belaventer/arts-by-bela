from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from profiles.models import UserProfile
from commissions.models import Artwork, Resolution, Size


class TestViews(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            username="TestUser", password="TestPass",
            is_superuser=True)
        self.test_user_profile = UserProfile.objects.get(
            user=self.test_user)
        image_path = f'./{settings.MEDIA_URL}logo.png'
        self.test_image = SimpleUploadedFile(
            'logo.png',
            content=open(image_path, 'rb').read(),
            content_type='image/png')

    def test_showcase(self):
        response = self.client.get('/showcase/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'showcase/showcase.html')

    def test_add_personal_work_no_login(self):
        response = self.client.get('/showcase/add/')
        self.assertRedirects(
            response, '/accounts/login/?next=/showcase/add/')

    def test_add_personal_work_not_superuser(self):
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.get(
            user=test_user_two)
        self.client.force_login(user=test_user_two)
        response = self.client.get('/showcase/add/')
        self.assertRedirects(
            response, '/showcase/')
        test_user_profile_two.delete()
        test_user_two.delete()

    def test_add_personal_work_login(self):
        self.client.force_login(user=self.test_user)
        response = self.client.get('/showcase/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'showcase/personal_work.html')

    def test_add_personal_work_invalid(self):
        test_res = Resolution.objects.create()
        test_size = Size.objects.create()
        self.client.force_login(user=self.test_user)
        response = self.client.post(
            '/showcase/add/', {
                'name': 'Add new personal work with invalid form inputs \
                    and verify it is not accepted',
                'description': 'Test artwork added',
                'illustration': self.test_image})
        self.assertEqual(response.status_code, 200)
        add_artwork = Artwork.objects.count()

        self.assertEqual(add_artwork, 0)
        test_res.delete()
        test_size.delete()

    def test_add_personal_work_valid(self):
        self.client.force_login(user=self.test_user)
        response = self.client.post(
            '/showcase/add/', {
                'name': 'Add valid new personal work',
                'description': 'Test artwork added',
                'illustration': self.test_image})
        self.assertRedirects(
            response, '/showcase/')
        test_artwork = get_object_or_404(
            Artwork, client_review='Test artwork added')

        self.assertEqual(
            test_artwork.commission.user_profile, self.test_user_profile)

        test_artwork.final_illustration.delete()
