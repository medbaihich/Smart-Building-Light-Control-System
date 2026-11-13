from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Permission, Zone


class SecurityAPITests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username='staff', password='test-password', is_staff=True)
        self.user = User.objects.create_user(username='user', password='test-password')
        self.visible = Zone.objects.create(name='Visible', building='Lab', floor=1)
        self.hidden = Zone.objects.create(name='Hidden', building='Lab', floor=2)
        Permission.objects.create(user=self.user, zone=self.visible, can_view=True)

    def test_anonymous_user_cannot_list_zones(self):
        self.assertIn(self.client.get('/api/zones/').status_code, (401, 403))

    def test_regular_user_cannot_modify_zones(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.post('/api/zones/', {'name': 'Unauthorized'}).status_code, 403)

    def test_regular_user_cannot_manage_accounts_or_permissions(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get('/api/users/').status_code, 403)
        self.assertEqual(self.client.get('/api/permissions/').status_code, 403)

    def test_regular_user_only_sees_authorized_zones(self):
        self.client.force_login(self.user)
        result = self.client.get('/api/zones/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual([row['name'] for row in result.json()], ['Visible'])

    def test_staff_can_list_zones(self):
        self.client.force_login(self.staff)
        result = self.client.get('/api/zones/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.json()), 2)
