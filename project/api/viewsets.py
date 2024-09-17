import pyrebase
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import (
    CrescimentoCrianca,
    Crianca,
    CriancaProfissional,
    Endereco,
    GrupoUsf,
    UnidadeSaudeFamiliar,
    User,
)
from .fyrebase import auth
from .middlewares import FirebaseAuthentication
from .permissions import IsAccountOwner, IsAdminOrReadOnly, ProfissionalPermission
from .serializers import (
    AdicionarProfissionalSerializer,
    CrescimentoCriancaSerializer,
    CriancaSerializer,
    EnderecoSerializer,
    GrupoUsfSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    UnidadeSaudeFamiliarSerializer,
    UserSerializer,
)
from .utils import ordenar_dados_crescimento_crianca


def send_email_verification(email: str, password: str):
    token: str = ""
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        token += login["idToken"]
    except pyrebase.pyrebase.HTTPError as err:
        return Response(
            {"erro-login-da-verificação-email": str(err)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        auth.send_email_verification(id_token=login["idToken"])
    except pyrebase.pyrebase.HTTPError as err:
        return Response(
            {"erro-verificação-email": str(err)}, status=status.HTTP_400_BAD_REQUEST
        )


class UserViewsets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountOwner]
    authentication_classes = [FirebaseAuthentication]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            auth.create_user_with_email_and_password(
                email=request.data["email"], password=request.data["password"]
            )

            send_email_verification(request.data["email"], request.data["password"])

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except pyrebase.pyrebase.HTTPError as err:
            if "EMAIL_EXISTS" in str(err):
                return Response(
                    {"message": "Email ja existe!"}, status=status.HTTP_409_CONFLICT
                )
            else:
                return Response({"erro": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args, **kwargs):
        token = request.headers.get("Authorization").split(" ")[1]

        pk = kwargs.get("pk")

        user_to_delete = User.objects.get(id=pk)

        if request.validated_email != user_to_delete.email:
            return Response(
                {"message": "You dont have permission for this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            auth.delete_user_account(token)
            return super().destroy(request, *args, **kwargs)
        except pyrebase.pyrebase.HTTPError as err:
            return Response(
                {"message": "Erro ao deletar conta", "erro": str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginViewsets(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            login = auth.sign_in_with_email_and_password(
                email=serializer.data["email"], password=serializer.data["password"]
            )

            return Response(
                {"access": login["idToken"], "refresh": login["refreshToken"]},
                status=status.HTTP_200_OK,
            )
        except pyrebase.pyrebase.HTTPError as err:
            if "INVALID_LOGIN_CREDENTIALS" in str(err):
                return Response(
                    {"message": "Email e/ou senha inválidos"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class ResetarSenhaView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]

        try:
            user_email_exists_validation = get_object_or_404(User, email=email)
            user = auth.send_password_reset_email(email)
            return Response({"message": "enviou email"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Email não enviado"}, status=status.HTTP_400_BAD_REQUEST
            )


class CriancaViewset(ModelViewSet):
    queryset = Crianca.objects.all()
    serializer_class = CriancaSerializer
    permission_classes = [ProfissionalPermission]
    authentication_classes = [FirebaseAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = CriancaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        crianca = Crianca.objects.get(id=serializer.data["id"])
        user = User.objects.get(id=request.user["id"])

        CriancaProfissional.objects.create(idCrianca=crianca, idProfissional=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetCriancasPorProfissional(APIView):
    permission_classes = [ProfissionalPermission]
    authentication_classes = [FirebaseAuthentication]

    def get(self, request: Request) -> Response:
        user = User.objects.get(id=request.user["id"])
        crianca_profissionais = CriancaProfissional.objects.filter(idProfissional=user)

        crianca_ids = [crianca.idCrianca.id for crianca in crianca_profissionais]

        criancas = []

        for id in crianca_ids:
            criancas.append(model_to_dict(Crianca.objects.get(id=id)))

        return Response(criancas, status=status.HTTP_200_OK)


class CrescimentoCriancaViewset(ModelViewSet):
    queryset = CrescimentoCrianca.objects.all()
    serializer_class = CrescimentoCriancaSerializer


class GraficoCrescimentoCriancaViewset(APIView):
    def get(self, request: Request, id_crianca: int) -> Response:
        # Validação do ID da criança
        crianca = get_object_or_404(Crianca, id=id_crianca)

        final_data = {
            "sexo": crianca.sexo,
            "alturas": [],
            "pesos": [],
            "perimetros": [],
            "imcs": [],
        }

        # Busca de dados de acordo com a criança
        lista_dados = CrescimentoCrianca.objects.filter(idCrianca=id_crianca)

        # Verificação se existem dados
        if not lista_dados:
            return Response(
                {"detail": "Nenhum dado encontrado para essa crianca."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CrescimentoCriancaSerializer(data=lista_dados, many=True)
        serializer.is_valid()

        # Ordenção dos dados de acordo com a idade da criança
        lista_ordenada = ordenar_dados_crescimento_crianca(serializer.data)

        for item in lista_ordenada:
            if item["idadeCrianca"] == "primeira semana":
                final_data["alturas"].append({"x": 0, "y": item["altura"]})
                final_data["pesos"].append({"x": 0, "y": item["peso"]})
                final_data["perimetros"].append({"x": 0, "y": item["perimetro"]})
                final_data["imcs"].append({"x": 0, "y": item["imc"]})
            else:
                final_data["alturas"].append(
                    {
                        "x": int(item["idadeCrianca"].split(" ")[0]),
                        "y": item["altura"],
                    }
                )
                final_data["pesos"].append(
                    {
                        "x": int(item["idadeCrianca"].split(" ")[0]),
                        "y": item["peso"],
                    }
                )
                final_data["perimetros"].append(
                    {
                        "x": int(item["idadeCrianca"].split(" ")[0]),
                        "y": item["perimetro"],
                    }
                )
                final_data["imcs"].append(
                    {
                        "x": int(item["idadeCrianca"].split(" ")[0]),
                        "y": item["imc"],
                    }
                )

        return Response(final_data, status=status.HTTP_200_OK)


class EnderecoViewsets(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer


class UsfViewsets(ModelViewSet):
    queryset = UnidadeSaudeFamiliar.objects.all()
    serializer_class = UnidadeSaudeFamiliarSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]


class GrupoUsfViewsets(ModelViewSet):
    queryset = GrupoUsf.objects.all()
    serializer_class = GrupoUsfSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]


class GrupoAddProfissional(APIView):
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, id_grupo: int) -> Response:
        serializer = AdicionarProfissionalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        grupo = get_object_or_404(GrupoUsf, id=id_grupo)
        profissional = get_object_or_404(User, id=serializer.data["idProfissional"])

        grupo.profissionais.add(profissional)
        grupo.save()

        grupoSerializer = GrupoUsfSerializer(data=grupo)
        grupoSerializer.is_valid()

        return Response(
            {"message": "Profissional adicionado com sucesso."},
            status=status.HTTP_200_OK,
        )


class GrupoRemoveProfissional(APIView):
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def delete(self, request: Request, id_grupo: int) -> Response:
        serializer = AdicionarProfissionalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        grupo = get_object_or_404(GrupoUsf, id=id_grupo)
        profissional = get_object_or_404(User, id=serializer.data["idProfissional"])

        grupo.profissionais.remove(profissional)
        grupo.save()

        grupoSerializer = GrupoUsfSerializer(data=grupo)
        grupoSerializer.is_valid()

        return Response(
            {"message": "Profissional removido com sucesso."},
            status=status.HTTP_200_OK,
        )


class AdminLoginViewset(ViewSet):
    serializer_class = TokenObtainPairSerializer
    def create(self, request, *args, **kwargs):
        view = TokenObtainPairView.as_view()

        return view(request._request, *args, **kwargs)