import pyrebase
from rest_framework.views import APIView, Request, Response, status
from rest_framework.viewsets import ModelViewSet

from ..models import User
from .fyrebase import auth
from .middlewares import FirebaseAuthentication
from .permissions import IsAccountOwner
from .serializers import (LoginSerializer, ResetPasswordSerializer,
                          UserSerializer)


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
            return Response({"message": "You dont have permission for this action"}, status=status.HTTP_403_FORBIDDEN)

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
        login = auth.sign_in_with_email_and_password(
            email=serializer.data["email"], password=serializer.data["password"]
        )

        return Response(
            {"access": login["idToken"], "refresh": login["refreshToken"]},
            status=status.HTTP_200_OK,
        )


class ResetarSenhaView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        try:
            user = auth.send_password_reset_email(email)
            return Response({"message": "enviou email"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Email não enviado"}, status=status.HTTP_400_BAD_REQUEST
            )
