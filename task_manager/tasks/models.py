from django.db import models
from django.utils import timezone

from app_users.models import AppUser
from tasks.utils import TaskStatuses


class Task(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=TaskStatuses.choices(), default=TaskStatuses.PENDING.value)
    employee = models.ForeignKey(AppUser, null=True, on_delete=models.PROTECT,
                                 related_name='tasks_as_employee')
    customer = models.ForeignKey(AppUser, null=True, on_delete=models.PROTECT,
                                 related_name='tasks_as_customer')
    created_date = models.DateField(default=timezone.now().date())
    updated_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    report = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
