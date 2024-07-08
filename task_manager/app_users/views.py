from django.contrib.auth import get_user_model
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from app_users.serializers import UserCreateSerializer, UserLoginSerializer, UserSerializer
from task_manager.utils import RoleEmployeeBasedPermission, RoleCustomerBasedPermission

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


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, RoleCustomerBasedPermission,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
