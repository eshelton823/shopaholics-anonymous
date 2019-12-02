from django.shortcuts import render
from django.shortcuts import redirect, reverse
from users.models import Order, Profile, get_default_cart, User
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .scrape import getItems
import json, ast
import decimal
import random
import string
from chat.models import Room
# Create your views here.

DRIVER_MARGIN = 10.00
TAX = .06

def home(request):
    if(request.user.is_authenticated):
        return redirect('shop:dashboard')
    return render(request, 'shop/home.html')

def order_to_list(o):
    context = {}
    ol = json.loads(o.order_list)

    try:
        print(ol["items"])
    except:
        ol = ast.literal_eval(ol)
        print(ol["items"])
    context['current_order'] = []
    for i in range(len(ol['items'])):
        context['current_order'].append({'title':ol['items'][i]['title'], 'image':ol['items'][i]['image'], 'id':ol['items'][i]['id'], 'price':ol['items'][i]['price']})
    return context['current_order']

def dashboard(request):
    # print(request.user)
    if request.user.username != "":
        if request.user.profile.email == "":
            request.user.profile.email = request.user.email
            request.user.profile.save()
        context = get_order_info(request.user)
        context['past_orders'] = list(Order.objects.filter(past_user__contains=request.user.username))
        print(context['past_orders'])
        return render(request, 'shop/dashboard.html', context)
    else:
        return redirect('/profile/signin')

def driver_dash(request):
    if request.user.username == "":
        return redirect('/profile/signin')
    if request.user.profile.driver_filled:
        context = get_driver_info(request.user)
        #context = get_order_info(request.user)
        context['past_deliveries'] = list(Order.objects.filter(past_driver__contains=request.user.username))
        return render(request, 'shop/driver_dash.html', context)
    else:
        return redirect('/profile/driver_info')

def store(request):
    if request.user.is_authenticated:
        context = {}
        if(request.method == "POST"):
            if(request.POST.get('delete', '')):
                item = request.POST.get('delete', '')
                request.user.profile.cart["items"].remove(ast.literal_eval(item))
            elif (request.POST.get('item', '')):
                item = request.POST.get('item', '')
                res = ast.literal_eval(item)
                try:
                    request.user.profile.cart["items"]
                except:
                    request.user.profile.cart = {"items":{}}
                    print("Made new.")
                request.user.profile.cart['items'].append(res)
                print("Request:", request.user.profile.cart['items'])
            request.user.save()
        query = request.GET.get('search')
        subtotal = 0.0
        for item in request.user.profile.cart['items']:
            subtotal += (float(item['price'][1:]))
        tax = (subtotal+DRIVER_MARGIN)*(TAX)
        total = (subtotal+DRIVER_MARGIN)*(1+TAX)
        context['tax_string'] = '${:,.2f}'.format(tax)
        context['subtotal_string'] = ('${:,.2f}'.format(subtotal))
        context['driver_margin_string'] = ('${:,.2f}'.format(DRIVER_MARGIN))
        context["total_string"] = ('${:,.2f}'.format(total))
        context['stripe_price'] = total*100
        if query is not None:
            context['items'] = getItems(query)
        if request.user.profile.is_shopping:
            context['disabled'] = True
        else:
            context['disabled'] = False
        if request.session.get('empty') is not None:
            context['empty'] = "Your cart is empty. Please add items before checking out."
            request.session['empty'] = None
        else:
            context['empty'] = False
        return render(request, 'shop/store.html', context)
    else:
        return redirect('profile/signin')

