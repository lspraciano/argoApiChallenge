# Desafio Argo - API

O desafio pedia para desenvolvermos uma API atendendo alguns requisitos,
dentre eles, ela deveria ser desenvolvida usando DJANGO. Vou contar um spoiler...
por não ter prática com este framework e ter aproximadamente 48 horas, resolvi
desenvolver usando FASTAPI. Espero que desfrutem deste trabalho.

## 📦 Status Do Projeto
- Em Desenvolvimento

## 📌 Versão Atual
- 1.00

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação
na sua máquina local.

### 📋 Pré-requisitos

- Python 3.10.2 +
- Poetry
- Git
- PostgreSQL

### 🔧 Instalação

1. Clonamos o repositório através do comando:

    ```
    git clone https://github.com/lspraciano/argoApiChallenge.git
    ```

2. No diretório raiz do projeto iremos rodar o comando:

    ```
    poetry install
    ```

3. No diretório "configuration" você deverá criar um arquivo com nome ".secrets.toml".
    O que é esse arquivo? Este é o arquivo destinado às variáveis de ambiente mais
    sensíveis do projeto. Abaixo temos o conteúdo obrigatório e a explicação dos
    campos.

    ```
    [default]
    JWT_SECRET = "insira_uma_chave_segura"
    ALGORITHM = "HS256"
    ONE_ADMIN_USER_NAME = "Nome do Usuáio Administrador 1"
    ONE_ADMIN_USER_EMAIL = "Email do Usuáio Administrador 1"
    ONE_ADMIN_PASSWORD = "Senha Inicial do Usuáio Administrador 1"
    TWO_ADMIN_USER_NAME = "Nome do Usuáio Administrador 2"
    TWO_ADMIN_USER_EMAIL = "Email do Usuáio Administrador 2"
    TWO_ADMIN_PASSWORD = "Senha Inicial do Usuáio Administrador 2"
    MAIL_USERNAME = "email para ser manipulado pela aplicação"
    MAIL_PASSWORD = "senha do email da aplicação"
    MAIL_FROM = "email para ser manipulado pela aplicação"
    MAIL_PORT = 587
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_FROM_NAME = "ARGO API"
    
    
    [production]
    DB_URL = "postgresql+asyncpg://postgres:SENHA_DO_BANCO@ENDERÇO_DO_BANCO/dbArgoApiProd"
    
    [development]
    DB_URL = "postgresql+asyncpg://postgres:SENHA_DO_BANCO@ENDERÇO_DO_BANCO/dbArgoApiDev"
    
    [testing]
    DB_URL = "postgresql+asyncpg://postgres:SENHA_DO_BANCO@ENDERÇO_DO_BANCO/dbArgoApiTest"
    ```
   
4. Esta aplicação poderá rodar em 3 modos, production, development e testing. Como
    realizamos a troca entre estes modos? Você deve exportar a variável de ambiente
    "ARGOAPI_APP_RUNNING_MODE" e passar um destes modos. Por exemplo:
    <br></br>

   No Windows: 
      ````
           setx ARGOAPI_APP_RUNNING_MODE "production"
      ````
   No Linux: 
      ````
           export ARGOAPI_APP_RUNNING_MODE=production
      ````   

    Observação: Caso esteja usando alguma IDE, sugiro que após exportar
    a variável de ambiente "ARGOAPI_APP_RUNNING_MODE" você reinicie a IDE.   

   <br></br>
    
5. Agora vamos iniciar a aplicação? Para isso vamos rodar os seguintes
   comandos:

    Iniciamos o ambiente virtual
      ````
           poetry shell
      ````    
    Rodamos a aplicação
      ````
           uvicorn app.main:app --host 0.0.0.0 --port 8000
      ````
   
6. Que tal consultar a documentação das rotas?
    Com a aplicação rodando você pode abrir seu navegador e digitar o 
    endereço abaixo
      ````
           http://127.0.0.1:8000/docs
      ````