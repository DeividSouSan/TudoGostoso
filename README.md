# TudoGostoso API

O TudoGostoso é uma API de uma sistema de compartilhamento de receitas. Por meio deste, os usuários podem autenticar-se recebendo permissão para ver, criar e deletar receitas.
## Objetivo

O objetivo do projeto foi aprender mais sobre o desenvolvimento de APIs utilizando o Python com FastAPI + MySQL.

## Funcionalidades

- [x] Cadastro de Usuários no Banco de Dados
- [x] Autenticação de Usuários (Login)
- [x] Autorização de Usuário por meio de Tokens JWT 
- [x] Sistema de Gerenciamento de Receitas (CRUD)

## Rotas

![image](https://github.com/user-attachments/assets/8c6d07ca-2e07-443b-8ae6-03688d090b08)


## Como Rodar o Projeto?

### Clonando

Primeiro clone o repositório. Isso pode ser feito baixando-o ou utilizando o comando:

```
git clone git@github.com:DeividSouSan/TudoGostoso.git
```

Utilizando sua IDE ou Editor de Texto, abra o projeto. Se estiver pelo terminal acesse a pasta onde baixou ou clonou o projeto e escreva: 

```
cd TudoGostoso
```

### Ambiente Virtual

Dentro da pasta do projeto, inicie um ambiente virtual. É recomendado instalar as bibliotecas em um ambiente virtual para evitar conflitos de versões com os pacotes instalados globalmente. Pelo terminal, crie um ambiente virtual utilizando:
```
python3 -m venv <nome_do_ambiente_virtual>
```

Geralmente o nome utilizado é .venv, mas isso é de sua escolha.

Para ativar o ambiente virutal no linux:

```
source .venv/bin/activate
```

Ou

```
. .venv/bin/activate
```

Para desativa-lo:

```
deactivate
```

No windows:
```
.venv/Scripts/activate
```

Para desativa-lo:

```
.venv/Scripts/deactivate
```

### Bibliotecas

Utilizei as seguintes bibliotecas para realização do projeto:

- FastAPI (Servidor e Rotas)
- Python Dotenv (Variáveis de Ambiente)
- PyMySQL (Driver de Conexão para o MySQL)
- SQLAlchemy (Object Relational Mapper)
- bcrypt (Hash da Senha)
- pydantic (Validação de Dados)
- alembic (Migrações do Banco de Dados)
- python-jose (Lidar com Tokens JWT)
- pre-commit (Formatar o código de forma padronizada)
- smtplib (Envio de emails)

Para baixar as bibliotecas do Python escreva no terminal (antes verifique se o ambiente virtual está ativado):

```bash
pip install -r requirements.txt
```

Assim todas as dependencias que estão dentro do arquivo `requirements.txt` serão baixadas para o seu ambiente virtual.

### Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

```
DATABASE_URL = 'mysql+pymysql://<<username>>:<<senha>>!@localhost/<<nome_banco_de_dados>>'
SECRET_KEY  = '<<chave_secreta_aleatória>>'
ALGORITHM = 'HS256'
EXPIRATION_MINUTES = 30

SENDER_EMAIL_ADDRESS = "<<email>>"
SENDER_EMAIL_PASSWORD = "<<senha>>"
```
Alguns adendos:
1. Você deve criar o banco de dados por meio de um SGBD para poder escrever o `DATABASE_URL`.
2. A `SECRET_KEY` deve conter 32 digitos.
3. Para conseguir enviar emails é necessário configurar sua conta do google para conseguir enviar emails SMTP.

### Banco de Dados

O banco de dados utilizado para essa aplicação foi o MySQL. É necessário que o banco de dados seja criado manualmente pelo SGBD para poder ser inserido na variável `DATABASE_ULR`.

### Finalmente Rodando a Aplicação

Para rodar a aplicação escreva enter na para `/api` e rode:
```
fastapi run
```
