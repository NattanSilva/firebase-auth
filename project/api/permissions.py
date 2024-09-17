from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.views import Request, View

from ..models import CriancaProfissional


class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        auth_header = request.headers.get("Authorization")

        if request.method == "POST" or request.method in SAFE_METHODS:
            return True

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        if request.user["is_authenticated"]:
            return True

    def has_object_permission(self, request: Request, view: View, obj: dict):
        if request.user["id"] == obj.id:
            return True


class ProfissionalPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        if request.user["is_authenticated"]:
            return True

    def has_object_permission(self, request: Request, view: View, obj: dict) -> bool:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        if request.user["is_authenticated"]:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        auth_header = request.headers.get("Authorization")

        if request.method in SAFE_METHODS:
            return True

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )
