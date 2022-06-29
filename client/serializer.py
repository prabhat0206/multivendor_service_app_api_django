from dataclasses import fields
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from adminn.serializer import *
from client.models import Address, Carrier, MidOrder, Order


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
    service = ServiceSerializer()
    class Meta:
        model = MidOrder
        fields = '__all__'


class OrderWithMidOrder(OrderSerializer):
    midorder_set = MidOrderSerializer(many=True)
    buyer_name = SerializerMethodField()

    def get_buyer_name(self, instance):
        return instance.user.name


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = MidOrder
        fields = ['start_time', 'end_time', 'service_date']


class ServiceViewSerializer(ServiceWithMoreDetails):
    review_set = ReviewSerializer(many=True)
    faq_set = FAQSerializer(many=True)


class CarrierSerializer(ModelSerializer):
    class Meta:
        model = Carrier
        fields = '__all__'
