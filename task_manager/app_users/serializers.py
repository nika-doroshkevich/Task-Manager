from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or UserModel.objects.filter(email=email).exists():
            raise ValidationError({"detail": "Please choose another email"})

        if not password or len(password) < 8:
            raise ValidationError({"detail": "Please choose another password, min 8 characters"})

        user_obj = UserModel.objects.create_user(email=attrs['email'], password=attrs['password'],
                                                 full_name=attrs['full_name'], phone=attrs['phone'], role=attrs['role'])
        user_obj.save()
        return user_obj


class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError({"detail": "Неверные логин или пароль"})

        user.last_login = timezone.now()
        user.save()

        token = super().validate(attrs)
        token['role'] = user.role
        token['id'] = user.id
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
