from django.db import models

class User(models.Model):
    #personal
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length = 50)
    password = models.CharField(max_length=30)

    #delivery info - need city or state or zip? assuming local a given or can calculate in range
    delivery_address = models.CharField(max_length=50) #check if in range
    delivery_apt_suite = models.CharField(max_length=20) 
    delivery_instructions = models.CharField(max_length=120)

    
    #location
    latitude = models.DecimalField(decimal_places=5, max_digits=9)
    longitude = models.DecimalField(decimal_places=5, max_digits=9)
    

    #store options
    STORE_SELECTIONS = [
        ('KRO', 'Kroger'),
        ('Wal', 'Wal-Mart'),
    ]

    #store preferences; can choose to set favorite store
    activate_favorite_store = models.BooleanField(default=False)
    favorite_store = models.CharField(max_length=15, choices=STORE_SELECTIONS, default=None,)

    #payment information
    credit_card_number = models.IntegerField()
    #expiration_date = check format
    security_number = models.IntegerField()

    #order information
    store_selection = models.CharField(max_length=15, choices=STORE_SELECTIONS, default=None)
    order_size = models.CharField(max_length=15) #small, med, large; calculate based on total price before delivery charge
    order_list = models.CharField(max_length=255)
    desired_delivery_time_range_lower_bound = models.TimeField()
    desired_delivery_time_range_upper_bound = models.TimeField()
    is_delivery_asap = models.BooleanField(default=False)




class Driver(models.Model):
    #personal
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length = 50)
    password = models.CharField(max_length=50)
    #profile_pic = models.ImageField()
    #phone_number = models.PhoneNumberField(_(""))
    deliveries_made = models.IntegerField()
    money_earned = models.DecimalField(decimal_places=2, max_digits=9)

    #car information
    license_plate_number = models.CharField(max_length=10)
    car_make = models.CharField(max_length=16)
    car_model = models.CharField(max_length=16)
    
    #car personals
    license_identifier_number = models.CharField(max_length=12)
    state_of_drivers_license_issuance = models.CharField(max_length=25)

    #payment information - put under lock and key - high risk
    credit_card_number = models.IntegerField()
    #expiration_date = check format
    security_number = models.IntegerField()

    #location
    latitude = models.DecimalField(decimal_places=5, max_digits=9)
    longitude = models.DecimalField(decimal_places=5, max_digits=9)

    #delivery - order
    order_start_time = models.TimeField()#when they accept the order
    order_deliver_time = models.TimeField()
    current_store_to_go_to = models.CharField(max_length=20)
    current_order_list = models.CharField(max_length=255)#need to find a way to store as list and make longer
    current_order_size = models.CharField(max_length=15)#small, med, large
    special_requests = models.CharField(max_length=150)

    #delivery - order status
    is_on_the_way_to_the_store = models.BooleanField(default=True) #first time driver accepts and this shows they will be on the way
    is_at_the_store = models.BooleanField(default=False)
    is_on_the_way_from_the_store = models.BooleanField(default=False) #make function that will turn True when driver gets back in car to go to customer

    #delivery - customer
    current_address_dropoff_street_and_street_number = models.CharField(max_length=35)
    customer_name = models.CharField(max_length=20)

    #miscellaneous
    #order_history_list = models.


    

    
    





