from django.contrib import admin
from .models import User, Hospital, Bed, Reservation

admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(Bed)
admin.site.register(Reservation)



# Register your models here.
