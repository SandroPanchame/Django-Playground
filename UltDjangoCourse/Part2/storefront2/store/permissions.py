# For creating custom permissions
# from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import permissions
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def _init_(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        # to make a GET request, user should have the view permission
        
class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')