from rest_framework import generics
from rest_framework.views import View
from account.models import User
from account.serializer import UserSerializer
from client.models import Carrier, Order, MidOrder
from client.serializer import MidOrderSerializer, OrderSerializer, OrderWithMidOrder, CarrierSerializer
from .models import Category, SubCategory, Offer, FAQ, Banner, Query, Coupon, Service, Review
from .serializer import *
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q


class CustomGenericView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]
    
    def delete(self, request, pk):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"success": True})


class CategoryADMIN(CustomGenericView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryADMIN(CustomGenericView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ServiceADMIN(CustomGenericView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BannerADMIN(generics.DestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response({"success": True})



class BannersADMIN(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminUser]


class OrderADMIN(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-oid')
    serializer_class = OrderWithMidOrder
    permission_classes = [IsAdminUser]


class OrderByIdADMIN(generics.RetrieveAPIView):
    queryset = Order.objects.all()
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


class AddDelivery(generics.ListCreateAPIView):
    queryset = User.objects.all().filter(delivery_boy=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UpdateDistroyDelivery(generics.RetrieveUpdateDestroyAPIView):
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
        total_amount = 0
        for order in deliverd_orders:
            total_amount += order.total_amount
        services = Service.objects.all().count()
        return Response({
            "orders": orders_count,
            "cancelled_orders": cancelled_orders,
            "completed": deliverd_orders.count(),
            "total_amount": total_amount,
            "services": services
        })


class CarrierView(generics.ListAPIView):
    queryset = Carrier.objects.all().order_by("-id")
    serializer_class = CarrierSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None


class AddCoupon(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]


class DeleteCouponView(generics.DestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response({"success": True})


class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None


class DeleteOfferView(generics.DestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAdminUser]


class SearchUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return self.queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(ph_number__icontains=query)
            )
        return self.queryset
