from rest_framework.views import APIView, Request, Response, status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import User
from .fyrebase import auth
from .permissions import IsAccountOwner
from .serializers import LoginSerializer, UserSerializer
from .middlewares import FirebaseAuthentication


class UserViewsets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountOwner]
    authentication_classes = [FirebaseAuthentication]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print(serializer.data)

        auth.create_user_with_email_and_password(
            email=serializer.data["email"], password=request.data["password"]
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginViewsets(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = auth.sign_in_with_email_and_password(
            email=serializer.data["email"], password=serializer.data["password"]
        )

        return Response({'access': login["idToken"], 'refresh': login["refreshToken"]}, status=status.HTTP_200_OK)
