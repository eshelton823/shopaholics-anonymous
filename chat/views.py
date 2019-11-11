from django.shortcuts import render
import users
import random
import string

# Create your views here.

from users.models import Order
from .models import Room

from django.conf import settings
from django.http import JsonResponse

from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

fake = Faker()

def token(request):
    #identity = request.GET.get('identity', fake.user_name())
    identity = ""
    if(request.user.is_authenticated):
        identity = request.user.username
    else:
        #TODO: kick back to sign in.
        pass
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)

def all_rooms(request):
    slug = Order.chat_room
    rooms = Room.objects.get(slug = slug)
    return render(request, 'chat/index.html', {'rooms': rooms})


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})