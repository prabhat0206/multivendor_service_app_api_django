from django.urls import path
from .views import *

urlpatterns = [
    path('services', MyServices.as_view(), name='services_v'),
    path('orders', MyOrders.as_view(), name='orders_v'),
    path('update_status/<int:pk>', UpdateStatus.as_view(), name='update_status_v'),
    path('users', Users.as_view(), name="users_v"),
    path('queries', QueryVendor.as_view(), name='queries'),
    path('send_query_to_admin/<int:pk>', SendQueryToAdmin.as_view(), name='send_query')
]
