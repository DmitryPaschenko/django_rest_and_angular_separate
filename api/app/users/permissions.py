from rest_framework import permissions
from cuser.middleware import CuserMiddleware


class DPChiefPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = False
        user = CuserMiddleware.get_user()
        if user.is_authenticated() and user.has_perm('dp_crm_chief_permission'):
            has_perm = True

        return has_perm
