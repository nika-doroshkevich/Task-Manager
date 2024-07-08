from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from tasks.models import Task
from tasks.utils import TaskStatuses

UserModel = get_user_model()


class TestModels(TestCase):
    def test_model_task(self):
        customer = UserModel.objects.create_user(email='email', password='password',
                                                 full_name='full_name', phone='phone', role='СОТРУДНИК')
        task = Task.objects.create(
            name='Task_1',
            customer=customer
        )
        self.assertEquals(str(task), 'Task_1')
        self.assertTrue(isinstance(task, Task))


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.employee1 = UserModel.objects.create_user(
            email='email1',
            password='password',
            full_name='employee',
            phone='phone',
            role='СОТРУДНИК'
        )
        self.employee2 = UserModel.objects.create_user(
            email='email2',
            password='password',
            full_name='employee',
            phone='phone',
            role='СОТРУДНИК'
        )
        self.employee_staff = UserModel.objects.create_user(
            email='email3',
            password='password',
            full_name='employee_staff',
            phone='phone',
            role='СОТРУДНИК',
            is_staff=1
        )
        self.customer1 = UserModel.objects.create_user(
            email='email4',
            password='password',
            full_name='customer',
            phone='phone',
            role='ЗАКАЗЧИК'
        )

        self.customer2 = UserModel.objects.create_user(
            email='email5',
            password='password',
            full_name='customer',
            phone='phone',
            role='ЗАКАЗЧИК'
        )

        self.task1 = Task.objects.create(
            name='Task_1',
            customer=self.customer1
        )
        self.task2 = Task.objects.create(
            name='Task_2',
            customer=self.customer2,
            employee=self.employee1
        )
        self.task3 = Task.objects.create(
            name='Task_3',
            customer=self.customer2,
            employee=self.employee2
        )

    def test_create_task(self):
        self.client.force_authenticate(user=self.employee_staff)
        url = reverse('task_create')
        data = {
            'name': 'New_Task',
            'customer': self.customer1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)

    def test_list_tasks_for_employee(self):
        self.client.force_authenticate(user=self.employee1)
        url = reverse('task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_tasks_for_employee_staff(self):
        self.client.force_authenticate(user=self.employee_staff)
        url = reverse('task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_tasks_for_customer(self):
        self.client.force_authenticate(user=self.customer1)
        url = reverse('task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_task(self):
        self.client.force_authenticate(user=self.employee1)
        url = reverse('task_detail', args=[self.task1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task1.id)

    def test_update_task(self):
        self.client.force_authenticate(user=self.employee1)
        url = reverse('task_update', args=[self.task2.id])
        data = {
            'name': 'Updated_Task_2'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task2.refresh_from_db()
        self.assertEqual(self.task2.name, 'Updated_Task_2')
        self.assertEqual(self.task2.updated_date, timezone.now().date())

    def test_assign_task(self):
        self.client.force_authenticate(user=self.employee1)
        url = reverse('task_assign', args=[self.task1.id])
        data = {
            'employee': self.employee1.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.employee, self.employee1)
        self.assertEqual(self.task1.status, TaskStatuses.IN_PROGRESS.value)
        self.assertEqual(self.task1.updated_date, timezone.now().date())

    def test_complete_task(self):
        self.client.force_authenticate(user=self.employee1)
        url = reverse('task_complete', args=[self.task2.id])
        data = {
            'report': 'report'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task2.refresh_from_db()
        self.assertEqual(self.task2.status, TaskStatuses.DONE.value)
        self.assertEqual(self.task2.completed_date, timezone.now().date())
