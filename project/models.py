from enum import Enum

from django.db import models


class Periodo(Enum):
    PRIMEIRA_SEMANA = "primeira semana"
    UM_MES = "1 mês"
    DOIS_MESES = "2 meses"
    QUATRO_MESES = "4 meses"
    SEIS_MESES = "6 meses"
    NOVE_MESES = "9 meses"
    DOZE_MESES = "12 meses"  # 1 ano
    QUINZE_MESES = "15 meses"
    DEZOITO_MESES = "18 meses"
    VINTE_QUATRO_MESES = "24 meses"  # 2 anos
    TRINTA_MESES = "30 meses"  # 2 anos e meio
    TRINTA_SEIS_MESES = "36 meses"  # 3 anos
    QUARENTA_DOIS_MESES = "42 meses"  # 3 anos e meio


class Sexo(Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    grupo = models.ForeignKey(
        "GrupoUsf",
        on_delete=models.CASCADE,
        related_name="profissionais",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"[{self.id}] - {self.name}"


class Crianca(models.Model):
    nomeDaCrianca = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    sexo = models.CharField(
        max_length=30,
        choices=[(choice.value, choice.value) for choice in Sexo],
        default="masculino",
    )
    nomeDaMae = models.CharField(max_length=150)
    cpfDaMae = models.CharField(max_length=14)
    dataNascimento = models.CharField(max_length=20)
    idadeCrianca = models.CharField(
        max_length=30, choices=[(choice.value, choice.value) for choice in Periodo]
    )
    maternidade = models.CharField(max_length=150)
    tipoDoParto = models.CharField(max_length=150)
    idadeGestacional = models.CharField(max_length=150)
    dataNascimentoMae = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.nomeDaCrianca}"


class CriancaProfissional(models.Model):
    idCrianca = models.ForeignKey(
        Crianca, on_delete=models.CASCADE, related_name="profissionais"
    )
    idProfissional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="criancas"
    )
    criadoEmDiaMesAno = models.DateField(auto_now_add=True)


class CrescimentoCrianca(models.Model):
    idCrianca = models.ForeignKey(Crianca, on_delete=models.CASCADE)
    idadeCrianca = models.CharField(
        max_length=20, choices=[(choice.value, choice.value) for choice in Periodo]
    )
    altura = models.FloatField()  # Altura em centímetros
    peso = models.FloatField()  # Peso em quilogramas
    perimetro = models.FloatField()
    imc = models.FloatField(null=True, blank=True)  # Campo para armazenar o IMC

    def calcular_imc(self):
        altura_metros = (
            self.altura / 100
        )  # Convertendo altura de centímetros para metros
        imc = self.peso / (altura_metros**2)
        return round(imc, 2)  # Arredonda o IMC para 2 casas decimais

    def save(self, *args, **kwargs):
        self.full_clean()  # Chama a função clean antes de salvar
        super(CrescimentoCrianca, self).save(*args, **kwargs)

    def clean(self):
        # Calcula o IMC antes de validar e salvar os dados no banco de dados
        self.imc = self.calcular_imc()
        super(CrescimentoCrianca, self).clean()

    def __str__(self) -> str:
        return f"[{self.id}] - {self.idCrianca}, {self.idadeCrianca}"


class Endereco(models.Model):
    logradouro = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    numero = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    municipio = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100)
    nomeUSF = models.CharField(max_length=100, default="USF")

    def __str__(self):
        return f"{self.logradouro}, {self.cep}, {self.municipio}, {self.estado}"


class GrupoUsf(models.Model):
    nome = models.CharField(max_length=180)

    # Relacionamento com USF
    usf = models.ForeignKey(
        "UnidadeSaudeFamiliar", on_delete=models.CASCADE, related_name="grupos"
    )

    def __str__(self) -> str:
        return f"[{self.id}] - {self.nome}"


class UnidadeSaudeFamiliar(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    criadoEmDiaMesAno = models.DateField(auto_now_add=True)

    # Endereço da USF
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    # idCuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    # idCrianca = models.ForeignKey(Crianca, on_delete=models.CASCADE)
    # idProfissionalDeSaude = models.ForeignKey(
    #     ProfissionalDeSaude, on_delete=models.CASCADE
    # )
    # idEndereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    # criadoEmDiaMesAno = models.DateField()
