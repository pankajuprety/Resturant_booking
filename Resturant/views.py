from django.shortcuts import render,redirect
from .models import Table_Reservation,Profile
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import View
from .forms import CustomRegistrationForm
from django.contrib.auth.views import LoginView,LogoutView

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
        return reverse_lazy('home')




class Home(View):
    #template_name = 'home.html'
    def get(self, request):
        return render(request,'home.html')