"""ResturantTableBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from .views import RegistrationView,CreateReservationView,LoginView,LogoutView,ViewReservationView,UpdateReservationView,DeleteReservationView


urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'), 
    path('create-reservation/',CreateReservationView.as_view(), name='create-reservation'),
    path('update-reservation/<int:pk>/', UpdateReservationView.as_view(), name='update-reservation'),
    path('', ViewReservationView.as_view(), name='view-reservation'),
    path('delete-reservation/<int:pk>',DeleteReservationView.as_view(), name = 'delete-reservation'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout')

]

