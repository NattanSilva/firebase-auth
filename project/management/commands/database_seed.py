import sys
from datetime import datetime

import pyrebase
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_seed import Seed

from project.models import (
    CrescimentoCrianca,
    Crianca,
    CriancaProfissional,
    Endereco,
    GrupoUsf,
    UnidadeSaudeFamiliar,
    User,
)

from ...api.fyrebase import auth


def regist_user_in_firebase(email: str, password: str):
    try:
        auth.create_user_with_email_and_password(email=email, password=password)
    except pyrebase.pyrebase.HTTPError as err:
        if "EMAIL_EXISTS" in str(err):
            raise Exception(f"Email já existente no firebase!")
        else:
            raise Exception(f"Erro ao criar conta\n erro: {str(err)}")


class Command(BaseCommand):
    help = "Popula o banco de dados com dados customizados"

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # Lipando banco de dados
        User.objects.all().delete()
        Crianca.objects.all().delete()
        CriancaProfissional.objects.all().delete()
        CrescimentoCrianca.objects.all().delete()
        Endereco.objects.all().delete()
        UnidadeSaudeFamiliar.objects.all().delete()
        GrupoUsf.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ Tabelas limpas com sucesso."))

        # Criando usuários
        seeder.add_entity(
            User,
            1,
            {
                "name": "Natan",
                "email": "natan@mail.com",
                "password": "12345678",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
            },
        )

        seeder.add_entity(
            User,
            1,
            {
                "name": "Maria",
                "email": "maria@mail.com",
                "password": "12345678",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
            },
        )

        usuarios_inseridos = seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ Usuários criados com sucesso."))

        # Buscando Usuários criados
        natan = User.objects.get(id=usuarios_inseridos[User][0])
        maria = User.objects.get(id=usuarios_inseridos[User][1])

        # Cadastrando Usuários no Firebase
        regist_user_in_firebase(natan.email, "12345678")
        regist_user_in_firebase(maria.email, "12345678")
        self.stdout.write(
            self.style.SUCCESS("✅ Usuários no Firebase criados com sucesso.")
        )

        # Criando Crianças
        seeder.add_entity(
            Crianca,
            1,
            {
                "nomeDaCrianca": "Joazinho",
                "sexo": "masculino",
                "cpf": "55555555566",
                "nomeDaMae": "Flávia",
                "cpfDaMae": "12345678999",
                "dataNascimento": "25-05-2024",
                "idadeCrianca": "primeira semana",
                "maternidade": "Maria da Neves",
                "tipoDoParto": "normal",
                "idadeGestacional": "9 meses",
                "dataNascimentoMae": "24-08-1995",
            },
        )

        seeder.add_entity(
            Crianca,
            1,
            {
                "nomeDaCrianca": "Pedrinho",
                "sexo": "masculino",
                "cpf": "55555555577",
                "nomeDaMae": "Salete",
                "cpfDaMae": "12345678988",
                "dataNascimento": "03-06-2024",
                "idadeCrianca": "primeira semana",
                "maternidade": "Maria da Neves",
                "tipoDoParto": "cesária",
                "idadeGestacional": "9 meses",
                "dataNascimentoMae": "19-12-1993",
            },
        )

        seeder.add_entity(
            Crianca,
            1,
            {
                "nomeDaCrianca": "Silvinha",
                "sexo": "feminino",
                "cpf": "12555555577",
                "nomeDaMae": "Salete",
                "cpfDaMae": "12345678988",
                "dataNascimento": "25-05-2024",
                "idadeCrianca": "primeira semana",
                "maternidade": "Maria da Neves",
                "tipoDoParto": "cesária",
                "idadeGestacional": "9 meses",
                "dataNascimentoMae": "19-12-1993",
            },
        )

        criancas_inseridas = seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ Crianças criadas com sucesso."))

        # Buscando Crianças criadas
        joazinho = Crianca.objects.get(id=criancas_inseridas[Crianca][0])
        pedrinho = Crianca.objects.get(id=criancas_inseridas[Crianca][1])
        silvinha = Crianca.objects.get(id=criancas_inseridas[Crianca][2])

        # Relacionando Crianças e Usuários
        seeder.add_entity(
            CriancaProfissional,
            1,
            {
                "idCrianca": joazinho,
                "idProfissional": natan,
                "criadoEmDiaMesAno": datetime.today(),
            },
        )

        seeder.add_entity(
            CriancaProfissional,
            1,
            {
                "idCrianca": pedrinho,
                "idProfissional": natan,
                "criadoEmDiaMesAno": datetime.today().strftime("%Y-%m-%d"),
            },
        )

        seeder.add_entity(
            CriancaProfissional,
            1,
            {
                "idCrianca": silvinha,
                "idProfissional": maria,
                "criadoEmDiaMesAno": datetime.today().strftime("%Y-%m-%d"),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ Crianças relacionadas com sucesso."))

        # Criando Endereços
        seeder.add_entity(
            Endereco,
            1,
            {
                "logradouro": "Rua Ozório Veloso, Funcionários",
                "cep": "58079570",
                "numero": 120,
                "estado": "PB",
                "municipio": "João Pessoa",
                "complemento": "casa",
                "nomeUSF": "USF Funcionários",
            },
        )
        cadastro_endereco_usf = seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ Endereço da usf criado com sucesso."))

        # Buscando Endereços criados
        usf_endereco = Endereco.objects.get(id=cadastro_endereco_usf[Endereco][0])

        # Criando USF
        seeder.add_entity(
            UnidadeSaudeFamiliar,
            1,
            {
                "nome": "USF Funcionários",
                "criadoEmDiaMesAno": datetime.today(),
                "endereco": usf_endereco,
            },
        )

        cadastro_usf = seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ USF registrada com sucesso."))

        # Buscando USF criada
        usf_funcionarios = UnidadeSaudeFamiliar.objects.get(
            id=cadastro_usf[UnidadeSaudeFamiliar][0]
        )

        # Criando Grupos de Usf
        seeder.add_entity(
            GrupoUsf,
            1,
            {
                "nome": "Enfermeiros Funcionários 1",
                "usf": usf_funcionarios,
            },
        )

        seeder.add_entity(
            GrupoUsf,
            1,
            {
                "nome": "Enfermeiros Funcionários 2",
                "usf": usf_funcionarios,
            },
        )
        cadastro_grupos_usf = seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ Grupos de USF criados com sucesso."))

        # Buscando Grupos de Usf criados
        grupo_enfermeiros_funcionarios_1 = GrupoUsf.objects.get(
            id=cadastro_grupos_usf[GrupoUsf][0]
        )
        grupo_enfermeiros_funcionarios_2 = GrupoUsf.objects.get(
            id=cadastro_grupos_usf[GrupoUsf][1]
        )

        # Adicionando Profissionais aos Grupos
        grupo_enfermeiros_funcionarios_1.profissionais.add(natan)
        grupo_enfermeiros_funcionarios_2.profissionais.add(maria)

        self.stdout.write(
            self.style.SUCCESS("✅ Profissionais adicionados aos grupos com sucesso.")
        )

        # Seed completo
        self.stdout.write(self.style.SUCCESS("✅ Banco de dados populado com sucesso!"))


# from .api.fyrebase import auth

# print("✅ Banco limpo...")

# # Criando endereços
# usf_endereco = {
#     "logradouro": "Rua Ozório Veloso, Funcionários",
#     "cep": "58079570",
#     "numero": 120,
#     "estado": "PB",
#     "municipio": "João Pessoa",
#     "complemento": "casa",
#     "nomeUSF": "USF Funcionários",
# }

# first_profissional_endereco = {
#     "logradouro": "Rua teste, Funcionários",
#     "cep": "58079570",
#     "numero": 135,
#     "estado": "PB",
#     "municipio": "João Pessoa",
#     "complemento": "casa",
#     "nomeUSF": usf_endereco["nomeUSF"],
# }

# second_profissional_endereco = {
#     "logradouro": "Rua teste 2, Funcionários",
#     "cep": "58079570",
#     "numero": 144,
#     "estado": "PB",
#     "municipio": "João Pessoa",
#     "complemento": "apartamento",
#     "nomeUSF": usf_endereco["nomeUSF"],
# }

# cadastro_endereco_usf = Endereco.objects.create(**usf_endereco)
# cadastro_endereco_profissional = Endereco.objects.create(**first_profissional_endereco)
# cadastro_endereco_profissional = Endereco.objects.create(**second_profissional_endereco)

# print("✅ Endereços criados...")

# first_profissional = {
#     "name": "Nattan Silva",
#     "email": "natan@mail.com",
#     "password": "12345678",
# }

# second_profissional = {
#     "name": "Maria Souza",
#     "email": "Maria@mail.com",
#     "password": "12345678",
# }

# # Criando usuários
# cadastro_natan = User.objects.create(**first_profissional)
# cadastro_maria = User.objects.create(**second_profissional)

# # Registrando profissionais no firebase
# try:
#     auth.create_user_with_email_and_password(
#         email=first_profissional["email"], password=first_profissional["password"]
#     )
#     auth.create_user_with_email_and_password(
#         email=second_profissional["email"], password=second_profissional["password"]
#     )
# except pyrebase.pyrebase.HTTPError as err:
#     if "EMAIL_EXISTS" in str(err):
#         print("message: Email ja existe!")
#         exit()
#     else:
#         print(f"erro: {str(err)}")
#         exit()


# print("✅ Profissionais criados...")

# # Criando crianças
# first_crianca = {
#     "nomeDaCrianca": "Joazinho",
#     "sexo": "masculino",
#     "cpf": "55555555566",
#     "nomeDaMae": "Flávia",
#     "cpfDaMae": "12345678999",
#     "dataNascimento": "25-05-2024",
#     "idadeCrianca": "primeira semana",
#     "maternidade": "Maria da Neves",
#     "tipoDoParto": "normal",
#     "idadeGestacional": "9 meses",
#     "dataNascimentoMae": "24-08-1995",
# }

# second_crianca = {
#     "nomeDaCrianca": "Pedrinho",
#     "sexo": "masculino",
#     "cpf": "55555555577",
#     "nomeDaMae": "Salete",
#     "cpfDaMae": "12345678988",
#     "dataNascimento": "03-06-2024",
#     "idadeCrianca": "primeira semana",
#     "maternidade": "Maria da Neves",
#     "tipoDoParto": "cesária",
#     "idadeGestacional": "9 meses",
#     "dataNascimentoMae": "19-12-1993",
# }

# third_crianca = {
#     "nomeDaCrianca": "Silvinha",
#     "sexo": "feminino",
#     "cpf": "12555555577",
#     "nomeDaMae": "Salete",
#     "cpfDaMae": "12345678988",
#     "dataNascimento": "25-05-2024",
#     "idadeCrianca": "primeira semana",
#     "maternidade": "Maria da Neves",
#     "tipoDoParto": "cesária",
#     "idadeGestacional": "9 meses",
#     "dataNascimentoMae": "19-12-1993",
# }

# cadastro_first_crianca = Crianca.objects.create(**first_crianca)
# cadastro_second_crianca = Crianca.objects.create(**second_crianca)
# cadastro_third_crianca = Crianca.objects.create(**third_crianca)

# print("✅ Crianças criadas...")

# CriancaProfissional.objects.create(
#     idCrianca=cadastro_first_crianca, idProfissional=cadastro_natan
# )
# CriancaProfissional.objects.create(
#     idCrianca=cadastro_second_crianca, idProfissional=cadastro_natan
# )
# CriancaProfissional.objects.create(
#     idCrianca=cadastro_third_crianca, idProfissional=cadastro_maria
# )

# print("✅ Crianças relacionadas aos profissionais...")
