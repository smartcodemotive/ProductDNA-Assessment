from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Tag, Task


class TaskAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_task_with_nested_tags(self):
        response = self.client.post(
            reverse('task-list'),
            {
                'title': 'Write docs',
                'description': 'API documentation',
                'status': 'pending',
                'tag_names': [{'name': 'work'}, {'name': 'docs'}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['tags']), 2)
        self.assertEqual(Tag.objects.count(), 2)

    def test_duplicate_tag_name_rejected(self):
        Tag.objects.create(name='work')
        response = self.client.post(
            reverse('tag-list'),
            {'name': 'work'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_tasks_by_status(self):
        Task.objects.create(title='A', status=Task.Status.PENDING)
        Task.objects.create(title='B', status=Task.Status.DONE)

        response = self.client.get(reverse('task-list'), {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'A')

    def test_filter_tasks_by_tag(self):
        tag = Tag.objects.create(name='work')
        task = Task.objects.create(title='Meeting', status=Task.Status.IN_PROGRESS)
        task.tags.add(tag)
        Task.objects.create(title='Other', status=Task.Status.PENDING)

        response = self.client.get(reverse('task-list'), {'tag': 'work'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Meeting')

    def test_unauthenticated_request_denied(self):
        client = APIClient()
        response = client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tag_crud(self):
        create = self.client.post(reverse('tag-list'), {'name': 'urgent'}, format='json')
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        tag_id = create.data['id']

        detail = self.client.get(reverse('tag-detail', args=[tag_id]))
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

        update = self.client.patch(
            reverse('tag-detail', args=[tag_id]),
            {'name': 'high-priority'},
            format='json',
        )
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        self.assertEqual(update.data['name'], 'high-priority')

        delete = self.client.delete(reverse('tag-detail', args=[tag_id]))
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
