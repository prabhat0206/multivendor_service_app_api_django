from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import *
from django.contrib.auth import password_validation
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.contrib import auth


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
            created_user = User.objects.get(id=serialized.data["id"])
            if "referal_code_other" in request.data:
                user = User.objects.get(
                    referal_code=request.data["referal_code_other"])
                if (user):
                    user.earned_points += 10
                    user.save()
            return Response({"success": True, "data": self.serializer_class(created_user).data, "token": created_user.auth_token.key})

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


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_with_ph_number(request):
    data = request.data
    user = User.objects.filter(ph_number=data.get('ph_number')).first()
    if (user):
        if user.check_password(data["password"]):
            return Response({"success": True, "token": user.auth_token.key, "user": UserSerializer(user).data})
    return Response({"success": False, "error": "Server unable to authenticate you"})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def set_profile_picture(request):
    data = request.FILES.get('image', None)
    if data:
        user = request.user
        user.profile_pic = data
        user.save()
        return Response({"success": True, "message": "profile set successfully"})
    return Response({"success": False, "error": "image not found"})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def refer_and_earn(request):
    code = request.data.get("referal_code", None)
    if code:
        user = request.user
        if user.refered_by:
            return Response(406)
        else:
            referal_user = User.objects.get(referal_code=code)
            if referal_user:
                user.refered_by = code
                user.save()
                referal_user.earned_points += 10
                referal_user.save()
                return Response({"success": True})
            else:
                return Response(404)
    else:
        return Response(400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    return Response(UserSerializer(request.user).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_user_existance(request):
    user = User.objects.filter(ph_number="+91"+request.GET.get("ph_number")).first()
    if user: return Response({"success": True}) 
    else: return Response({"success": False})
