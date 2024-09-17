from django.contrib import admin
from .models import (
    CrescimentoCrianca,
    Crianca,
    CriancaProfissional,
    Endereco,
    GrupoUsf,
    UnidadeSaudeFamiliar,
    User,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Crianca)
admin.site.register(CriancaProfissional)
admin.site.register(CrescimentoCrianca)
admin.site.register(Endereco)
admin.site.register(GrupoUsf)
admin.site.register(UnidadeSaudeFamiliar)
