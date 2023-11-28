from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

User = get_user_model()
class TaskModelTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='Description for testing',
            due_date='2023-12-12',
            status='OPEN'
        )

    def test_task_creation(self):
        task = Task.objects.get(title='Test Task')
        self.assertEqual(task.description, 'Description for testing')

    def test_task_attributes(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.due_date, '2023-12-12')
        self.assertEqual(self.task.status, 'OPEN')

        # Additional assertions for attributes
        self.assertIsNotNone(self.task.timestamp)  # Checking timestamp is not None
        self.assertEqual(self.task.tags.count(), 0)  # Checking tags count initially
        self.assertEqual(self.task.description[:5], 'Descr')  # Checking partial description
        self.assertIn('Task', self.task.title)  # Checking for a substring in title
        self.assertTrue(self.task.status in ['OPEN', 'WORKING', 'DONE', 'OVERDUE'])  # Checking status value

    def test_task_title_max_length(self):
        max_length = self.task._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_task_description_max_length(self):
        max_length = self.task._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_task_str_representation(self):
        self.assertEqual(str(self.task), self.task.title)

    def test_task_default_status(self):
        new_task = Task.objects.create(
            title='New Task',
            description='New Description',
            due_date='2023-12-12'
        )
        self.assertEqual(new_task.status, 'OPEN')
print("Integration test")
class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='Description for testing',
            due_date='2023-12-12',
            status='OPEN'
        )
        self.superuser = User.objects.create_superuser(username='admin', email='', password='password')
        self.client.credentials(HTTP_AUTHORIZATION='Basic YWRtaW46cGFzc3dvcmQ=')


    def test_get_single_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')
        self.assertEqual(response.data['description'], 'Description for testing')

    def test_create_task(self):
        url = reverse('task-list-create')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'due_date': '2024-01-01',
            'status': 'OPEN'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'due_date': '2023-12-15',
            'status': 'WORKING'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(pk=self.task.id)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.description, 'Updated Description')

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.id).exists())
    def test_read_all_tasks(self):
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0) 

    def test_read_filtered_tasks(self):
        url = reverse('task-list-create')
        data = {'status': 'OPEN'}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  
    def test_failed_create_task(self):
        # Try creating a task with incomplete data
        url = reverse('task-list-create')
        data = {
            'description': 'Incomplete Task',
            'due_date': '2023-12-12',
            'status': 'OPEN'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)