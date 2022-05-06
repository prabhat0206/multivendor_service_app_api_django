from django.urls import path
from .views import *

urlpatterns = [
    path('categories', CategoryAPI.as_view(), name='categories'),
    path('sub_categories', SubCategoryAPI.as_view(), name='sub_Categories'),
    path('services', ServiceAPI.as_view(), name='services'),
    path('cart', CartAPI.as_view(), name='cart'),
    path('address', AddressAPI.as_view(), name='address'),
    path('address/<int:pk>', AddressUpdateDelete.as_view(), name='address_update_delete'),
    path('category/<int:category>', ServiceByCategory.as_view(), name='category_wise_service'),
    path('category_sub/<int:category>', SubCategoryByCategory.as_view(), name='category_wise_sub'),
    path('subcategory/<int:sub_category>', ServiceBySubCategory.as_view(), name='sub_category_wise_service'),
    path('trending', TreandingServices.as_view(), name="trending_services"),
    path('order', OrderAPI.as_view(), name='order_view_create'),
    path('order/<int:pk>', OrderRetriveUpdate.as_view(), name='order_update'),
    path('time/<int:sid>/<str:query_date>', TimeSlotAPI.as_view(), name='time'),
    path('banner/<str:name>', BannerAPI.as_view(), name='banner'),
    path('order_id', OrderID.as_view(), name='order_id'),
    path('service/<int:pk>', ServiceViewApi.as_view(), name='service_api')
]
