from django.db import models
from account.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    state = models.CharField(max_length=255)
    pin_code = models.IntegerField()
