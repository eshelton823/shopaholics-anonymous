import unittest
from django.test import Client
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
        #Check it's 200
        self.assertEqual(response.status_code, 200)
