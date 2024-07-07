from rest_framework.permissions import BasePermission


class RoleEmployeeBasedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['СОТРУДНИК']


class RoleCustomerBasedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ЗАКАЗЧИК']
