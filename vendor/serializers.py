from dataclasses import field
from rest_framework.serializers import ModelSerializer
from account.models import User
from client.models import Order
from client.serializer import MidOrderSerializer

class UserVSerializer(MidOrderSerializer):
    class Meta:
        model = User
        fields = ['name', 'ph_number']

class OrderVSerializer(ModelSerializer):
    midorder_set = MidOrderSerializer(many=True)
    user = UserVSerializer()
    class Meta:
        model = Order
        fields = ['oid', 'address', 'date_time',
                  'payment_method', 'midorder_set', 'total_amount', 'status', 'user', 'wallet_balance_use']


# class MidOrderVSerializer(MidOrderSerializer):
#     order = OrderVSerializer()

