from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

def validate_less_than_99(value):
    if value >= 99 & value < 0:
        raise ValidationError(_('Value must be less than 99 or more than 0.'))

class Table(models.Model):
    seats = models.IntegerField(validators=[validate_less_than_99])
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name +" seats:"+ str(self.seats)

class Table_Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    number_of_party = models.IntegerField(validators=[validate_less_than_99])
    reservation_start = models.DateTimeField()
    reservation_end = models.DateTimeField()
    special_order = models.TextField()

    def __str__(self):
        date = self.reservation_start.date()
        start = self.reservation_start.time()
        end = self.reservation_end.time()
        return str(date)+","+str(start)+" to "+str(end)

    def clean(self):
        if self.table and self.number_of_party > self.table.seats:
            raise ValidationError(
                f"The party size ({self.number_of_party}) is greater than seats available in reserved table"
            )

        if self.table:
            existing_reservations = Table_Reservation.objects.filter(
                table=self.table,
                reservation_start__lt = self.reservation_end,
                reservation_end__gt = self.reservation_start,
                
            ) 

            if existing_reservations.exists():
                raise ValidationError(
                    "The table is already reserver for the specified date and time range"
                )

class Category(models.Model):
    type=models.CharField(max_length=255)
    
    def __str__(self):
        return self.type

class Menu(models.Model):
    item_name = models.CharField(max_length=255)
    item_price = models.FloatField()
    ingredients = models.TextField()
    images = models.FileField(upload_to="images/",blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        self.item_price = round(self.item_price,2)
        super(Menu,self).save(*args,**kwargs)




