from django.shortcuts import render
from django.shortcuts import redirect, reverse
from users.models import Order
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import OrderForm
# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def dashboard(request):
    # print(request.user)
    if request.user.username != "":
        context = get_order_info(request.user)
        return render(request, 'shop/dashboard.html', context)
    else:
        return redirect('/profile/signin')

def driver_dash(request):
    if request.user.profile.driver_filled:
        return render(request, 'shop/driver_dash.html')
    else:
        return redirect('/profile/driver_info')

def store(request):
    if request.user.is_authenticated:
        return render(request, 'shop/store.html')
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

                try:
                    asap = request.POST['asap']
                    o.is_delivery_asap = True
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
    print(user.profile.is_shopping)
    if not user.profile.is_shopping:
        context['status'] = "Not Shopping"
        context['current_order'] = "You aren't shopping right now!"
        context['price'] = "$0.00"
        context['driver'] = "N/A"
        context['drop'] = "N/A"
    else:
        context['status'] = "Shopping"
        o = Order.objects.filter(user=user.email)[0]
        context['current_order'] = o.order_list
        print(user.email)
        context['price'] = o.order_cost
        if not o.driver == "":
            context['driver'] = o.driver
        else:
            context["driver"] = "Unmatched"
        context['drop'] = o.order_deliver_time
    if user.profile.has_order or user.profile.is_matching:
        context["identity"] = "Driver"
    else:
        context["identity"] = "Shopper"
    return context

def reset(request):
    request.user.profile.is_shopping = False
    request.user.profile.save()
    return HttpResponseRedirect(reverse('shop:dashboard'))

def match(request):
    
    return HttpResponseRedirect(reverse('shop:dashboard'))