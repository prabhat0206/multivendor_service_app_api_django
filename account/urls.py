from django.urls import path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('wallet', AddBalanceToWallet.as_view(), name='wallet'),
    path('user/login', login_with_ph_number, name='user'),
    path('set_profile', set_profile_picture, name='set_profile'),
    path('refer', refer_and_earn, name='refer'),
    path('details', user_details, name='user_details'),
]
