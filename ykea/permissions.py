from rest_framework import permissions
from django.contrib.auth.models import User

class MyPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    message = "Only some users have permissions"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.groups.filter(name='Comercials').exists()

        return request.user.groups.filter(name='Comercials').exists()

    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Comercials').exists()
