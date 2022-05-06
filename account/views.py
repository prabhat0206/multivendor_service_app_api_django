from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import *
from django.contrib.auth import password_validation
from rest_framework.response import Response
from django.conf import settings


class Login(ObtainAuthToken):
    def post(self, request):
        serialized = self.serializer_class(
            data=request.data, context={'request': request})
        if serialized.is_valid():
            user = serialized.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            serialized_user = UserSerializer(user).data
            return Response({"Success": True, "token": token.key, "user": serialized_user})
        return Response({"Success": False, "Error": "Invalid login credentials"})


class LoginUser(ObtainAuthToken):

    def validate_password(self, value):
        print(password_validation.validate_password(value, self.instance))
        return value

    def post(self, request):
        data = request.data
        self.validate_password(data['password'])
        return Response({"Success": True})


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        new_user = request.data
        new_user['superuser'] = False
        new_user['staff'] = False
        serialized = self.serializer_class(data=new_user)
        if (serialized.is_valid()):
            serialized.save()
            if "referal_code_other" in request.data:
                user = User.objects.get(referal_code=request.data["referal_code_other"])
                if (user):
                    user.earned_points += 10
                    user.save()
            return Response({"success": True, "data": serialized.data})
        
        return Response({"success": False, "error": serialized.errors})


class AddBalanceToWallet(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request):
        instance = self.request.user
        data = request.data
        balance_to_add = data.pop("amount")
        if (settings.CLIENT.utility.verify_payment_signature(data)):
            instance.wallet_balance += balance_to_add
            instance.save()
            return Response({"success": True})
        else:
            return Response({"success": False, "error": "Server is not responding correctly"})
