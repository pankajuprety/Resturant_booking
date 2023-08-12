from django.shortcuts import render,redirect
from .models import Table_Reservation,Profile
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import View,ListView
from .forms import CustomRegistrationForm,Table_ReservationForm
from django.contrib.auth.views import LoginView,LogoutView
from datetime import datetime
from django.db.models import Q

# Create your views here.
class RegistrationView(FormView):
    template_name='registration.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        loc = form.cleaned_data['address']
        user=form.save()
        profile = Profile.objects.create(
            user = user,
            phone_number = phone_number,
            address = loc
        )
        login(self.request,user)

        return super().form_valid(form)

class LoginView(LoginView):
    template_name='login.html'
    fields="__all__"
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('create_reservation')




class CreateReservationView(LoginRequiredMixin,FormView):
    form_class = Table_ReservationForm
    template_name = 'create_reservation.html'
    context_object_name = 'table_reservation'
    success_url = reverse_lazy('view_reservation')

    def form_valid(self, forms):
        reservation = forms.save(commit=False)
        reservation.user = self.request.user
        reservation.save()
        return super().form_valid(forms)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



class ViewReservationView(ListView):
    model = Table_Reservation
    template_name = 'display_reservation.html'
    context_object_name = 'reservation'

    def get_queryset(self):
        start_date = self.request.GET.get("start_date")
        table_name = self.request.GET.get('table_name')
        username = self.request.GET.get('username')
        print(start_date,"   ",table_name,"   ", datetime.now())
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                
        if username:
            return Table_Reservation.objects.filter(Q(user__username=username) & Q(reservation_start__gt=formatted_datetime))

        elif start_date and table_name == None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            return Table_Reservation.objects.filter(reservation_start__date=start_date)
        
        elif table_name and start_date =="":
            return Table_Reservation.objects.filter(Q(table__name__icontains=table_name) & Q(reservation_start__gt=formatted_datetime))            
        
        elif table_name and start_date:
            return Table_Reservation.objects.filter(
                Q(table__name__icontains=table_name) & Q(reservation_start__date=start_date) & Q(reservation_start__gt=formatted_datetime)
                )
        else:
            return Table_Reservation.objects.filter(reservation_start__gt=formatted_datetime)
        






