from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Lamp, Permission, Zone


class ZoneAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='resident', password='test-password')
        self.zone = Zone.objects.create(name='Shared zone', building='Test', floor=1)
        self.lamp = Lamp.objects.create(name='Desk', zone=self.zone, user=self.user)

    def test_unassigned_user_cannot_control_zone(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('control_zone', args=[self.zone.pk]), {'action': 'turn_on'})
        self.assertEqual(response.status_code, 404)

    def test_read_only_user_cannot_control_zone(self):
        Permission.objects.create(user=self.user, zone=self.zone, can_view=True)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('control_zone', args=[self.zone.pk])).status_code, 200)
        self.assertEqual(self.client.post(reverse('control_zone', args=[self.zone.pk]), {'action': 'turn_on'}).status_code, 404)

    @patch('core.views.LightController')
    def test_authorized_user_can_control_zone(self, controller):
        Permission.objects.create(user=self.user, zone=self.zone, can_control=True)
        self.client.force_login(self.user)
        response = self.client.post(reverse('control_zone', args=[self.zone.pk]), {'action': 'turn_on'})
        self.assertEqual(response.status_code, 302)
        controller.return_value.turn_on.assert_called_once_with(self.zone.pk)

    def test_toggle_lamp_rejects_get(self):
        Permission.objects.create(user=self.user, zone=self.zone, can_control=True)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('toggle_lamp', args=[self.lamp.pk])).status_code, 405)

    def test_simulation_requires_login(self):
        self.assertEqual(self.client.get(reverse('simulation')).status_code, 302)
