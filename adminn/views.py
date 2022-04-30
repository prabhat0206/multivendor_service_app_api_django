from rest_framework import generics
from .models import Category, SubCategory
from .serializer import *
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
        return Response({"success": False, "error": serialized_data.error})


class CategoryADMIN(AddItemToModelWithImage):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryADMIN(AddItemToModelWithImage):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ServiceADMIN(AddItemToModelWithImage):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
