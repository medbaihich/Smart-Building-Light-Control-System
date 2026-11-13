"""Authenticated REST endpoints with explicit staff and per-zone authorization."""

from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ActivityLog, Lamp, Permission, Schedule, Zone
from .serializers import (ActivityLogSerializer, PermissionSerializer,
                          ScheduleSerializer, UserSerializer, ZoneSerializer)


class StaffWriteOrAuthenticatedRead(BasePermission):
    """Authenticated readers; only staff can create/edit/delete records."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and
                    (request.method in SAFE_METHODS or user.is_staff))


def visible_zone_ids(user):
    return (Permission.objects.filter(user=user)
            .filter(Q(can_view=True) | Q(can_control=True))
            .values_list('zone_id', flat=True))


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Only staff can enumerate accounts. Account creation happens in staff UI."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ZoneViewSet(viewsets.ModelViewSet):
    serializer_class = ZoneSerializer
    permission_classes = [StaffWriteOrAuthenticatedRead]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Zone.objects.all()
        return Zone.objects.filter(pk__in=visible_zone_ids(self.request.user))


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [StaffWriteOrAuthenticatedRead]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(zone_id__in=visible_zone_ids(self.request.user))


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit history is read-only through the API and visible only to staff."""
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminUser]


class LampStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lamps = Lamp.objects.all()
        if not request.user.is_staff:
            lamps = lamps.filter(zone_id__in=visible_zone_ids(request.user))
        return Response([{'id': lamp.id, 'status': lamp.status} for lamp in lamps])
