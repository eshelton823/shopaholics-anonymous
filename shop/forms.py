from django import forms

class OrderForm(forms.Form):
    delivery_address = forms.CharField(label="delivery address", max_length=50)
    delivery_apt_suite = forms.CharField(label="apartment", max_length=20)
    delivery_instructions = forms.CharField(label="instructions", max_length=120)
    is_delivery_asap = forms.BooleanField(label = "is_asap")