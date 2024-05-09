from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.views import Request, View


class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        auth_header = request.headers.get("Authorization")

        if request.method == "POST":
            return True

        if not auth_header or not auth_header.startswith("Bearer "):
            return False
        
        if request.user["is_authenticated"]:
            return True
