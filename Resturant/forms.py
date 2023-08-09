from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

#Create form below
class CustomRegistrationForm(UserCreationForm):
    #email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2','email','phone_number','address')