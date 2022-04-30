from rest_framework.serializers import ModelSerializer
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(ModelSerializer):

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = User
        exclude = ['user_permissions', 'groups']
        extra_kwargs = {'password': {'write_only': True}}


