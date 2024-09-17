import os

import dotenv
import firebase_admin
from django.forms.models import model_to_dict
from firebase_admin import auth, credentials
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import Request

from ..models import User

from .utils import validate_env_variables

dotenv.load_dotenv()

validate_env_variables(
    [
        "FIREBASE_PROJECT_ID",
        "FIREBASE_PRIVATE_KEY_ID",
        "FIREBASE_PRIVATE_KEY",
        "FIREBASE_CLIENT_EMAIL",
        "FIREBASE_CLIENT_ID",
        "FIREBASE_CLIENT_CERT_URL",
    ]
)

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
        "universe_domain": "googleapis.com",
    }
)
firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        id_token = request.headers.get("Authorization")

        if not id_token:
            return None

        try:
            decoded_token = auth.verify_id_token(id_token.split(" ")[1])
            print("Token verificado com sucesso!")
            email = decoded_token["email"]
            user = model_to_dict(User.objects.get(email=email))
            user.update({"is_authenticated": True})
            user.pop("password")
            request.validated_email = email
            return (user, None)
        except auth.InvalidIdTokenError:
            # Token inválido
            raise AuthenticationFailed("Token inválido")
        except User.DoesNotExist:
            # Usuário não encontrado
            raise AuthenticationFailed("Usuário não encontrado")
        except Exception as e:
            # Outro erro
            raise AuthenticationFailed(str(e))
