from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import LoginViewsets, UserViewsets, ResetarSenhaView

router = DefaultRouter()
router.register("users", UserViewsets)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginViewsets.as_view()),
    path("password/reset/", ResetarSenhaView.as_view()),
]
