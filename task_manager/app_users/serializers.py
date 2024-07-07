from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, data):
        user_obj = UserModel.objects.create_user(email=data['email'], password=data['password'],
                                                 full_name=data['full_name'], phone=data['phone'], role=data['role'])
        user_obj.save()
        return user_obj


class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        user.last_login = timezone.now()
        user.save()

        token = super().validate(attrs)
        token['role'] = user.role
        token['id'] = user.id
        return token
