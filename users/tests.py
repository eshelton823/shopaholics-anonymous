import unittest
from django.test import Client
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from users.models import Profile, Order
from django.utils import timezone
import mock
from shop.views import match, reset, swap
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

# Create your tests here.
class UserModelTests(TestCase):
    def setUp(self):
        # These tsests need a user.
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # Every test needs a client.
        self.client = Client()

    def testCreated(self):
        print(self.user, self.user.password)
        self.assertNotEqual(self.user, None)

    def testHasProfile(self):
        print("Shopping?", self.user.profile.is_shopping)
        self.assertNotEqual(self.user.profile, None)

class ManualLoginTests(TestCase):
    def setUp(self):
        User.objects.create(username="u1", password=make_password("u2"), email="u1@email.com")
        u1 = User.objects.get(username='u1')
        u1.logout()
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.get(username="u1")

    def test_login_success(self):
        data = {'username': 'u1', 'password': 'u2'}
        response = self.client.post("/validate_login/", data)
        # redirect = response.status_code
        self.assertTrue(User.objects.get(username='u1').is_authenticated)

    def test_login_failure_username(self):
        data = {'username': 'u2', 'password': 'u2'}
        response = self.client.post("/validate_login/", data)
        self.assertFalse(User.objects.get(username='u1').is_authenticated)

    def test_login_failure_password(self):
        data = {'username': 'u2', 'password': 'u3'}
        response = self.client.post("/validate_login/", data)
        self.assertFalse(User.objects.get(username='u1').is_authenticated)