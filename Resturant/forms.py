from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Table_Reservation
from django.utils import timezone


#Create form below
class CustomRegistrationForm(UserCreationForm):
    #email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2','email','phone_number','address')

class Table_ReservationForm(forms.ModelForm):
    class Meta:
        model = Table_Reservation
        fields = ('table','number_of_party','reservation_start','reservation_end','special_order')

    reservation_start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs= {'type' : 'datetime-local'}),
        input_formats = ['%Y-%m-%dT%H:%M'],

    )

    reservation_end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs= {'type' : 'datetime-local'}),
        input_formats = ['%Y-%m-%dT%H:%M'],

    )

    def clean(self):
        cleaned_data = super().clean()
        reservation_start =  self.cleaned_data.get('reservation_start')
        reservation_end =  self.cleaned_data.get('reservation_end')
        reserve_date = reservation_start.date()
        reserve_time = reservation_start.time()
        reserve_end_date = reservation_end.date()
        #reserve_end_time = reservation_end.time()


        now = timezone.now()        
        current_date = now.date()
        current_time  = now.time().replace(microsecond=0)
        reservation_start = reservation_start.replace(microsecond=0)
        if reservation_start:
            if reserve_date < current_date :
                raise forms.ValidationError("Reservation can't be made in past date")
            if reserve_date == current_date:
                if reserve_time < current_time:
                    raise forms.ValidationError("Resevation cannot be made in past time")
            if reservation_start.weekday() == 5:
                raise forms.ValidationError("Reservations cannot be done on saturday")
            if reservation_start.hour >= 23 or reservation_start.hour < 8:
                raise forms.ValidationError("Reservation is closed from 23hr to 8hr in morning")
            
        if reservation_end:
            if reserve_end_date < reserve_date:
                raise forms.ValidationError("Check Reservation end date")
            if reservation_end.weekday() == 5:
                raise forms.ValidationError("Resturant is closed on Saturday, Check checkout date")
            if reservation_start.hour >= 23 or reservation_start.hour <= 8:
                raise forms.ValidationError("Reservation is closed from 23hr to 8hr in morning")


        return cleaned_data











    # def clean_reservation_start(self):
    #     reservation_start =  self.cleaned_data.get('reservation_start')
    #     if reservation_start:
    #         now = timezone.now()
    #         if reservation_start <= now:
    #             raise forms.ValidationError("Reservation start must be in the future")
    #         if reservation_start.weekday() == 5:
    #             raise forms.ValidationError("Reservations cannot be done on saturday")
    #         if reservation_start.hour > 23 and reservation_start < 8:
    #             raise forms.ValidationError("Reservation is closed during 23hr to 8hr in morning")
    #     return reservation_start
    # def clean_reservation_end(self):    
    #     reservation_end = self.cleaned_data.get('reservation_end')
    #    # reservation_start = self.cleaned_data.get('reservation_start')
    #     if reservation_end:
    #         now = timezone.now()
    #         if reservation_end <= now :
    #             raise forms.ValidationError("Reservation start must be in the future")
    #         if reservation_end.weekday() == 5:
    #             raise forms.ValidationError("Reservations cannot be done on saturday")
    #         if reservation_end.hour > 23 and reservation_end.hour < 8:
    #             raise forms.ValidationError("Reservation is closed during 23hr to 8hr in morning")
    #     return reservation_end
        

