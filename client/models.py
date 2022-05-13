from django.db import models
from account.models import User
from adminn.models import Service
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


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    payment_method = models.CharField(max_length=20)
    rz_payment_id = models.CharField(max_length=100, null=True, blank=True)
    rz_order_id = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.FloatField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    discount = models.IntegerField(default=0)
    redeemed_points = models.IntegerField(default=0)
    coupon_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, default="order_placed")


class MidOrder(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.IntegerField()
    service_name = models.CharField(max_length=255)
    service_cost = models.FloatField(default=0)
    service_description = models.TextField()
    service_date = models.DateField()
    image = models.ImageField(upload_to='services', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    instruction = models.TextField(blank=True, null=True)
    delivery_boy = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)