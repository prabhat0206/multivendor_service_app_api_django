from django.urls import path
from .views import *

urlpatterns = [
    path('categories', CategoryAPI.as_view(), name='categories'),
    path('sub_categories', SubCategoryAPI.as_view(), name='sub_Categories'),
    path('services', ServiceAPI.as_view(), name='services'),
    path('cart', CartAPI.as_view(), name='cart'),
    path('address', AddressAPI.as_view(), name='address'),
    path('category/<int:category>', ServiceByCategory.as_view(), name='category_wise_service'),
    path('category_sub/<int:category>', SubCategoryByCategory.as_view(), name='category_wise_sub'),
    path('subcategory/<int:sub_category>', ServiceBySubCategory.as_view(), name='sub_category_wise_service')
]
