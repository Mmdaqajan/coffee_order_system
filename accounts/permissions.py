from rest_framework.permissions import BasePermission


class IsBarista(BasePermission):
    message = "شما دسترسی باریستا را ندارید."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if not hasattr(request.user, "profile"):
            return False

        return request.user.profile.role == "barista"