from django.contrib import admin
from .models import Profile,Table,Table_Reservation,Menu,Category
# Register your models here.
admin.site.register(Profile)
admin.site.register(Table)
admin.site.register(Table_Reservation)
admin.site.register(Menu)
admin.site.register(Category)