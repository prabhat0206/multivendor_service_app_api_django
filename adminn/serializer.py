from rest_framework.serializers import ModelSerializer
from .models import Category, Coupon, Query, SubCategory, Service, Review, Offer, FAQ, Banner

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        exclude = ['user']

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'    

class QuerySerializer(ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'

# class TimeSlotSerializer(ModelSerializer):
#     class Meta:
#         model = TimeSlot
#         fields = '__all__'

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
