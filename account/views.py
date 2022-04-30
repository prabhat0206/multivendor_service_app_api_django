from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializer import *
from rest_framework.response import Response


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
