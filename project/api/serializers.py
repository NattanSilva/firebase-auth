from rest_framework import serializers

from ..models import (
    CrescimentoCrianca,
    Crianca,
    Endereco,
    GrupoUsf,
    UnidadeSaudeFamiliar,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        write_only_fields = ["password"]
        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=12)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CriancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crianca
        fields = "__all__"


class CrescimentoCriancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrescimentoCrianca
        fields = "__all__"


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = "__all__"


class GrupoUsfSerializer(serializers.ModelSerializer):
    profissionais = UserSerializer(many=True, read_only=True)

    class Meta:
        model = GrupoUsf
        fields = "__all__"


class UnidadeSaudeFamiliarSerializer(serializers.ModelSerializer):
    grupos = GrupoUsfSerializer(many=True, read_only=True)

    class Meta:
        model = UnidadeSaudeFamiliar
        fields = ["id", "nome", "criadoEmDiaMesAno", "endereco", "grupos"]


class AdicionarProfissionalSerializer(serializers.Serializer):
    idProfissional = serializers.IntegerField()
