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
    class Meta:
        model = MidOrder
        fields = '__all__'


class MidOrderSerializerWithService(MidOrderSerializer):
    service = ServiceSerializer()
    service_name = SerializerMethodField()
    service_description = SerializerMethodField()
    image = SerializerMethodField()
    sid = SerializerMethodField()

    def get_service_name(self, instance):
        return instance.service.name if instance.service else ""

    def get_service_description(self, instance):
        return instance.service.description if instance.service else ""

    def get_image(self, instance):
        return instance.service.image.url if instance.service else ""

    def get_sid(self, instance):
        return instance.service.sid if instance.service else 0


class OrderWithMidOrder(OrderSerializer):
    midorder_set = MidOrderSerializerWithService(many=True)
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
