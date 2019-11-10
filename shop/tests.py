import unittest
from django.test import Client
from django.contrib.staticfiles import finders
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from users.models import Profile, Order
from django.utils import timezone
from shop.views import match, reset, swap

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
    def testStorePageDashboardLoggedOut(self):
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
    def testStorePageDashboardLoggedIn(self):
        login = self.client.login(username='testuser', password='12345')
        #Get dashboard
        response = self.client.get("/dashboard")
        #Check it's 200, now signed in
        self.assertEqual(response.status_code, 200)

class MatchTests(TestCase):
    def setUp(self):
        #has order
        User.objects.create_user(username="customer1", password='12345', email='c1@email.com')
        User.objects.get(username="customer1").profile.is_shopping=True
        User.objects.create_user(username="customer2", password='12345', email='c2@email.com')
        User.objects.get(username="customer2").profile.is_shopping = True
        #has no order
        User.objects.create_user(username="customer3", password='12345', email='c3@email.com')
        User.objects.get(username="customer3").profile.is_shopping = True
        # User.objects.create_user(username="customer4", password='12345', email='c4@email.com')
        # User.objects.create_user(username="customer5", password='12345', email='c5@email.com')

        #has order
        User.objects.create_user(username="driver1", password='12345', email='d1@email.com')
        User.objects.get(username="driver1").profile.has_order=True

        #is matching
        User.objects.create_user(username="driver2", password='12345', email='d2@email.com')
        User.objects.get(username="driver2").profile.is_matching=True
        User.objects.get(username="driver2").profile.start_matching=timezone.now() + timezone.timedelta(days=-1)


        User.objects.create_user(username="driver3", password='12345', email='d3@email.com')
        User.objects.get(username="driver3").profile.is_matching = True
        User.objects.get(username="driver3").profile.start_matching = timezone.now() + timezone.timedelta(days=-2)
        # User.objects.create_user(username="driver4", password='12345', email='d4@email.com')
        #
        # #in limbo
        # User.objects.create_user(username="driver5", password='12345', email='d5@email.com')

        #is matching, has order
        User.objects.create_user(username="both1", password='12345', email='b1@email.com')
        User.objects.get(username="both1").profile.is_matching = True
        User.objects.get(username="both1").profile.start_matching = timezone.now()
        User.objects.get(username="both1").profile.is_matching = True
        User.objects.get(username="both1").profile.is_shopping = True
        #is matching, no order
        # User.objects.create_user(username="both2", password='12345', email='b2@email.com',is_matching=True)
        #
        # #in limbo
        # User.objects.create_user(username="both3", password='12345', email='b3@email.com')

        #matched order
        # Order.objects.create(user='c1@email.com', driver='d1@email.com', order_cost=45.00, store_selection="WAL")
        #
        # #waiting for matches
        # Order.objects.create(user='c2@email.com', driver='d1@email.com', store_selection="WAL")
        Order.objects.create(user='c3@email.com', order_placed = timezone.now() + timezone.timedelta(days=-1), delivery_instructions="drop check", store_selection="WAL")
        # Order.objects.create(user='b1@email.com', order_placed=timezone.now() + timezone.timedelta(hours=-1), store_selection="WAL")

        self.factory = RequestFactory()
        self.client = Client()

    def test_match_earlier_driver(self):
        self.user = User.objects.get(email='c3@email.com')
        self.client.get('/dashboard')
        self.client.get('shop:match')
        o3 = Order.objects.get(user='c3@email.com')
        self.assertEqual(o3.driver, 'd3@email.com')

    def test_match_earlier_order(self):
        match()
        o1 = Order.objects.get(user='c3@email.com')
        self.assertNotEqual(o1.driver, "")

    def test_match_multiple(self):
        match()
        o1 = Order.objects.get(user='c3@email.com')
        o2 = Order.objects.get(user='b1@email.com')
        self.assertTrue(o1.driver != "" and o2.driver != "")

    def test_drop_unmatched_not_shopping(self):
        request = self.client.get('/dashboard')
        request.user = User.objects.get(user='c3@gmail.com')
        reset(request)
        self.assertFalse(request.user.profile.is_shopping)

    def test_drop_unmatched_order_unlinked(self):
        request = self.client.get('/dashboard')
        request.user = User.objects.get(user='c3@gmail.com')
        reset(request)
        o1 = Order.objects.get(delivery_instructions="drop check")
        self.assertEquals(o1.user, "DROPPED")

    def test_resolve_order_user(self):
        match()
        request = self.client.get('/dashboard')
        request.user = User.objects.get(user='c3@gmail.com')
        reset(request)
        self.assertFalse(request.user.profile.is_shopping)

    def test_resolve_order_driver(self):
        match()
        request = self.client.get('/dashboard')
        request.user = User.objects.get(email='c3@gmail.com')
        reset(request)
        d = User.objects.get(email="d3@email.com")
        self.assertFalse(d.profile.has_order)

    def test_resolve_order_driver_match(self):
        match()
        request = self.client.get('/dashboard')
        request.user = User.objects.get(email='c3@gmail.com')
        reset(request)
        d = User.objects.get(email="d3@email.com")
        self.assertFalse(d.profile.is_matching)

    def test_resolve_order_order(self):
        match()
        print("here2")
        request = self.client.get('/dashboard')
        request.user = User.objects.get(email='c3@gmail.com')
        reset(request)
        o1 = Order.objects.get(delivery_instructions="drop check")
        self.assertEquals(o1.user, "COMPLETED")



