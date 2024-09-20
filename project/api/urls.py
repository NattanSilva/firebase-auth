from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (
    AdminLoginViewset,
    CrescimentoCriancaViewset,
    CriancaViewset,
    EnderecoViewsets,
    GetCriancasPorProfissional,
    GraficoCrescimentoCriancaViewset,
    GrupoAddProfissional,
    GrupoRemoveProfissional,
    GrupoUsfViewsets,
    LoginViewsets,
    ResetarSenhaView,
    UserViewsets,
    UsfViewsets,
)

router = DefaultRouter()
router.register("users", UserViewsets)
router.register("crianca", CriancaViewset)
router.register("crescimentoCrianca", CrescimentoCriancaViewset)
router.register("enderecos", EnderecoViewsets)
router.register("usf", UsfViewsets)
router.register("grupoUsf", GrupoUsfViewsets)
router.register(r"adminLogin", AdminLoginViewset, basename="adminLogin")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginViewsets.as_view()),
    path("password/reset/", ResetarSenhaView.as_view()),
    path("crianca-profissional/", GetCriancasPorProfissional.as_view()),
    path(
        "graficos/crescimento/<int:id_crianca>/",
        GraficoCrescimentoCriancaViewset.as_view(),
    ),
    path("grupoUsf/<int:id_grupo>/add", GrupoAddProfissional.as_view()),
    path("grupoUsf/<int:id_grupo>/remove", GrupoRemoveProfissional.as_view()),
]
