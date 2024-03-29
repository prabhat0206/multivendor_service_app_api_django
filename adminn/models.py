from typing import Any
from django.db import models
from account.models import User


class CustomManaget(models.Manager):
    
    def all(self):
        return super().all().exclude(is_deleted=True)
    
    def filter(self, *args: Any, **kwargs: Any):
        return super().filter(*args, **kwargs).exclude(is_deleted=True)
    
    def get(self, *args: Any, **kwargs: Any):
        return super().exclude(is_deleted=True).get(*args, **kwargs)


class Banner(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="top")
    image = models.ImageField(upload_to="banner")

    def __str__(self) -> str:
        return str(self.name) if self.name else "No Banner"

class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category")
    is_deleted = models.BooleanField(default=False)

    objects = CustomManaget()

    def __str__(self) -> str:
        return str(self.name) if self.name else "No Category"

class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="sub_category")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    objects = CustomManaget()

    def __str__(self) -> str:
        return str(self.name) if self.name else "No Sub Category"

class Service(models.Model):
    sid = models.AutoField(primary_key=True)
    user = models.ManyToManyField(User, blank=True)
    image = models.ImageField(upload_to="services", null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField()
    provider = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='providing')
    service_price = models.FloatField(default=0)
    actual_price = models.FloatField(default=0)
    is_trending = models.BooleanField(default=False)
    min_time_range = models.IntegerField(default=1)
    max_time_range = models.IntegerField(default=2)
    min_strength = models.IntegerField(default=1)
    max_strength = models.IntegerField(default=2)
    is_deleted = models.BooleanField(default=False)

    objects = CustomManaget()

    def save(self, *args, **kwargs):
        self.category = self.sub_category.category
        super(Service, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name) if self.name else "No Service"

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    message = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000)
    answer = models.TextField()
    other = models.CharField(max_length=10, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)

class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()


class Query(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_at_admin = models.BooleanField(default=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    coupon_id = models.CharField(max_length=100)
    is_percentage = models.BooleanField(default=False)
    value = models.PositiveIntegerField(default=1)
    valid_till = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

