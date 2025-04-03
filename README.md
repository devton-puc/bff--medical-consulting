# BFF Medical Consulting (Customer) - Projeto MVP

Projeto MVP para disciplina **Desenvolvimento Full Stack Avançado** 

Este projeto é uma aplicação back-end for front-end desenvolvida com Python Utilizando Flask. O objetivo é criar um serviço para interagir com front-end permitindo adicionar, editar, excluir e visualizar informações dos Pacientes.

### Modelo de Arquitetura:

1. **Camada de Frontend (React)**:
   - Aplicação `react web--medical-consulting` é responsável por interagir com os e fazer a integração com a API.

2. **Camada de BFF (Backend For Frontend)**:
   - A API `bff--medical-consulting` utiliza arquitetura bff (backend for front end), processando as solicitações e coordenando as interações entre a aplicação e os serviços backend.

3. **O BFF se conecta as seguintes apis**:
   - `api--patient`: Gerencia os dados dos pacientes (ex.: informações de cadastro, histórico médico).
   - `api--appointment`: Lida com agendamentos e consulta a serviços externos.
   - `viacep (externa)`: Serviço externo para obter endereços com base nos CEPs fornecidos.

4. **Integração com Serviço Externo**:
   - A API `api--appointment` conecta-se à `API do Google Gemini`, que retorna os medicamentos recomendados com base nos sintomas.
   

## Funcionalidades

- **Cadastro de Pacientes**: Permite adicionar novos Pacientes com informações como nome, email, telefone, idade e endereço.
- **Alteração de Pacientes**: Permite alterar as informações dos Pacientes existentes.
- **Busca de Pacientes**: Busca as informações dos Pacientes existentes para edição.
- **Exclusão de Pacientes**: Permite excluir Pacientes do banco de dados.
- **Visualização de Pacientes**: Lista todos os Pacientes cadastrados filtrando por nome.
- **Cadastro de Consultas médicas**: Permite adicionar novos Consultas médicass com informações como id do paciente, crm do medico, data do atendimento e sintomas.
- **Alteração de Consultas médicas**: Permite alterar as informações dos Consultas médicas existentes.
- **Busca de Consultas médicas**: Busca as informações dos Consultas existentes para edição.
- **Exclusão de Consultas médicas**: Permite excluir Consultas médicas do banco de dados.
- **Visualização de Consultas médicas**: Lista todos os Consultas filtrando por id do paciente.
- **Busca de Cep**: Permite Consultar os dados de endereço, informando o CEP.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal utilizada no projeto.
- **Flask**: Framework para desenvolvimento da API.
- **SQLite**: Banco de dados utilizado para armazenar os dados dos Pacientes e endereços.
- **Pydantic**: Biblioteca para validação de dados e definição de esquemas.
- **flask-openapi3**: Biblioteca para documentação da API.

## Instalando o projeto

Será necessário ter o python instalado. A versão indicada é a 3.12.6 e a do pip é a 24.2. 
Após clonar o repositório, é necessário ir ao diretório raiz do projeto, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Instale o venv:

```
 python -m venv .venv 
```

Ative o Venv com o comando abaixo:

```
 .venv\Scripts\activate
```

Assim que ativado, instale as depedencias.

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Crie um arquivo .env e coloque o o conteúdo:

```
VIACEP_API_URL=https://viacep.com.br/ws
API_PATIENT_URL=http://localhost:3000
API_APPOINTMENT_URL=http://localhost:4000
```

## Rodando a aplicação

Execute os projetos api--patient e api--appointment

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

## Rodando Testes

Esta aplicação possui testes unitários. Para rodar os testes, basta instalar
o projeto e em seguida executar o comando abaixo:

```
(env)$ pytest
```

## Rodando via Docker (Precisa ter o Docker Instalado)

Importante: Execute o projeto api--patient e api--apointment via docker antes de executar esta api. 

Neste cenário, precisa ter iniciado o mysql em um dos docker-compose contido
nos projetos indicados acima.

Execute o comando para gerar a imagem via Docker

```
docker build -t bff--medical-consulting .
```

Para executar o container, rode o comando abaixo:

```
docker run --name bff--medical-consulting \
    --network api-backend \  
    -p 5000:5000 \
    -e VIACEP_API_URL=<URL DO VIA CEP> \
    -e API_PATIENT_URL=<URL DA API-PATIENT> \
    -e API_APPOINTMENT_URL=<URL DA API-APPOINTMENT> \

    bff--medical-consulting:latest
```

# Rodando via docker-compose:

Configure a chave da api key do gemini no service api-apointment no docker-compose.yaml:

```
    environment:
        ...
      - GEMINI_TOKEN=<SUA API KEY>cker-compose
```

Para rodar via docker-compose, efetue um comando abaixo:

```
docker compose up
```

Este comando executa todas as aplicações. 

# Importante:

- É necessário que os projetos api--patient e api--appointment estejam no mesmo diretório. 
- Não rode o docker-compose.yaml do projeto api--patient e(ou) api--appointment, para evitar conflito de portas do mysql.


## Documentação OpenAPI

A documentação OpenAPI da API está disponível em:

- **URL**: `[http://localhost:5000/openapi/swagger](http://localhost:5000/openapi/swagger)`


## POSTMAN

Para executar, importe as collections do postman 

```
bff--medical-consulting.postman_collection.json
```

## Autor
Clayton Morais de Oliveira
