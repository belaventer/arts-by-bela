from django.test import TestCase
from django.contrib.auth.models import User

from profiles.models import UserProfile
from commissions import models


class TestViews(TestCase):

    def setUp(self):
        """
        Setup required model Instances on test database
        """
        self.test_res = models.Resolution.objects.create(
            resolution="72 dpi", price_factor=1)
        self.test_size = models.Size.objects.create(
            size="A7 74 x 105 mm", price_factor=1)
        self.test_user = User.objects.create(
            username="TestUser", password="TestPass")
        self.test_user_profile = UserProfile.objects.get(
            user=self.test_user)
        self.test_superuser = User.objects.create(
            username="TestSuperUser", password="TestPass",
            email="testsupermail@someemail.com", is_superuser=True)
        self.test_commission = models.Commission.objects.create(
            user_profile=self.test_user_profile, name="Test",
            description="Test", resolution_price=self.test_res,
            size_price=self.test_size, number_characters=2)

    def test_payment_no_login(self):
        """
        Test login required decorator on payment view
        """
        response = self.client.get(
            f'/payment/{self.test_commission.id}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/payment/{self.test_commission.id}/')

    def test_payment_wrong_user(self):
        """
        Test redirection if logged user is not commission owner
        """
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.get(
            user=test_user_two)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/payment/{self.test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_user_profile_two.delete()
        test_user_two.delete()

    def test_payment_exists(self):
        """
        Test redirection if commission has wip, i.e, was already paid
        """
        test_wip = models.WIP.objects.create(
            commission=self.test_commission)
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/payment/{self.test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_wip.delete()

    def test_payment_required(self):
        """
        Test get response and template of payment view
        """
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/payment/{self.test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment.html')

    def test_payment_success(self):
        """
        Test post response with valid form of payment view
        """
        self.client.force_login(user=self.test_user)
        response = self.client.post(f'/payment/{self.test_commission.id}/')
        self.assertRedirects(
            response, f'/payment/success/{self.test_commission.id}/')
        created_wip = models.WIP.objects.get()
        self.assertEqual(created_wip.commission, self.test_commission)

    def test_payment_success_wrong_user(self):
        """
        Test redirection if logged user is not commission owner
        """
        test_user_two = User.objects.create(
            username="TestUser2", password="TestPass")
        test_user_profile_two = UserProfile.objects.get(
            user=test_user_two)
        self.client.force_login(user=test_user_two)
        response = self.client.get(
            f'/payment/success/{self.test_commission.id}/')
        self.assertRedirects(response, '/profile/')
        test_user_profile_two.delete()
        test_user_two.delete()

    def test_payment_success_template(self):
        """
        Test get response and template of payment_success view
        """
        self.client.force_login(user=self.test_user)
        response = self.client.get(
            f'/payment/success/{self.test_commission.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment_success.html')