def process_order(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # try:
            o = Order()
            o.delivery_address = request.POST['del_add']
            o.order_list = json.dumps(request.user.profile.cart)
            print(o.order_list)
            # print("HERE" + str(len(o.order_list)))
            if len(o.order_list) == 13:
                request.session['empty'] = True
                return HttpResponseRedirect(reverse('shop:store'))
            request.user.profile.cart = get_default_cart()
            try:
                o.delivery_apt_suite = request.POST['appt_suite']
            finally:
                o.delivery_instructions = request.POST['del_instr']
                o.store_selection = 'WAL'
                o.user = request.user.username
                o.customer_name = request.user.first_name
                o.has_paid = False
                o.order_cost = round(float(request.POST['price'])/100, 2)
                try:
                    asap = request.POST['asap']
                    o.is_delivery_asap = True
                    o.desired_delivery_time_range_lower_bound = timezone.now()
                    o.desired_delivery_time_range_upper_bound = timezone.now()
                except:
                    o.desired_delivery_time_range_lower_bound = timezone.now() + timezone.timedelta(days=int(request.POST['d_time'][0]))
                    o.desired_delivery_time_range_upper_bound = timezone.now() + timezone.timedelta(days=int(request.POST['d_time'][2]))
                finally:
                    o.save()
                    request.user.profile.is_shopping = True
                    request.user.save()
                return HttpResponseRedirect(reverse('shop:checkout'))
        # except:
        #     return HttpResponseRedirect(reverse('shop:failure'))

def success(request):
    return render(request, 'shop/success.html')

def failure(request):
    return render(request, 'shop/failure.html')

def checkout(request):
    context = {}
    o = Order.objects.get(user=request.user.username)
    context['stripe_price'] = o.order_cost*100
    context['list'] = order_to_list(o)
    context['price'] = '${:,.2f}'.format(o.order_cost)
    context['key'] = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'shop/checkout.html', context)

def search(request):
    if not request.user.is_authenticated:
        return redirect('/profile/signin')
    query = request.GET.get('search')
    if query is None:
        return render(request, 'shop/search.html')
    else:
        context = {}
        context['items'] = getItems(query)
        return render(request, 'shop/search.html', context)

def pay(request):
    o = Order.objects.get(user=request.user.username)
    o.has_paid = True
    o.save()
    return HttpResponseRedirect(reverse('shop:success'))


def get_order_info(user):
    context = {}
    # print(user.profile.is_shopping)
    if not user.profile.is_shopping:
        context['status'] = "Not Shopping"
        context['current_order'] = "You aren't shopping right now!"
        # context['price'] = "$0.00"
        context['driver'] = "N/A"
        context['drop'] = "N/A"
        context['disabled'] = "Not Currently Shopping"
        context['paid'] = "N/A"
    else:
        context['status'] = "Shopping"
        o = Order.objects.filter(user=user.username)[0]
        context['current_order'] = order_to_list(o)
        # print(user.email)
        # context['price'] =
        if o.has_paid:
            context['paid'] = "You have paid for your order!"
        else:
            context['paid'] = "Unpaid. Pay now to start matching!"
        if o.driver != "":
            context['driver'] = o.driver
            context['disabled'] = "Resolve Order"
        else:
            if o.has_paid:
                context["driver"] = "Unmatched"
            else:
                context["driver"] = "Pay for your order to start matching"
            context['disabled'] = "Drop Order"
        context['drop'] = o.desired_delivery_time_range_upper_bound
        context['chat_room'] = o.chat_room

    if user.profile.has_order or user.profile.is_matching:
        context["identity"] = "Driver"
    else:
        context["identity"] = "Shopper"
    if user.profile.is_shopping:
        o = Order.objects.filter(user=user.username)[0]
        context['chat_room'] = o.chat_room
        # print(o)
        context['current'] = o.customer_name
        if o.is_delivery_asap:
            context['late_time'] = "ASAP"
        else:
            context['late_time'] = o.desired_delivery_time_range_upper_bound
        context['address'] = o.delivery_address
        if o.delivery_apt_suite != "":
            context['apt'] = o.delivery_apt_suite
        else:
            context['apt'] = "Not specified"
        context['instructions'] = o.delivery_instructions
        context['cost'] = '${:,.2f}'.format(o.order_cost)
        context['list'] = o.order_list
        # print(o.customer_name)
    else:
        context['current'] = "None"
        context['late_time'] = "N/A"
        context['cost'] = "N/A"
        context['list'] = "N/A"
        context['address'] = "N/A"
        context['apt'] = "N/A"
        context['instructions'] = "N/A"
    return context

