from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
class User(models.Model):
    # Defining fields for the User table
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    bloodGroup = models.CharField(max_length=5)
    password = models.CharField(max_length=255, null=True)


class Hospital(models.Model):
    hospitalName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    location = models.TextField()
    area = models.TextField(null=True)
    password = models.CharField(max_length=255, null=True)

    @property
    def total_beds(self):
        return self.beds.count()
    
    @property
    def available_beds(self):
        return  self.beds.filter(status=1).count()
    
    def available_beds_by_type(self, bed_type):
        return self.beds.filter(status=1, bed_type=bed_type).count()

class Bed(models.Model):
    BED_TYPES = [
        ('ICU', 'ICU'),
        ('GEN', 'General'),
        ('PRI', 'Private'),
    ]
    STATUS_CHOICES = [
        (1, 'Available'),
        (2, 'Occupied'),
        (3, 'Maintenance'),
    ]
    hospital = models.ForeignKey(Hospital, related_name='beds', on_delete=models.CASCADE)
    bed_type = models.CharField(max_length=50, choices=BED_TYPES, default='GEN')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('discharged', 'Discharged'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)