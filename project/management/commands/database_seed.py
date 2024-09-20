import sys
from datetime import datetime

import pyrebase
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_seed import Seed

from project.models import (CrescimentoCrianca, Crianca, CriancaProfissional,
                            Endereco, GrupoUsf, Periodo, UnidadeSaudeFamiliar,
                            User)

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

        # Criando dados de crescimento do joãzinho
        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.PRIMEIRA_SEMANA._value_,
                "altura": 45,
                "peso": 3.5,
                "perimetro": 2,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.UM_MES._value_,
                "altura": 55,
                "peso": 4.1,
                "perimetro": 2.5
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.DOIS_MESES._value_,
                "altura": 57,
	            "peso": 4.8,
	            "perimetro": 2.7,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.QUATRO_MESES._value_,
                "altura": 62,
                "peso": 6.1,
                "perimetro": 3,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.SEIS_MESES._value_,
                "altura": 64,
                "peso": 7.3,
                "perimetro": 3.2,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.NOVE_MESES._value_,
                "altura": 69,
                "peso": 8.65,
                "perimetro": 4.7,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.DOZE_MESES._value_,
                "altura": 75,
                "peso": 9.8,
                "perimetro": 6.2,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.QUINZE_MESES._value_,
                "altura": 77,
                "peso": 10.4,
                "perimetro": 7.7,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.DEZOITO_MESES._value_,
                "altura": 80,
                "peso": 10.8,
                "perimetro": 9.2,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": joazinho,
                "idadeCrianca": Periodo.VINTE_QUATRO_MESES._value_,
                "altura": 85,
                "peso": 11.8,
                "perimetro": 12.2,
            }
        )

        # Criando Crescimento da silvinha
        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": silvinha,
                "idadeCrianca": Periodo.PRIMEIRA_SEMANA._value_,
                "altura": 45,
                "peso": 3.5,
                "perimetro": 2,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": silvinha,
                "idadeCrianca": Periodo.UM_MES._value_,
                "altura": 55,
                "peso": 4.1,
                "perimetro": 2.5
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": silvinha,
                "idadeCrianca": Periodo.DOIS_MESES._value_,
                "altura": 57,
	            "peso": 4.8,
	            "perimetro": 2.7,
            }
        )
        
        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": silvinha,
                "idadeCrianca": Periodo.QUATRO_MESES._value_,
                "altura": 62,
                "peso": 6.1,
                "perimetro": 3,
            }
        )

        seeder.add_entity(
            CrescimentoCrianca,
            1,
            {
                "idCrianca": silvinha,
                "idadeCrianca": Periodo.SEIS_MESES._value_,
                "altura": 64,
                "peso": 7.3,
                "perimetro": 3.2,
            }
        )

        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS("✅ Crescimento das crianças criados com sucesso.")
        )

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