def get_driver_info(d):
    context = {}
    if d.profile.has_order:
        o = Order.objects.filter(driver=d.username)[0]
        # print(o)
        context['current'] = o.customer_name
        context['status'] = "You have an order!"
        if o.is_delivery_asap:
            context['late_time'] = "ASAP"
        else:
            context['late_time'] = o.desired_delivery_time_range_upper_bound
        context['address'] = o.delivery_address
        if o.delivery_apt_suite != "":
            context['apt'] = o.delivery_apt_suite
        else:
            context['apt'] = "Not specified"
        context['instructions'] = o.delivery_instructions
        context['cost'] = '${:,.2f}'.format(o.order_cost)
        context['list'] = order_to_list(o)
        context['chat_room'] = o.chat_room
        context['current_order'] = order_to_list(o)
        # print(o.customer_name)
    else:
        context['current'] = "None"
        context['late_time'] = "N/A"
        context['cost'] = "N/A"
        context['list'] = "N/A"
        context['address'] = "N/A"
        context['apt'] = "N/A"
        context['instructions'] = "N/A"
        context['status'] = "Not matching"
    if d.profile.is_matching:
        context['status'] = "Waiting for a match"
        context['matching'] = "Stop matching"
        # context['disable'] = ""
    elif not d.profile.is_matching and d.profile.has_order:
        context['matching'] = "Order in progress: Cannot change status"

        # context['disable'] = "disabled"
    else:
        context['matching'] = "Start matching"
        # context['disable'] = ""
    context['money'] = "$" + str(d.profile.money_earned)
    context['deliveries'] = d.profile.deliveries_made
    context['plate'] = d.profile.license_plate_number
    context['make'] = d.profile.car_make
    context['model'] = d.profile.car_model
    context['state'] = d.profile.state_of_drivers_license_issuance
    context['license'] = d.profile.license_identifier_number
    return context

def swap(request):
    if request.user.profile.is_matching:
        request.user.profile.is_matching = False
        request.user.profile.started_matching = None
        request.user.profile.save()
    elif not request.user.profile.is_matching and not request.user.profile.has_order:
        request.user.profile.is_matching = True
        request.user.profile.started_matching = timezone.now()
        request.user.profile.save()
        match(request)
    return HttpResponseRedirect(reverse('shop:driver_dash'))


def reset(request):
    if not request.user.profile.is_shopping:
        return HttpResponseRedirect(reverse('shop:dashboard'))
    o = Order.objects.filter(user=request.user.username)[0]
    price = o.order_cost
    if o.driver != "":
        if o.driver == request.user.username:
            request.user.profile.has_order = False
            request.user.profile.money_earned += price
            request.user.save()
        else:
            d = User.objects.filter(username=o.driver)[0].profile
            d.has_order = False
            d.money_earned += price
            d.save()
        o.past_user = o.user
        o.past_driver = o.driver
        o.user = "COMPLETE"
        o.customer_name = "COMPLETE"
        o.driver = "COMPLETE"
        o.is_completed = True
        o.save()
    else:
        o.user = "DROPPED"
        o.customer_name = "DROPPED"
        o.driver = "DROPPED"
        o.past_user = request.user.username
        o.past_driver = None
        o.save()
    request.user.profile.is_shopping = False
    request.user.save()
    return HttpResponseRedirect(reverse('shop:dashboard'))

def match(request):
    # print("matching!")
    # NOTE: Currently a person could be matched to their own order!! Decide as a team if that's OK or not
    drivers = Profile.objects.filter(is_matching=True).order_by('started_matching')
    orders = Order.objects.filter(driver="", has_paid=True).order_by('id')
    queuedrivers = []
    queueorders = []
    for driver in drivers:
        # print("DRIVER")
        # print(driver.email)
        queuedrivers.append(driver)
    for order in orders:
        # print("ORDER")
        # print(order.delivery_instructions)
        queueorders.append(order)
    while (len(queuedrivers) > 0) and (len(queueorders) > 0):
        d = queuedrivers.pop(0)
        o = queueorders.pop(0)
        d.has_order = True
        d.is_matching = False
        d.started_matching = None
        d.deliveries_made += 1
        d.save()
        o.order_start_time = timezone.now()
        o.driver = d.user.username
        slug = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        Room.objects.create(name='Shopper Chat', slug=slug, description="Chat about your order")
        o.chat_room = slug
        o.save()
    # print(request.path_info)
    return HttpResponseRedirect(reverse('shop:dashboard'))

def view_order(request, order_id):
    o = Order.objects.filter(id=order_id)
    context = {}
    if(len(o) != 0):
        o = o[0]
    else:
        return HttpResponseRedirect(reverse('shop:home'))
    # print(o.past_driver, o.past_user, request.user.username)
    if ((not request.user.is_authenticated)):
        return HttpResponseRedirect(reverse('shop:home'))
        #Broken up for clarity
    elif (o.past_driver != request.user.username and o.past_user != request.user.username):
        return HttpResponseRedirect(reverse('shop:home'))
    print(o.special_requests)
    context['current_order'] = order_to_list(o)
    context['order'] = o
    return render(request, 'shop/view_order.html', context)
