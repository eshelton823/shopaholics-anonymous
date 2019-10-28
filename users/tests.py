import unittest
from django.test import Client
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.contrib.auth.models import User

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
