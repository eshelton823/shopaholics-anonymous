# import unittest
from django.test import Client
from django.contrib.staticfiles import finders
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from users.models import Profile, Order
from django.utils import timezone
import mock
from shop.views import match, reset, swap
# import shop.views

# def match():
#     print('matching!')
#     # NOTE: Currently a person could be matched to their own order!! Decide as a team if that's OK or not
#     drivers = Profile.objects.filter(is_matching=True).order_by('started_matching')
#     orders = Order.objects.filter(driver="").order_by('order_placed')
#     queuedrivers = []
#     queueorders = []
#     for driver in drivers:
#         queuedrivers.append(driver)
#     for order in orders:
#         queueorders.append(order)
#     while len(queuedrivers) > 0 and len(queueorders) > 0:
#         d = queuedrivers.pop(0)
#         o = queueorders.pop(0)
#         d.has_order = True
#         d.is_matching = False
#         d.started_matching = None
#         d.save()
#         o.order_start_time = timezone.now()
#         o.driver = d.email
#         o.save()
#     return True

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
        # User.objects.create_user(username="customer1", password='12345', email='c1@email.com')
        # User.objects.get(username="customer1").profile.is_shopping=True
        # User.objects.create_user(username="customer2", password='12345', email='c2@email.com')
        # User.objects.get(username="customer2").profile.is_shopping = True
        #has no order
        User.objects.create_user(username="customer3", password='12345', email='c3@email.com')
        u1 = User.objects.get(username="customer3")
        u1.profile.is_shopping = True
        u1.profile.email = u1.email
        u1.save()
        # User.objects.create_user(username="customer4", password='12345', email='c4@email.com')
        # User.objects.create_user(username="customer5", password='12345', email='c5@email.com')

        #has order
        # User.objects.create_user(username="driver1", password='12345', email='d1@email.com')
        # User.objects.get(username="driver1").profile.has_order=True

        #is matching
        # User.objects.create_user(username="driver2", password='12345', email='d2@email.com')
        # User.objects.get(username="driver2").profile.is_matching=True
        # User.objects.get(username="driver2").profile.start_matching=timezone.now() + timezone.timedelta(days=-1)


        User.objects.create_user(username="driver3", password='12345', email='d3@email.com')
        d1 = User.objects.get(username="driver3")
        d1.profile.is_matching = True
        d1.profile.started_matching = timezone.now() + timezone.timedelta(days=-2)
        d1.profile.email = d1.email
        d1.save()
        # print(User.objects.get(username="driver3").profile.is_matching)
        # User.objects.create_user(username="driver4", password='12345', email='d4@email.com')
        #
        # #in limbo
        # User.objects.create_user(username="driver5", password='12345', email='d5@email.com')

        #is matching, has order
        b1 = User.objects.create_user(username="both1", password='12345', email='b1@email.com')
        b1.profile.is_matching = True
        b1.profile.started_matching = timezone.now()
        b1.profile.email = b1.email
        b1.profile.is_shopping = True
        b1.save()

        #is matching, no order
        # User.objects.create_user(username="both2", password='12345', email='b2@email.com')
        # User.objects.get(username="both2").profile.is_matching=True
        #
        # #in limbo
        # User.objects.create_user(username="both3", password='12345', email='b3@email.com')

        #matched order
        # Order.objects.create(user='c1@email.com', driver='d1@email.com', order_cost=45.00, store_selection="WAL")
        #
        # #waiting for matches
        # Order.objects.create(user='c2@email.com', driver='d1@email.com', store_selection="WAL")
        Order.objects.create(user='c3@email.com', order_placed = timezone.now() + timezone.timedelta(days=-1), delivery_instructions="drop check", store_selection="WAL", order_cost=45)
        Order.objects.create(user='b1@email.com', order_placed=timezone.now() + timezone.timedelta(hours=-1), store_selection="WAL")

        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.get(email='c3@email.com')

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_earlier_driver(self, mock_match):
        mock_match()
        o3 = Order.objects.get(user='c3@email.com')
        self.assertEqual(o3.driver, 'd3@email.com')

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_earlier_order(self, mock_match):
        mock_match()
        o1 = Order.objects.get(user='c3@email.com')
        self.assertNotEqual(o1.driver, "")

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_multiple(self, mock_match):
        mock_match()
        o1 = Order.objects.get(user='c3@email.com')
        o2 = Order.objects.get(user='b1@email.com')
        self.assertTrue(o1.driver != "" and o2.driver != "")

    @mock.patch('shop.views.reset', side_effect=reset)
    def test_drop_unmatched_not_shopping(self, mock_reset):
        request = self.factory.get('/dashboard')
        # self.user = User.objects.get(user='c3@gmail.com')
        request.user = self.user
        # print(request.user.email)
        # print(request.user.profile.is_shopping)
        mock_reset(request)
        # print(request.user.email)
        # print(request.user.profile.is_shopping)
        self.assertFalse(request.user.profile.is_shopping)

    @mock.patch('shop.views.reset', side_effect=reset)
    def test_drop_unmatched_order_unlinked(self, mock_reset):
        request = self.factory.get('/dashboard')
        request.user = self.user
        mock_reset(request)
        o1 = Order.objects.get(delivery_instructions="drop check")
        self.assertEquals(o1.user, "DROPPED")

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_user(self, mock_reset, mock_match):
        mock_match()
        request = self.factory.get('/dashboard')
        request.user = self.user
        # request.user = User.objects.get(user='c3@gmail.com')
        mock_reset(request)
        self.assertFalse(request.user.profile.is_shopping)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_driver(self, mock_reset, mock_match):
        mock_match()
        request = self.client.get('/dashboard')
        request.user = self.user
        mock_reset(request)
        d = User.objects.get(email="d3@email.com")
        self.assertFalse(d.profile.has_order)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_driver_match(self, mock_reset, mock_match):
        mock_match()
        request = self.client.get('/dashboard')
        request.user = self.user
        mock_reset(request)
        d = User.objects.get(email="d3@email.com")
        self.assertFalse(d.profile.is_matching)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_order(self, mock_reset, mock_match):
        mock_match()
        # print("here2")
        request = self.client.get('/dashboard')
        request.user = self.user
        mock_reset(request)
        o1 = Order.objects.get(delivery_instructions="drop check")
        self.assertEquals(o1.user, "COMPLETE")

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_driver_gets_money(self, mock_reset, mock_match):
        mock_match()
        # print("here2")
        request = self.client.get('/dashboard')
        request.user = self.user
        o1 = Order.objects.get(delivery_instructions="drop check")
        driver = Profile.objects.get(email=o1.driver).email
        mock_reset(request)
        d1 = Profile.objects.get(email=driver)
        self.assertEquals(d1.money_earned, 45.0)


