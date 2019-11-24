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
        User.objects.create_user(username="customer1", password='12345', email='c1@email.com')
        u1 = User.objects.get(username="customer1")
        u1.profile.email = u1.email
        u1.save()

        # User.objects.create_user(username="customer2", password='12345', email='c2@email.com')
        # User.objects.get(username="customer2").profile.is_shopping = True
        #has no order
        User.objects.create_user(username="customer3", password='12345', email='c3@email.com')
        u3 = User.objects.get(username="customer3")
        u3.profile.is_shopping = True
        u3.profile.email = u3.email
        u3.save()
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
        Order.objects.create(user='customer3', order_placed = timezone.now() + timezone.timedelta(days=-1), delivery_instructions="drop check", store_selection="WAL", order_cost=45, has_paid=True)
        Order.objects.create(user='both1', order_placed=timezone.now() + timezone.timedelta(hours=-1), store_selection="WAL", has_paid=True)

        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.get(email='c3@email.com')

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_earlier_driver(self, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        o3 = Order.objects.get(user='customer3')
        self.assertEqual(o3.driver, 'driver3')

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_earlier_order(self, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        o1 = Order.objects.get(user='customer3')
        self.assertNotEqual(o1.driver, "")

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_multiple(self, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        o1 = Order.objects.get(user='customer3')
        o2 = Order.objects.get(user='both1')
        self.assertTrue(o1.driver != "" and o2.driver != "")

    @mock.patch('shop.views.reset', side_effect=reset)
    def test_drop_unmatched_not_shopping(self, mock_reset):
        request = self.factory.get('/dashboard')
        request.user = self.user
        mock_reset(request)
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
        request = self.factory.get('/dashboard')
        mock_match(request)
        request.user = self.user
        mock_reset(request)
        self.assertFalse(request.user.profile.is_shopping)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_driver(self, mock_reset, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        request.user = self.user
        mock_reset(request)
        d = User.objects.get(email="d3@email.com")
        self.assertFalse(d.profile.has_order)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_driver_match(self, mock_reset, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        request.user = self.user
        mock_reset(request)
        d = User.objects.get(email="d3@email.com")
        self.assertFalse(d.profile.is_matching)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_resolve_order_order(self, mock_reset, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        request.user = self.user
        mock_reset(request)
        o1 = Order.objects.get(delivery_instructions="drop check")
        self.assertEquals(o1.user, "COMPLETE")

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_driver_gets_money(self, mock_reset, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        request.user = self.user
        o1 = Order.objects.get(delivery_instructions="drop check")
        driver = User.objects.get(username=o1.driver).profile.email
        mock_reset(request)
        d1 = Profile.objects.get(email=driver)
        self.assertEquals(d1.money_earned, 45.0)

    @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.reset', side_effect=reset)
    def test_driver_increases_orders(self, mock_reset, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)

        request.user = self.user
        o1 = Order.objects.get(delivery_instructions="drop check")
        driver = User.objects.get(username=o1.driver).profile.email
        mock_reset(request)
        d1 = Profile.objects.get(email=driver)
        self.assertEquals(d1.deliveries_made, 1)

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_not_shopping(self, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        u1 = User.objects.get(email="c1@email.com")
        self.assertFalse(u1.profile.is_shopping)

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_not_matched(self, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        # u1 = User.objects.get(email="c1@email.com")
        o = Order.objects.filter(user="c1@gmail.com")
        self.assertEquals(len(o), 0)

    @mock.patch('shop.views.match', side_effect=match)
    def test_match_not_driver(self, mock_match):
        request = self.factory.get('/dashboard')
        mock_match(request)
        # u1 = User.objects.get(email="c1@email.com")
        o = Order.objects.filter(driver="c1@gmail.com")
        self.assertEquals(len(o), 0)


class SwapTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="driver3", password='12345', email='d3@email.com')
        d1 = User.objects.get(username="driver3")
        # d1.profile.is_matching = True
        d1.profile.started_matching = timezone.now() + timezone.timedelta(days=-2)
        d1.profile.email = d1.email
        d1.profile.driver_filled = True
        d1.save()

        Order.objects.create(user='c3@email.com', driver='None', order_placed = timezone.now() + timezone.timedelta(days=-1), delivery_instructions="swap check", store_selection="WAL", order_cost=45, has_paid=True)

        User.objects.create_user(username="customer3", password='12345', email='c3@email.com')
        u3 = User.objects.get(username="customer3")
        u3.profile.is_shopping = True
        u3.profile.email = u3.email
        u3.save()

        self.client = Client()
        self.user = User.objects.get(username="driver3")
        self.factory = RequestFactory()

    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_default_not_matched(self, mock_swap):
        request = self.factory
        request.user = self.user
        self.assertFalse(request.user.profile.is_matching)

    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_set_matching(self, mock_swap):
        request = self.factory
        request.user = self.user
        mock_swap(request)
        self.assertTrue(request.user.profile.is_matching)

    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_set_not_matching(self, mock_swap):
        request = self.factory
        request.user = self.user
        mock_swap(request)
        mock_swap(request)
        self.assertFalse(request.user.profile.is_matching)

    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_set_swap_and_match(self, mock_swap):
        request = self.factory.get('/driver_dash')
        o1 = Order.objects.get(delivery_instructions="swap check")
        o1.driver = ""
        o1.save()
        request.user = self.user
        mock_swap(request)
        self.assertFalse(User.objects.get(email="d3@email.com").profile.is_matching)

    # @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_set_swap_and_call_match(self, mock_swap):
        request = self.factory
        request.user = self.user
        o1 = Order.objects.get(delivery_instructions="swap check")
        o1.driver = ""
        o1.save()
        mock_swap(request)
        # mock_swap(request)
        self.assertFalse(User.objects.get(email="d3@email.com").profile.is_matching)

    # @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_set_swap_and_get_order(self, mock_swap):
        request = self.factory
        request.user = self.user
        o1 = Order.objects.get(delivery_instructions="swap check")
        o1.driver = ""
        o1.save()
        mock_swap(request)
        # mock_swap(request)
        self.assertTrue(User.objects.get(email="d3@email.com").profile.has_order)

    # @mock.patch('shop.views.match', side_effect=match)
    @mock.patch('shop.views.swap', side_effect=swap)
    def test_match_set_swap_and_check_unchanged(self, mock_swap):
        request = self.factory
        request.user = self.user
        o1 = Order.objects.get(delivery_instructions="swap check")
        o1.driver = ""
        o1.save()
        mock_swap(request)
        mock_swap(request)
        self.assertFalse(User.objects.get(email="d3@email.com").profile.is_matching)
