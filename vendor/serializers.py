from rest_framework.serializers import ModelSerializer
from client.models import Order
from client.serializer import MidOrderSerializer


class OrderVSerializer(ModelSerializer):
    midorder_set = MidOrderSerializer(many=True)
    class Meta:
        model = Order
        fields = ['oid', 'address', 'date_time',
                  'payment_method', 'midorder_set', 'total_amount']


# class MidOrderVSerializer(MidOrderSerializer):
#     order = OrderVSerializer()

