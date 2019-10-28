import unittest
from django.test import Client
from django.contrib.staticfiles import finders
from django.test import TestCase

# Create your tests here.
class PageTests(TestCase):
    def setUp(self):
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
    def testStorePage(self):
        #Get store page
        response = self.client.get("/store")
        #Check it's 302 -- redirect on no sign in.
        self.assertEqual(response.status_code, 302)
    def testCSS(self):
        #Get store page
        response = finders.find("custom.css")
        #Check it's 200

        self.assertIn("custom.css", response)
        self.assertNotEqual(response, None)
