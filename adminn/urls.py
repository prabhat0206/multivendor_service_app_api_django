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
    path('banners', BannersADMIN.as_view(), name='banners'),
    path('banner/<int:pk>', BannerADMIN.as_view(), name='banner_update'),
    path('orders', OrderADMIN.as_view(), name='orders'),
    path('all_users', UserADMIN.as_view(), name='all_users'),
    path('update_user/<int:pk>', UserUpdateADMIN.as_view(), name='update_user'),
    path('review', ReviewAdmin.as_view(), name='review_Add'),
    path('review/<int:pk>', ReviewAdmin.as_view(), name='review_Update'),
    path('faq', FAQAdmin.as_view(), name='faq_add'),
    path('faq/<int:pk>', FAQAdmin.as_view(), name='faq_update'),
    path('vendor', AddVendor.as_view(), name='add_vendor'),
    path('update_vendor', UpdateDistroyVendor.as_view(), name='update_vendor'),
    path('assign_order/<int:pk>', AssignDeliveryBoy.as_view(), name='assign_order'),
    path('status', StatsView.as_view(), name='status'),
]
