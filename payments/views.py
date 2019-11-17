import stripe
from django.shortcuts import redirect, reverse


from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    template_name = 'payments/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='Order Charge',
            source=request.POST['stripeToken']
        )
        return reverse('shop:pay')