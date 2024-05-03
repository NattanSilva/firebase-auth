from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.views import Request, View



class IsAccountOwner(permissions.BasePermission):
  def has_permission(self, request: Request, view: View) -> bool:
    return request.method in SAFE_METHODS or request.user["is_authenticated"]