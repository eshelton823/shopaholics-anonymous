from django.shortcuts import render
from django.shortcuts import redirect, reverse
from users.models import Order, Profile
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from .forms import OrderForm
# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def dashboard(request):
    # print(request.user)
    if request.user.username != "":
        if request.user.profile.email == "":
            request.user.profile.email = request.user.email
            request.user.profile.save()
        context = get_order_info(request.user)
        return render(request, 'shop/dashboard.html', context)
    else:
        return redirect('/profile/signin')

def driver_dash(request):
    if request.user.username == "":
        return redirect('/profile/signin')
    if request.user.profile.driver_filled:
        context = get_driver_info(request.user)
        return render(request, 'shop/driver_dash.html', context)
    else:
        return redirect('/profile/driver_info')

def store(request):
    if request.user.is_authenticated:
        context = {}
        if request.user.profile.is_shopping:
            context['disabled'] = True
        else:
            context['disabled'] = False
        return render(request, 'shop/store.html', context)
    else:
        return redirect('profile/signin')

def process_order(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        try:
            o = Order()
            o.delivery_address = request.POST['del_add']
            try:
                o.delivery_apt_suite = request.POST['appt_suite']
            finally:
                o.delivery_instructions = request.POST['del_instr']
                o.store_selection = 'WAL'
                o.user = request.user.email
                o.customer_name = request.user.first_name
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
                return HttpResponseRedirect(reverse('shop:success'))
        except:
            return HttpResponseRedirect(reverse('shop:failure'))

def success(request):
    return render(request, 'shop/success.html')

def failure(request):
    return render(request, 'shop/failure.html')


def get_order_info(user):
    context = {}
    # print(user.profile.is_shopping)
    if not user.profile.is_shopping:
        context['status'] = "Not Shopping"
        context['current_order'] = "You aren't shopping right now!"
        context['price'] = "$0.00"
        context['driver'] = "N/A"
        context['drop'] = "N/A"
        context['disabled'] = "Not Currently Shopping"
    else:
        context['status'] = "Shopping"
        o = Order.objects.filter(user=user.email)[0]
        context['current_order'] = o.order_list
        # print(user.email)
        context['price'] = o.order_cost
        if o.driver != "":
            context['driver'] = o.driver
            context['disabled'] = "Resolve Order"
        else:
            context["driver"] = "Unmatched"
            context['disabled'] = "Drop Order"
        context['drop'] = o.desired_delivery_time_range_upper_bound

    if user.profile.has_order or user.profile.is_matching:
        context["identity"] = "Driver"
    else:
        context["identity"] = "Shopper"
    if user.profile.is_shopping:
        o = Order.objects.filter(user=user.email)[0]
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
        context['cost'] = o.order_cost
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
        o = Order.objects.filter(driver=d.email)[0]
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
        context['cost'] = o.order_cost
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
    context['money'] = d.profile.money_earned
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
        match()
    return HttpResponseRedirect(reverse('shop:driver_dash'))


def reset(request):
    if not request.user.profile.is_shopping:
        return HttpResponseRedirect(reverse('shop:dashboard'))
    o = Order.objects.filter(user=request.user.email)[0]
    price = o.order_cost
    if o.driver != "":
        d = Profile.objects.filter(email=o.driver)[0]
        d.has_order = False
        d.money_earned += price
        d.save()
        o.user = "COMPLETE"
        o.customer_name = "COMPLETE"
        o.driver = "COMPLETE"
        o.save()
    else:
        o.user = "DROPPED"
        o.customer_name = "DROPPED"
        o.driver = "DROPPED"
        o.save()
    # u = Profile.objects.filter(email=request.user.email)[0]
    # print("we're here")
    # print(request.user.profile.is_shopping)
    request.user.profile.is_shopping = False
    # print(request.user.profile.is_shopping)
    request.user.save()
    return HttpResponseRedirect(reverse('shop:dashboard'))

def match():
    # print('matching!')
    # NOTE: Currently a person could be matched to their own order!! Decide as a team if that's OK or not
    drivers = Profile.objects.filter(is_matching=True).order_by('started_matching')
    # print(drivers)
    orders = Order.objects.filter(driver="").order_by('id')
    # print(orders)
    queuedrivers = []
    queueorders = []
    for driver in drivers:
        # print(driver.email, end=", ")
        queuedrivers.append(driver)
    for order in orders:
        # print(order.order_placed)
        queueorders.append(order)
    # len(queueorders)
    while (len(queuedrivers) > 0) and (len(queueorders) > 0):
        # print(len(queueorders) > 0)
        d = queuedrivers.pop(0)
        # print("EMAIL")
        # print(d.email)
        o = queueorders.pop(0)
        # print("LENGTH: "  + str(len(queueorders)))
        d.has_order = True
        d.is_matching = False
        d.started_matching = None
        d.save()
        o.order_start_time = timezone.now()
        o.driver = d.email
        o.save()
    return HttpResponseRedirect(reverse('shop:dashboard'))