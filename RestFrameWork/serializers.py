from rest_framework import serializers
from django.contrib.auth.models import User
from Resturant.models import Table_Reservation,Table
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError 
from datetime import datetime




class Table_Reservation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_Reservation
        fields = "__all__"
    

    def validate(self, data):
        # Get the instance if available (for updates)
        instance = self.instance

        # Check if the instance exists (for updates) and the user is the same as the logged-in user
        if instance and instance.user != self.context['request'].user:
            raise ValidationError("You don't have permission to update this reservation.")

        # Add other validation logic here

        # For example, validate party size against table seats

        if 'table' in data and 'number_of_party' in data:
            table = data['table']
            number_of_party = data['number_of_party']
            if table.seats < number_of_party:
                raise ValidationError("The party size is greater than seats available in reserved table.")
            
        if 'reservation_start' in data and 'reservation_end' in data:
            reservation_start = data['reservation_start'].replace(tzinfo=None)
            reservation_end = data['reservation_end'].replace(tzinfo=None)            
            currentDate = datetime.now().replace(microsecond=0)            
            if reservation_start >= reservation_end or reservation_start < currentDate:                
                raise ValidationError("Check Reservation DateTime") 
            if reservation_start.hour > 23 or reservation_start.hour < 8:
                raise ValidationError("Reservation is closed before 8 and after 23 hour") 
        

        if 'table' in data and 'reservation_start' in data and 'reservation_end' in data:
            table = data['table']
            reservation_start = data['reservation_start']
            reservation_end = data['reservation_end']
            if instance:
                reg_id =instance.id                    
                existing_reservations = Table_Reservation.objects.filter(
                    table=table,             
                    reservation_start__lt=reservation_end,
                    reservation_end__gt=reservation_start,
                ).exclude(id=reg_id)
                if existing_reservations.exists():
                    raise ValidationError("The table is already reserved for the specified date and time range.")   
            else:
                existing_reservations = Table_Reservation.objects.filter(
                table=table,             
                reservation_start__lt=reservation_end,
                reservation_end__gt=reservation_start,)
            if existing_reservations.exists():
                raise ValidationError("The table is already reserved for the specified date and time range.")  
        
        return data


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields ="__all__"


