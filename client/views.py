from rest_framework import generics
from adminn.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from adminn.serializer import *
from client.models import Address
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
        return super(ServiceByCategory, self).get_queryset(*args, **kwargs).filter(category=self.category)


class SubCategoryByCategory(SubCategoryAPI):

    def get_queryset(self, *args, **kwargs):
        return super(SubCategoryByCategory, self).get_queryset(*args, **kwargs).filter(category=self.category)


class ServiceBySubCategory(ServiceAPI):

    def get_queryset(self, *args, **kwargs):
        return super(ServiceBySubCategory, self).get_queryset(*args, **kwargs).filter(sub_category=self.sub_category)


class TimeSlotAPI(generics.ListAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    def get_queryset(self, *args, **kwargs):
        return super(TimeSlotAPI, self).get_queryset(*args, **kwargs).filter()


class AddressAPI(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

