from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.postgres.fields import JSONField



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # personal -- updated on sign-in and profile
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    # username = models.CharField(max_length=20, default="")
    USERNAME_FIELD = 'username'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']
    # is_anonymous =
    # password = models.CharField(max_length=100)
    # username = models.CharField(max_length=50, unique=True)
    # last_login = models.DateTimeField(default=timezone.now)
    # profile_pic = models.ImageField()
    # phone_number = models.PhoneNumberField(_(""))
    deliveries_made = models.IntegerField(default=0)
    money_earned = models.DecimalField(decimal_places=2, max_digits=9, default=0)

    # car information
    license_plate_number = models.CharField(max_length=10, default="0")
    car_make = models.CharField(max_length=16, default="")
    car_model = models.CharField(max_length=16, default="")

    # car personals
    license_identifier_number = models.CharField(max_length=12, default="")
    state_of_drivers_license_issuance = models.CharField(max_length=25, default="")

    # payment information - put under lock and key - high risk -- 3rd party, for our sake.
    # credit_card_number = models.IntegerField()
    # expiration_date = check format
    # security_number = models.IntegerField()

    # miscellaneous
    # order_history_list = models.ArrayField()
    # is_authenticated = models.BooleanField()
    # current_order = models.CharField(max_length = 50, default="")
    is_shopping = models.BooleanField(default=False) # THIS ONE IS IF A USER IS SHOPPING
    is_matching = models.BooleanField(default=False) # THIS ONE IS IF A DRIVER IS MATCHING
    has_order = models.BooleanField(default=False) # THIS ONE IS IF A DRIVER IS MATCHED WITH AN ORDER
    driver_filled = models.BooleanField(default=False)
    started_matching = models.TimeField(null=True, blank=True)
    cart = JSONField(default={'items':[]})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





class Order(models.Model):
    #relationship with user (many-to-many)
    user = models.CharField(max_length=20)
    driver = models.CharField(max_length=20, default='')
    ### FOR USER SIDE ###
    #delivery info - need city or state or zip? assuming local a given or can calculate in range
    delivery_address = models.CharField(max_length=50) #check if in range
    delivery_apt_suite = models.CharField(max_length=20)
    delivery_instructions = models.CharField(max_length=120)


    #user location -- to be used with mapping
    dropoff_latitude = models.DecimalField(decimal_places=5, max_digits=9, default=0.0)
    dropoff_longitude = models.DecimalField(decimal_places=5, max_digits=9, default=0.0)

    #driver location
    driver_latitude = models.DecimalField(decimal_places=5, max_digits=9, default=0.0)
    driver_longitude = models.DecimalField(decimal_places=5, max_digits=9, default=0.0)

    STORE_SELECTIONS = [
        ('KRO', 'Kroger'),
        ('WAL', 'Wal-Mart'),
    ]

    #order information
    store_selection = models.CharField(max_length=15, choices=STORE_SELECTIONS, default=None)
    order_size = models.CharField(max_length=15, default="small") #small, med, large; calculate based on total price before delivery charge
    # TODO
    order_cost = models.DecimalField(decimal_places=5, max_digits=9, default=0.0)
    order_list = models.CharField(max_length=1000, default="cheese")
    # order_list = models.CharField(max_length=255, default=None) #will be list of objs later...
    desired_delivery_time_range_lower_bound = models.TimeField(null=True, blank=True)
    desired_delivery_time_range_upper_bound = models.TimeField(null=True, blank=True)
    is_delivery_asap = models.BooleanField(default=False)

    #delivery - order
    order_placed = models.TimeField(default=timezone.now)
    order_start_time = models.TimeField(null=True, blank=True)#when they accept the order
    order_deliver_time = models.TimeField(null=True, blank=True)
    current_store_to_go_to = models.CharField(max_length=20, default="")
    special_requests = models.CharField(max_length=150, default="")

    #delivery - order status
    is_on_the_way_to_the_store = models.BooleanField(default=True) #first time driver accepts and this shows they will be on the way
    is_at_the_store = models.BooleanField(default=False)
    is_on_the_way_from_the_store = models.BooleanField(default=False) #make function that will turn True when driver gets back in car to go to customer

    #delivery - customer
    current_address_dropoff_street_and_street_number = models.CharField(max_length=35, default="")
    customer_name = models.CharField(max_length=20, default="")
