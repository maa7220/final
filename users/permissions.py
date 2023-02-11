from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_admin)


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_doctor)


class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_nurse)
