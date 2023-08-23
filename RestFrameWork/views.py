from django.shortcuts import render, redirect
from django.urls import reverse
from Resturant.models import Table_Reservation,Table
from RestFrameWork.serializers import Table_Reservation_Serializer,TableSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q


class ViewReservationView(APIView):    
    def get(self, request):
        reservation = Table_Reservation.objects.all()
        serializer = Table_Reservation_Serializer(reservation, many = True)
        return Response(serializer.data, status = 200)


class CreateAPIReservationView(APIView):
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    #template_name = "api/createReservationApi.html"


    def get(self,request):
        user_id = request.user.id
        reservation = Table_Reservation.objects.filter(user = user_id)
        serializer = Table_Reservation_Serializer(reservation, many = True)
        #print(request.user)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        data = request.data
        data['user'] = request.user.id

        serializer = Table_Reservation_Serializer(data=data)  # Pass request.data to the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateReservationView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request,pk, *args, **kwargs):
        reservation_id = pk
        #print("primarykey: ",reservation_id)
        user_id = request.user.id
        # print("UserId: ", user_id)
        model = Table_Reservation.objects.filter(Q(user = user_id) & Q(id = reservation_id))
        if model:
            serializer = Table_Reservation_Serializer(model, many = True)
            return Response(serializer.data, status = 200)
        
        else:
            return Response("Data Not Found", status =404)
        
    def put(self,request,pk, *args,**kwargs):
        try:
            table_reservation= Table_Reservation.objects.get(pk=pk)
        except Table_Reservation.DoesNotExist:
            return Response("Reservation not found", status= 404)
                    
        serializer = Table_Reservation_Serializer(instance = table_reservation, data=request.data, context = {"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = 200)        
        else:
            return Response(serializer.errors,status= 400)










