from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Task
from .utils import TaskStatuses

UserModel = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role == 'ЗАКАЗЧИК':
            user = UserModel.objects.get(id=user.id)
            validated_data['customer'] = user

        if validated_data['customer'] is None:
            raise ValidationError({"detail": "Поле Customer не должно быть null"})

        task = Task.objects.create(**validated_data)
        return task

    def assign_task(self, instance):
        user = self.context['request'].user
        task_id = instance.id

        try:
            Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValidationError({"detail": "Задачи не существует"})

        if instance.employee_id is None:
            instance.employee_id = user.id
            instance.updated_date = timezone.now().date()
            instance.status = TaskStatuses.IN_PROGRESS.value

            instance.save()
            return instance
        else:
            raise ValidationError({"detail": "Задача уже выполняется"})

    def complete_task(self, instance, validated_data):
        user = self.context['request'].user
        task_id = instance.id

        try:
            Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValidationError({"detail": "Задачи не существует"})

        if validated_data['report'] is None:
            raise ValidationError({"detail": "Поле Report не может быть пустым"})

        instance.completed_date = timezone.now().date()
        instance.status = TaskStatuses.DONE.value

        instance.save()
        return instance
