from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from app_users.serializers import UserCreateSerializer, UserLoginSerializer
from task_manager.utils import RoleEmployeeBasedPermission

UserModel = get_user_model()


class UserAPICreate(APIView):
    permission_classes = (permissions.IsAuthenticated, RoleEmployeeBasedPermission,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        user = serializer.create(request.data)
        if user:
            return Response(status=status.HTTP_201_CREATED)
        return Response({"detail": "Ошибка при создании пользователя"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)
