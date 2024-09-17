import os

import dotenv

dotenv.load_dotenv()


def validate_env_variables(lista_de_variaveis):
    for variavel in lista_de_variaveis:
        if not os.environ.get(variavel) or os.environ.get(variavel) == "":
            raise KeyError(f"{variavel} variable does not exist on .env file!")


def dict_list_find(lista: list[dict], key: str, value) -> dict | None:
    result: dict | None = None
    for data in lista:
        if data[key] == value:
            result = data

    return result


def ordenar_dados_crescimento_crianca(lista_dados: list[dict]) -> list[dict]:
    lista_ordenada = []

    if len(lista_dados) == 1:
        return lista_dados

    if dict_list_find(lista_dados, "idadeCrianca", "primeira semana"):
        lista_ordenada.append(
            dict_list_find(lista_dados, "idadeCrianca", "primeira semana")
        )

        lista_dados.remove(
            dict_list_find(lista_dados, "idadeCrianca", "primeira semana")
        )

    for item in lista_dados:
        menor = int(item["idadeCrianca"].split(" ")[0])
        menor_dado = item

        for dado in lista_dados:
            if int(item["idadeCrianca"].split(" ")[0]) < menor:
                menor = int(item["idadeCrianca"].split(" ")[0])
                menor_dado = dado

        if not menor_dado in lista_ordenada:
            lista_ordenada.append(menor_dado)

    return lista_ordenada
