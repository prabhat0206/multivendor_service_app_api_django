from django.urls import path
from .views import *

urlpatterns = [
    path('category', CategoryADMIN.as_view(), name='add_category'),
    path('category/<int:pk>', CategoryADMIN.as_view(), name='category_update'),
    path('sub_category', SubCategoryADMIN.as_view(), name='add_subcategory'),
    path('sub_category/<int:pk>', SubCategoryADMIN.as_view(), name='sub_category_update'),
    path('service', ServiceADMIN.as_view(), name='add_service'),
    path('service/<int:pk>', ServiceADMIN.as_view(), name='service_update')
]
