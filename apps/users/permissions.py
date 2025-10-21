from rest_framework.permissions import BasePermission

from apps.users.permissions import HasRole, MinimumRoleLevel, APIView

class HasRole(BasePermission):
    """
    Allow access only for users having specific role slug(s).
    Usage:
        permission_classes = [HasRole('admin')]  # only admin
        permission_classes = [HasRole('agent', 'admin')]  # agent or admin
    """

    def __init__(self, *required_slugs):
        self.required_slugs = required_slugs

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not request.user.role:
            return False
        return request.user.role.slug in self.required_slugs


class MinimumRoleLevel(BasePermission):
    """
    Allow if user's role.level >= required level
    Usage: MinimumRoleLevel(80)  # admin & above (superadmin)
    """

    def __init__(self, min_level):
        self.min_level = min_level

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.role:
            return False
        return user.role.level >= self.min_level




class SomeAdminView(APIView): 
    permission_classes = [MinimumRoleLevel(80)]  # admin & superadmin

class AgentView(APIView):
    permission_classes = [HasRole('agent', 'admin', 'superadmin')]
