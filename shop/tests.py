import unittest
from django.test import Client
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class ViewTests(TestCase):
    def setUp(self):
        # Some tests need a user.
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Every test needs a client.
        self.client = Client()
    def testLogInPage(self):
        #Get sign in page
        response = self.client.get("/profile/signin/")
        #Check it's 200
        self.assertEqual(response.status_code, 200)
    def testHomePage(self): 
        #Get home page
        response = self.client.get("/")
        #Check it's 200
        self.assertEqual(response.status_code, 200)
    def testStorePageLoggedOut(self):
        #Get store page
        response = self.client.get("/store")
        #Check it's 302 -- redirect on no sign in.
        self.assertEqual(response.status_code, 302)
    def testStorePageDashboard(self):
        #Get dashboard
        response = self.client.get("/dashboard")
        #Check it's 302 -- redirect on no sign in.
        self.assertEqual(response.status_code, 302)
    def testCSS(self):
        #Get store page
        response = finders.find("custom.css")
        #Check it's 200
        self.assertIn("custom.css", response)
        self.assertNotEqual(response, None)
    def testStorePageLoggedIn(self):
        login = self.client.login(username='testuser', password='12345')
        #Get store page
        response = self.client.get("/store")
        #Check it's 200, accessible when logged in
        self.assertEqual(response.status_code, 200)
    def testStorePageDashboard(self):
        login = self.client.login(username='testuser', password='12345')
        #Get dashboard
        response = self.client.get("/dashboard")
        #Check it's 200, now signed in
        self.assertEqual(response.status_code, 200)
