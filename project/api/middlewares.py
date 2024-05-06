import os

import dotenv
import firebase_admin
from django.forms.models import model_to_dict
from firebase_admin import auth, credentials
from rest_framework import authentication
from rest_framework.views import Request, Response, status

from ..models import User

dotenv.load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CRED"))
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
            # Faça algo com o UID, como autenticar o usuário
            user = model_to_dict(User.objects.get(email=email))
            user.update({"is_authenticated": True})
            return (user, None)
        except auth.InvalidIdTokenError:
            # Token inválido
            raise ("message: token invalido!")
        except Exception as e:
            # Outro erro
            raise (f"Erro ao verificar o token do Firebase: {e}")
