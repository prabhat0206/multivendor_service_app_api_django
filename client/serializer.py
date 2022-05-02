from rest_framework.serializers import ModelSerializer
from adminn.serializer import *
from client.models import Address, MidOrder, Order


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

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class MidOrderSerializer(ModelSerializer):
    class Meta:
        model = MidOrder
        fields = '__all__'


class OrderWithMidOrder(OrderSerializer):
    midorder_set = MidOrderSerializer(many=True)


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = MidOrder
        fields = ['start_time', 'end_time', 'service_date']
