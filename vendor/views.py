from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from adminn.models import Query, Service
from rest_framework.response import Response
from client.models import MidOrder, Order
from .serializers import *
from adminn.serializer import QuerySerializer
from rest_framework.permissions import IsAdminUser, BasePermission
from account.serializer import UserSerializer
from client.serializer import OrderSerializer, ServiceWithMoreDetails, MidOrderSerializer


class IsDeliveryUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.delivery_boy)


class MyOrders(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderVSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        return super(MyOrders, self).get_queryset(*args, **kwargs).filter(delivery_boy=self.request.user).order_by('-oid')


class MyServices(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceWithMoreDetails
    permission_classes = [IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        return super(MyServices, self).get_queryset(*args, **kwargs).filter(provider=self.request.user).order_by('-sid')


class UpdateStatus(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderVSerializer
    permission_classes = [IsDeliveryUser, IsAdminUser]

    def update(self, request, pk):
        instance = self.get_object()
        if request.user.delivery_boy:
            if request.user != instance.delivery_boy:
                return Response(401)
        status = request.GET.get('status', None)
        if not status:
            return Response(404)
        instance.status = status
        instance.save()
        return Response({"success": True})


class Users(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(delivery_boy=request.user)
        users = []
        for order in instance:
            if order.user not in users:
                users.append(order.user)
        return Response({"success": True, "data": self.serializer_class(users, many=True).data})


class QueryVendor(ListAPIView):

    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        return super(QueryVendor, self).get_queryset(*args, **kwargs).filter(service__provider=self.request.user).order_by('-oid')


class SendQueryToAdmin(UpdateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = [IsAdminUser]

    def update(self, request):
        instance = self.get_object()
        instance.is_at_admin = True
        return Response({"success": True, "data": self.serializer_class(instance).data})
