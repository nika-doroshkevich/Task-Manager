from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.utils import TaskStatuses


class TaskAPICreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TaskAPIList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return get_task_queryset(user)


class TaskAPIRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return get_task_queryset(user)


def get_task_queryset(user):
    if user.role == 'СОТРУДНИК' and user.is_staff == 1:
        queryset = Task.objects.all()
    else:
        if user.role == 'СОТРУДНИК':
            queryset = Task.objects.filter(Q(employee=user.id) | Q(employee=None))
        else:
            if user.role == 'ЗАКАЗЧИК':
                queryset = Task.objects.filter(customer=user.id)
            else:
                queryset = []
    return queryset


class BaseTaskAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.status == TaskStatuses.DONE.value:
            raise ValidationError({"detail": "Завершенная задача не доступна для редактирования"})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.handle_update(serializer, instance, request)
        self.perform_update(serializer)
        return Response(serializer.data)

    def handle_update(self, serializer, instance, request):
        pass


class TaskAPIAssign(BaseTaskAPIView):
    def handle_update(self, serializer, instance, request):
        serializer.instance = serializer.assign_task(instance)


class TaskAPIComplete(BaseTaskAPIView):
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(employee=user.id)

    def handle_update(self, serializer, instance, request):
        serializer.instance = serializer.complete_task(instance, serializer.validated_data)


class TaskAPIUpdate(BaseTaskAPIView):
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(employee=user.id)

    def handle_update(self, serializer, instance, request):
        instance.updated_date = timezone.now().date()
        instance.save()
