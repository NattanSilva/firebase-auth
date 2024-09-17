# AUTH API with FIREBASE

### Dependências:

1. <a href="https://python.org.br/instalacao-windows/" target="_blank">Python3</a>
2. <a href="https://www.postgresql.org/download/" target="_blank">PostgreSQL</a>

### 1 - Crie seu ambiente virtual:

```shell
python -m venv venv
```

### 2 - Ative seu ambiente virtal:

```shell
# linux:
source venv/bin/activate

# windows (powershell):
.\venv\Scripts\activate

# windows (git bash):
source venv/Scripts/activate
```

### 3 - Instale as dependências do projeto:

```shell
pip install -r requirements.txt
```

### 4 - Crie uma nova Database local:

<p>Para executar o projeto localmente crie um banco de dados separado apenas para esta aplicação.</p>

```shell
# Acesse a shell do postgres no seu terminal com seu usuario e senha:
psql -U seu_usuario
# Crie uma nova Database com o comando:
CREATE DATABASE nome_do_seu_novo_banco_de_dados;
# Verifique se o Database foi criada corretamente:
\l
# Caso sua nova Database apareça na listagem de Databases tudo ocorreu com sucesso!
# Para sair da shell do postgres basta digitar o comando abaixo e pressionar enter:
\quit
```

### 5 - Configure sua conexão com o banco de dados:

<p>Para esta etapa copie o arquivo <code>.env.example</code> e mude o nome da cópia para <code>.env</code> e preencha os campos com as informações de acordo com as instruções a seguir.</p>

```shell
# Faça o download das credenciais do firebase e renomeie para cred.json
FIREBASE_CRED="caminho para as credencias baixadas"

# postgres configurations
PG_DATABASE=
PG_USER=
PG_PASSWORD=
PG_HOST=
PG_PORT=
# Firebase configurations
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_DATABASE_URL=
FIREBASE_PROJECT_ID=
FIREBASE_STORAGE_BUCKET=
FIREBASE_MESSAGING_SENDER_ID=
FIREBASE_APP_ID=

# Firebase Credentials
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=
FIREBASE_CLIENT_ID=
FIREBASE_CLIENT_CERT_URL=
```

### 6 - Gere as migrações:

```shell
python manage.py makemigrations
```

### 7 - Execute as migrações:

```shell
python manage.py migrate
```

### 8 - Inicie o servidor:

```shell
python manage.py runserver
```
