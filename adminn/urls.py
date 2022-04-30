from django.urls import path
from .views import *

urlpatterns = [
    path('category', CategoryADMIN.as_view(), name='add_category'),
    path('sub_category', SubCategoryADMIN.as_view(), name='add_subcategory'),
    path('service', ServiceADMIN.as_view(), name='add_service'),
]
