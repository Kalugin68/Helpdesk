from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from users.models import User


class TicketPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == User.Role.ADMIN:
            return True

        if request.method in SAFE_METHODS:
            return True

        if user.role == User.Role.SUPPORT:
            return True

        if user.role == User.Role.USER:
            if request.method == 'POST':
                return True

        return False