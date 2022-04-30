from rest_framework.serializers import ModelSerializer
from adminn.serializer import *
from client.models import Address


class CategorySerializerWithServices(CategorySerializer):
    service_set = ServiceSerializer(many=True)


class ServiceWithMoreDetails(ServiceSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()


class SubCategoryWithServices(SubCategorySerializer):
    category = CategorySerializer()
    service_set = ServiceSerializer(many=True)


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
