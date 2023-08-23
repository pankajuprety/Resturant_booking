from django.urls import path,include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import ViewReservationView,CreateAPIReservationView,UpdateReservationView



urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',ViewReservationView.as_view(), name = 'serialView'),
    path('createApiReservation/',CreateAPIReservationView.as_view(), name = 'createView'),
    path('update/<int:pk>/',UpdateReservationView.as_view(), name = 'updateView')
]