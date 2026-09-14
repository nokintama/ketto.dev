from django.conf import settings
from rest_framework import permissions


class HasServiceToken(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('X-Service-Token')
        return token == settings.SERVICE_TOKEN