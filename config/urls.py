from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('control/', admin.site.urls),
    path('admin/', include('adminn.urls')),
    path('rest/', include('client.urls')),
    path('auth/', include('account.urls')),
    path('vendor/', include('vendor.urls'))
]
