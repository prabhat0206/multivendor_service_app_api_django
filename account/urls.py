from django.urls import path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('wallet', AddBalanceToWallet.as_view(), name='wallet'),
    path('user/login', LoginUser.as_view(), name='user')
]
