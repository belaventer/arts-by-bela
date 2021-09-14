from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestViews(TestCase):

    def test_profile_no_login(self):
        """
        Test login required decorator on profile view
        """
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_profile_login(self):
        """
        Test get response and template of profile view
        """
        test_user = User.objects.create(
            username="TestUser", password="TestPass")
        test_user_profile = UserProfile.objects.get(user=test_user)
        self.client.force_login(user=test_user)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        test_user.delete()
        test_user_profile.delete()

    def test_profile_login_superuser(self):
        """
        Test superuser login of profile
        """
        test_user = User.objects.create(
            username="TestUser", password="TestPass", is_superuser=True)
        test_user_profile = UserProfile.objects.get(user=test_user)
        self.client.force_login(user=test_user)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        test_user.delete()
        test_user_profile.delete()

    def test_profile_update(self):
        """
        Test post response with valid form of profile view
        """
        test_user = User.objects.create(
            username="TestUser", password="TestPass")
        test_user_profile = UserProfile.objects.get(user=test_user)
        self.client.force_login(user=test_user)
        response = self.client.post('/profile/', {'first_name': 'Test Name'})
        self.assertEqual(response.status_code, 200)
        updated_profile = UserProfile.objects.get(id=test_user_profile.id)
        self.assertEqual(updated_profile.first_name, 'Test Name')
        test_user.delete()
        test_user_profile.delete()
        updated_profile.delete()

    def test_profile_invalid(self):
        """
        Test post response with invalid form of profile view
        """
        test_user = User.objects.create(
            username="TestUser", password="TestPass")
        test_user_profile = UserProfile.objects.get(user=test_user)
        self.client.force_login(user=test_user)
        response = self.client.post(
            '/profile/', {'first_name': 'datadatadatadatadatadatadatadata'})
        self.assertEqual(response.status_code, 200)
        updated_profile = UserProfile.objects.get(id=test_user_profile.id)
        self.assertFalse(updated_profile.first_name)
        test_user.delete()
        test_user_profile.delete()
        updated_profile.delete()


class TestModels(TestCase):

    def test_userprofile_string_method_returns_username(self):
        """
        Test UserProfile model string method
        """
        test_user = User.objects.create(
            username="TestUser", password="TestPass")
        test_user_profile = UserProfile.objects.get(user=test_user)
        self.assertEqual(str(test_user_profile), test_user.username)
        test_user.delete()
        test_user_profile.delete()
