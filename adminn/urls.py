from django.urls import path
from .views import *

urlpatterns = [
    path('category', CategoryADMIN.as_view(), name='add_category'),
    path('category/<int:pk>', CategoryADMIN.as_view(), name='category_update'),
    path('sub_category', SubCategoryADMIN.as_view(), name='add_subcategory'),
    path('sub_category/<int:pk>', SubCategoryADMIN.as_view(), name='sub_category_update'),
    path('service', ServiceADMIN.as_view(), name='add_service'),
    path('service/<int:pk>', ServiceADMIN.as_view(), name='service_update'),
    path('banner', BannerADMIN.as_view(), name='banner'),
    path('banner/<int:pk>', BannerADMIN.as_view(), name='banner_update'),
    path('orders', OrderADMIN.as_view(), name='orders'),
    path('all_users', UserADMIN.as_view(), name='all_users'),
    path('update_user/<int:pk>', UserUpdateADMIN.as_view(), name='update_user')
]
