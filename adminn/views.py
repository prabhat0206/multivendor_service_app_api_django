from rest_framework import generics
from rest_framework.views import View
from account.models import User
from account.serializer import UserSerializer
from client.models import Order, MidOrder
from client.serializer import MidOrderSerializer, OrderSerializer, OrderWithMidOrder
from .models import Category, SubCategory
from .serializer import *
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class AddItemToModelWithImage(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        incoming_data = request._request.POST.dict()
        incoming_data['image'] = request._request.FILES.get('image')
        serialized_data = self.serializer_class(data=incoming_data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({"success": True, "data": serialized_data.data})
        return Response({"success": False, "error": serialized_data.errors})

    def update(self, request, pk):
        instance = self.get_object()
        print(request.data)
        data_for_change = request._request.POST.dict()
        if 'image' in request._request.FILES:
            data_for_change['image'] = request._request.FILES.get('image')
        serialized = self.serializer_class(
            instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            return Response({"success": True, "data": serialized.data})
        return Response({"success": False, "Errors": str(serialized.errors)})


class CategoryADMIN(AddItemToModelWithImage):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryADMIN(AddItemToModelWithImage):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ServiceADMIN(AddItemToModelWithImage):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BannerADMIN(AddItemToModelWithImage):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class BannersADMIN(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminUser]


class OrderADMIN(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-oid')
    serializer_class = OrderWithMidOrder
    permission_classes = [IsAdminUser]


class UserADMIN(generics.ListAPIView):
    queryset = User.objects.all().filter(staff=False, superuser=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserUpdateADMIN(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ReviewAdmin(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]

class FAQAdmin(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminUser]


class AddVendor(generics.ListCreateAPIView):
    queryset = User.objects.all().filter(staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UpdateDistroyVendor(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AssignDeliveryBoy(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderWithMidOrder

    def update(self, request, pk):
        data = self.get_object()
        data.delivery_boy = User.objects.get(id=int(request.GET.get('id')))
        data.save()
        return Response({"Success": True})


class StatsView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders_count = self.get_queryset().count()
        cancelled_orders = self.get_queryset().filter(status="cancelled").count()
        deliverd_orders = self.get_queryset().filter(status="completed")
        total_amount = deliverd_orders.annotate(total_price=Sum("total_amount"))
        print(total_amount)
        services = Service.objects.count()
        return Response({
            "orders": orders_count,
            "cancelled_orders": cancelled_orders,
            "completed": deliverd_orders.count(),
            # "total_amount": total_amount.total_price,
            "services": services
        })