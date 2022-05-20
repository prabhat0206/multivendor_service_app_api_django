import json
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import View
from adminn.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from adminn.serializer import *
from client.models import Address
from django.conf import settings
from .serializer import *


class CategoryAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryAPI(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ServiceAPI(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceWithMoreDetails


class CartAPI(generics.ListCreateAPIView):

    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated]   

    def get(self, request):
        cart_products = request.user.service_set.all()
        return Response({"success": True, "cart_products": ServiceSerializer(cart_products, many=True).data})

    def post(self, request):
        service = self.get_queryset().get(sid=request.GET.get('sid'))
        if service:
            if service in request.user.service_set.all():
                return Response({"success": False, "error": "product already exists in your cart"})
            request.user.service_set.add(service)
            return Response({"success": True})
        return Response({"success": False, "error": "Something went wrong"})

    def delete(self, request):
        service = self.get_queryset().get(sid=request.GET.get('sid'))
        if service:
            if service in request.user.service_set.all():
                request.user.service_set.remove(service)
                return Response({"success": True})
            else:
                return Response({"success": False, "error": "product not in your card"})
        return Response({"success": False, "error": "Something went wrong"})


class ServiceByCategory(ServiceAPI):

    def get_queryset(self, *args, **kwargs):
        return super(ServiceByCategory, self).get_queryset(*args, **kwargs).filter(category=self.kwargs['category'])


class SubCategoryByCategory(SubCategoryAPI):

    def get_queryset(self, *args, **kwargs):
        return super(SubCategoryByCategory, self).get_queryset(*args, **kwargs).filter(category=self.kwargs.get('category'))


class ServiceBySubCategory(ServiceAPI):

    def get_queryset(self, *args, **kwargs):
        return super(ServiceBySubCategory, self).get_queryset(*args, **kwargs).filter(sub_category=self.kwargs.get('sub_category'))


class AddressAPI(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serialized = self.serializer_class(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"success": True, "address": serialized.data})
        return Response({"success": False, "error": serialized.errors})

class AddressUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


class TreandingServices(generics.ListAPIView):
    queryset = Service.objects.all().order_by('-sid').filter(is_trending=True)
    serializer_class = ServiceWithMoreDetails
    pagination_class = None


class OrderAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWithMidOrder
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = self.get_queryset().filter(user=request.user).order_by('-oid')
        serialized = self.serializer_class(orders, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = request.user.id
        address = Address.objects.get(id=data['address'])
        if address:
            data['address'] = f'{address.name}, {address.address_1}, {address.address_2}, {address.city}, {address.state}, {address.pin_code}, {address.telephone}'
        if data['payment_method'] != 'cod':
            if not (settings.CLIENT.utility.verify_payment_signature(data)):
                return Response({"success": False, "error": "payment id not valid"})
        
        if 'wallet_balance_use' in data:
            if user.wallet_balance - int(data['wallet_balance_use']) < 0:
                return Response({"success": False, "error": "Your wallet balance is not enough"})
            user.wallet_balance =- int(data['wallet_balance_use'])
            user.save()
        
        order = OrderSerializer(data=data)
        if order.is_valid():
            order.save()
            services_id = [services['sid'] for services in data['services']]
            services = Service.objects.filter(sid__in=services_id)
            total_amount = 0
            for service in services:
                for ser in data['services']:
                    if ser['sid'] == service.sid:
                        service_data = {
                            "sid": service.sid,
                            "service_name": service.name,
                            "service_description": service.description,
                            "service_cost": service.service_price,
                            "image": service.image,
                            "order": order.data['oid'],
                            "service": service.sid,
                            "start_time": ser['start_time'],
                            "end_time": ser['end_time'],
                            "service_date": ser['service_date'],
                            "instruction": ser['instruction']
                        }
                        mid_order = MidOrderSerializer(data=service_data)
                        if mid_order.is_valid():
                            mid_order.save()
                        else:
                            print(mid_order.errors)
                        total_amount += service.service_price
            model_data = Order.objects.get(oid=order.data['oid'])
            model_data.total_amount  = total_amount - (total_amount * data['discount'] / 100)
            cart_products = request.user.service_set.all()
            model_data.save()
            for service in cart_products:
                request.user.remove(service)
            return Response({"success": True, "data": self.serializer_class(model_data).data})
        return Response({"success": False, "error": order.errors})


class OrderRetriveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWithMidOrder
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order = self.queryset.get(oid=self.kwargs.get('pk'))
        if order.user == self.request.user:
            return order
        return None


class TimeSlotAPI(View):
    queryset = MidOrder.objects.all()
    serializer_class = TimeSlotSerializer

    def get(self, request, sid, query_date):
        query = self.queryset.filter(service_date=query_date, service=sid)
        return JsonResponse({"success": True, "data": self.serializer_class(query, many=True).data}, safe=False)


class BannerAPI(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = None
    def get_queryset(self, *args, **kwargs):
        return super(BannerAPI, self).get_queryset(*args, **kwargs).filter(name=self.kwargs.get('name'))


class OrderID(View):
    def get(self, request):
        order = settings.CLIENT.order.create({
            "amount": float(request.GET.get("amount")) * 100,
            "currency": "INR",
            "receipt": "#1receipt",
            "notes": {
                "note1": "payment"
            }
        })
        return JsonResponse({'success': True, "order_id": order['id']}, safe=False)


class ServiceViewApi(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceViewSerializer


class ApplyCarrier(generics.CreateAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    permission_classes = [AllowAny]


class CouponsViewApi(generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
