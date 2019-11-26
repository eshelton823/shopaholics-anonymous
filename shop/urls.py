from django.urls import path, include

from . import views



app_name = "shop"

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('driver_dash', views.driver_dash, name='driver_dash'),
    path('home', views.home, name='home'),
    path('store', views.store, name='store'),
    path('search', views.search, name='search'),
    path('process_order', views.process_order, name='process_order'),
    path('success', views.success, name='success'),
    path('failure', views.failure, name='failure'),
    path('shop/reset', views.reset, name='reset'),
    path('shop/match', views.match, name='match'),
    path('shop/swap', views.swap, name='swap'),
    path('shop/checkout', views.checkout, name='checkout'),
    path('shop/pay', views.pay, name="pay"),
    path('order/<int:order_id>', views.view_order, name="view_order"),
]
