from django.db import models
from account.models import User

class Banner(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="top")
    image = models.ImageField(upload_to="banner")

class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category")

class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="sub_category")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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

    def save(self, *args, **kwargs):
        self.category = self.sub_category.category
        super(Service, self).save(*args, **kwargs)

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
    name = models.CharField(max_length=255)
    coupon_id = models.CharField(max_length=25, unique=True)
    description = models.TextField()
    discount = models.IntegerField(default=10)


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
