# 🚗 EasyDrive API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.1-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descrição do Projeto

**EasyDrive** é uma API RESTful robusta e escalável para gerenciamento de **aluguel de veículos**, desenvolvida com Django Rest Framework. O sistema oferece gestão completa de usuários, clientes, veículos e aluguéis, com recursos avançados como:

- 🔐 Autenticação JWT com tokens rotativos e blacklist
- 📊 Logging centralizado em MongoDB
- 📚 Documentação interativa Swagger/OpenAPI
- 🏗️ Arquitetura modular em camadas com padrões de projeto (Repository, Null Object, Service Layer)
- 🎯 Separação de responsabilidades por domínio (accounts, auth, client, vehicle, rent)

## 🛠️ Tecnologias Utilizadas

### Backend

- **Django 5.1.1** - Framework web Python
- **Django Rest Framework 3.15.2** - API RESTful
- **PostgreSQL** - Banco de dados principal
- **MongoDB** - Armazenamento de logs de erros

### Autenticação & Segurança

- **djangorestframework-simplejwt** - Autenticação JWT
- **Token Blacklist** - Logout seguro com invalidação de tokens

### Documentação

- **drf-spectacular** - Swagger/OpenAPI 3.0

### Bibliotecas Adicionais

- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **psycopg2-binary** - Driver PostgreSQL
- **pymongo** - Driver MongoDB síncrono
- **motor** - Driver MongoDB assíncrono (para operações async)
- **django-cors-headers** - CORS para requisições cross-origin

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/RobsonFe/easydrive.git
cd easydrive
```

### 2. Criar Ambiente Virtual

```bash
python -m venv .venv
```

### 3. Ativar o Ambiente Virtual

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# PostgreSQL
NOME_DO_BANCO=easydrive
USUARIO_DO_BANCO=postgres
SENHA_DO_BANCO=admin
HOST_DO_BANCO=localhost
PORTA_DO_BANCO=5432

# MongoDB (Logs)
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_HOST=localhost
MONGO_DB_NAME=ativosdb
```

### 6. Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Criar Superusuário (Opcional)

```bash
python manage.py createsuperuser
```

### 8. Iniciar o Servidor

```bash
python manage.py runserver
```

### 9. Acessar a Aplicação

- **API:** <http://127.0.0.1:8000>
- **Admin:** <http://127.0.0.1:8000/admin>
- **Swagger:** <http://127.0.0.1:8000/api/docs/>
- **ReDoc:** <http://127.0.0.1:8000/api/schema/redoc/>

## 📚 Documentação da API

### Acesso à Documentação Interativa

- 📖 **Swagger UI:** <http://127.0.0.1:8000/api/docs/>
- 📄 **ReDoc:** <http://127.0.0.1:8000/api/schema/redoc/>
- 🔧 **Schema OpenAPI:** <http://127.0.0.1:8000/api/schema/>

---

## 🔐 Autenticação

### Obter Token JWT (Padrão DRF)

```http
POST /api/token/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "sua_senha"
}
```

**Resposta:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Renovar Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login (Sign In)

```http
POST /api/v1/login
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "sua_senha"
}
```

**Resposta:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Cadastro (Sign Up)

```http
POST /api/v1/signup
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123",
  "cpf": "12345678900",
  "address": "Rua Exemplo, 123",
  "phone": "81999999999"
}
```

**Resposta:**

```json
{
  "result": {
    "user": {
      "id": 1,
      "email": "joao@example.com",
      "name": "João Silva",
      "avatar": null
    },
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Logout (Sign Out)

```http
POST /api/v1/logout
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 🛣️ Endpoints Principais

### 👤 Usuários (Accounts)

#### Obter Dados do Usuário Autenticado

```http
GET /api/v1/user/
Authorization: Bearer {access_token}
```

**Resposta:**

```json
{
  "result": {
    "id": 1,
    "email": "joao@example.com",
    "name": "João Silva",
    "avatar": "http://127.0.0.1:8000/media/avatars/uuid.jpg"
  }
}
```

#### Atualizar Usuário

```http
PATCH /api/v1/user/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

{
  "name": "João Silva Atualizado",
  "email": "joao.novo@example.com",
  "password": "nova_senha123"
}
```

**Nota:** O campo `avatar` pode ser enviado como arquivo multipart/form-data.

---

### 👥 Clientes

#### Criar Cliente

```http
POST /api/v1/client/create/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "user": 1
}
```

**Resposta (201 Created):**

```json
{
  "message": "Cliente criado com sucesso!",
  "result": {
    "id": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
    "user": 1,
    "total_rentals": 0,
    "client_data": {
      "id": 1,
      "email": "joao@example.com",
      "name": "João Silva",
      "avatar": null
    }
  }
}
```

#### Listar Clientes

```http
GET /api/v1/client/list/
Authorization: Bearer {access_token}
```

#### Detalhes do Cliente

```http
GET /api/v1/clients/{uuid}
Authorization: Bearer {access_token}
```

#### Listar Clientes com Dados do Usuário

```http
GET /api/v1/client/user/list/
Authorization: Bearer {access_token}
```

#### Deletar Cliente

```http
DELETE /api/v1/client/delete/{uuid}
Authorization: Bearer {access_token}
```

---

### 🚗 Veículos

#### Criar Veículo

```http
POST /api/v1/vehicle/create/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "brand": "toyota",
  "model": "corolla",
  "year": 2024,
  "quantity": 5,
  "type_vehicle": "Carro",
  "description": "Veículo sedan econômico"
}
```

**Resposta (201 Created):**

```json
{
  "message": "Veículo criado com sucesso!",
  "result": {
    "id": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
    "brand": "toyota",
    "model": "corolla",
    "year": 2024,
    "quantity": 5,
    "type_vehicle": "Carro",
    "description": "Veículo sedan econômico",
    "is_available": true
  }
}
```

#### Listar Todos os Veículos

```http
GET /api/v1/vehicle/list/
Authorization: Bearer {access_token}
```

#### Listar Apenas Carros

```http
GET /api/v1/vehicle/list/car
Authorization: Bearer {access_token}
```

#### Listar Apenas Motos

```http
GET /api/v1/vehicle/list/moto
Authorization: Bearer {access_token}
```

#### Deletar Veículo

```http
DELETE /api/v1/vehicle/delete/{uuid}
Authorization: Bearer {access_token}
```

---

### 📝 Aluguéis

#### Criar Aluguel

```http
POST /api/v1/rent/create/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
  "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
  "start_date": "2024-11-26"
}
```

**Resposta (201 Created):**

```json
{
  "message": "Aluguel criado com sucesso!",
  "result": {
    "id": "5adb384a-5e82-44cc-8fd7-11e73ef2074e",
    "start_date": "26-11-2024",
    "end_date": null,
    "returned": false,
    "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
    "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e"
  }
}
```

**Nota:** Ao criar um aluguel, a quantidade do veículo é automaticamente decrementada.

#### Listar Aluguéis

```http
GET /api/v1/rent/list/
Authorization: Bearer {access_token}
```

**Resposta (200 OK):**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "15ebca20-a279-42cf-9528-94286e38b125",
      "start_date": "01-11-2024",
      "end_date": "02-11-2024",
      "returned": true,
      "client_data": {
        "id": "5191d544-20b2-47bf-885a-9f8772daf3b8",
        "user": 2,
        "total_rentals": 5,
        "client_data": {
          "id": 2,
          "email": "joao@example.com",
          "name": "João Silva",
          "avatar": null
        }
      },
      "vehicle_data": {
        "id": "be5fa173-7ee2-4137-b3ca-1a18d6726c1f",
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2023,
        "quantity": 8,
        "type_vehicle": "Carro",
        "description": "Veículo sedan econômico",
        "is_available": true
      },
      "created_at": "2024-11-01T10:00:00Z",
      "updated_at": "2024-11-02T15:30:00Z"
    }
  ]
}
```

#### Detalhes do Aluguel

```http
GET /api/v1/rent/detail/{uuid}/
Authorization: Bearer {access_token}
```

**Resposta (200 OK):**

```json
{
  "id": "15ebca20-a279-42cf-9528-94286e38b125",
  "start_date": "01-11-2024",
  "end_date": "02-11-2024",
  "returned": true,
  "client": "5191d544-20b2-47bf-885a-9f8772daf3b8",
  "vehicle": "be5fa173-7ee2-4137-b3ca-1a18d6726c1f",
  "client_data": {
    "id": "5191d544-20b2-47bf-885a-9f8772daf3b8",
    "user": 2,
    "total_rentals": 5,
    "client_data": {
      "id": 2,
      "email": "joao@example.com",
      "name": "João Silva",
      "avatar": null
    }
  },
  "vehicle_data": {
    "id": "be5fa173-7ee2-4137-b3ca-1a18d6726c1f",
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2023,
    "quantity": 8,
    "type_vehicle": "Carro",
    "description": "Veículo sedan econômico",
    "is_available": true
  },
  "created_at": "2024-11-01T10:00:00Z",
  "updated_at": "2024-11-02T15:30:00Z"
}
```

#### Finalizar Aluguel (Devolução)

```http
PATCH /api/v1/rent/update/{uuid}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "end_date": "2024-11-30"
}
```

**Resposta (200 OK):**

```json
{
  "message": "Baixar no aluguel realizado com sucesso!",
  "result": {
    "id": "5adb384a-5e82-44cc-8fd7-11e73ef2074e",
    "start_date": "26-11-2024",
    "end_date": "30-11-2024",
    "returned": true,
    "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
    "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
    "client_data": {
      "id": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
      "user": 1,
      "total_rentals": 1,
      "client_data": {
        "id": 1,
        "email": "joao@example.com",
        "name": "João Silva",
        "avatar": null
      }
    },
    "vehicle_data": {
      "id": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
      "brand": "Toyota",
      "model": "Corolla",
      "year": 2024,
      "quantity": 5,
      "type_vehicle": "Carro",
      "description": "Veículo sedan econômico",
      "is_available": true
    },
    "created_at": "2024-11-26T10:00:00Z",
    "updated_at": "2024-11-30T15:30:00Z"
  }
}
```

**Nota:** Ao finalizar um aluguel, a quantidade do veículo é automaticamente incrementada.

#### Deletar Aluguel

```http
DELETE /api/v1/rent/delete/{uuid}
Authorization: Bearer {access_token}
```

---

## 🏗️ Arquitetura do Projeto

```
easydrive/
├── api/
│   ├── accounts/              # Módulo de Contas (Usuários)
│   │   ├── models.py          # Modelo User (AbstractBaseUser)
│   │   ├── serializer.py     # Serializers de usuário
│   │   ├── views.py           # Views de usuário
│   │   ├── service.py         # Camada de serviço (UserService)
│   │   ├── validation.py      # Validações customizadas
│   │   └── urls.py            # URLs do módulo accounts
│   ├── auth/                  # Módulo de Autenticação
│   │   ├── views.py           # SignInView, SignUpView, SignOutView
│   │   ├── service.py         # AuthenticationService
│   │   ├── validations.py     # Validações de autenticação
│   │   ├── types.py           # Type hints (TypedDict)
│   │   └── urls.py            # URLs do módulo auth
│   ├── client/                # Módulo de Clientes
│   │   ├── models.py          # Modelo Client
│   │   ├── serializer.py      # Serializers de cliente
│   │   ├── views.py           # Views de cliente
│   │   └── urls.py            # URLs do módulo client
│   ├── vehicle/               # Módulo de Veículos
│   │   ├── models.py          # Modelo Vehicle e TypeVehicle
│   │   ├── serializer.py      # Serializers de veículo
│   │   ├── views.py           # Views de veículo
│   │   └── urls.py            # URLs do módulo vehicle
│   ├── rent/                  # Módulo de Aluguéis
│   │   ├── models.py          # Modelo Rental
│   │   ├── serializer.py      # Serializers de aluguel
│   │   ├── views.py           # Views de aluguel
│   │   └── urls.py            # URLs do módulo rent
│   ├── config/
│   │   └── mongodb/           # Configurações MongoDB
│   │       ├── connection.py  # Handler síncrono + Null Object Pattern
│   │       └── async_connection.py  # Handler assíncrono
│   ├── middleware/            # Middleware customizado
│   │   └── middlewares.py    # LogErroMiddleware
│   ├── repositories/         # Repository Pattern
│   │   ├── mongo_adapter.py   # Adapter síncrono (PyMongo)
│   │   └── async_mongo_adapter.py  # Adapter assíncrono (Motor)
│   ├── swagger/               # Mixins Swagger
│   │   └── user_mixin.py     # UserCreateSwaggerMixin
│   ├── utils/                 # Utilitários
│   │   └── allowed_tags.py   # Hook para filtrar endpoints no Swagger
│   ├── exceptions.py          # Exceções customizadas
│   └── apps.py                # Configuração do app principal
├── core/
│   ├── settings.py            # Configurações Django
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # Configuração WSGI
├── .env                       # Variáveis de ambiente
├── .gitignore
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```

---

## 🎨 Padrões de Projeto

### Repository Pattern

Abstração para acesso ao MongoDB:

- `MongoAdapter` (síncrono) - `api/repositories/mongo_adapter.py`
- `AsyncMongoAdapter` (assíncrono) - `api/repositories/async_mongo_adapter.py`

**Métodos disponíveis:**
- `find_one()`, `find_many()` - Busca de documentos
- `insert_one()`, `insert_many()` - Inserção de documentos
- `update_one()`, `update_many()` - Atualização de documentos
- `delete_one()`, `delete_many()` - Deleção de documentos
- `aggregate()` - Agregações MongoDB
- `count_documents()` - Contagem de documentos

### Null Object Pattern

Resiliência para falhas de conexão MongoDB:

- `NullCollection` - Implementação nula de collection
- `NullDBConnection` - Implementação nula de conexão
- `AsyncNullCollection` - Versão assíncrona
- `AsyncNullDBConnection` - Versão assíncrona

Quando não há conexão com MongoDB, o sistema continua funcionando sem erros, retornando valores seguros (None, listas vazias).

### Service Layer Pattern

Camada de serviço para lógica de negócio:

- `UserService` - `api/accounts/service.py` (gerenciamento de avatar)
- `AuthenticationService` - `api/auth/service.py` (signin/signup)

---

## 🔧 Funcionalidades Avançadas

### 1. Logging Automático

Middleware `LogErroMiddleware` captura automaticamente:

- Erros HTTP (status >= 400)
- Exceções não tratadas
- Salva logs no MongoDB com sanitização de dados sensíveis

**Sanitização automática:**
- Remove: `password`, `senha`, `token`, `apikey`, `secret`, `access_token`, `refresh_token`, etc.
- Substitui por `"********"` nos logs

### 2. Validações Customizadas

- Email único por usuário
- CPF único por usuário
- Validação de disponibilidade de veículos
- Validação de formato de avatar (JPEG/PNG)

### 3. Gestão de Estoque

- Decremento automático ao criar aluguel
- Incremento automático na devolução
- Flag `is_available` atualizado automaticamente no método `save()` do modelo

### 4. Autenticação JWT

- Tokens rotativos com refresh token
- Blacklist habilitado para logout seguro
- Access token válido por 24 horas
- Refresh token válido por 8 dias

### 5. Relacionamentos e Otimizações de Performance

O módulo `api.rent` utiliza relacionamentos ForeignKey para acessar dados de `Client` e `Vehicle`:

**Relacionamentos:**
- `Rental.client` → `Client` (ForeignKey com `related_name='rentals'`)
- `Rental.vehicle` → `Vehicle` (ForeignKey com `related_name='rentals'`)
- `Client.user` → `User` (OneToOneField)
- Cadeia de relacionamentos: `Rental → Client → User`

**Otimizações de Performance:**
- Todas as views de listagem usam `select_related('client__user', 'vehicle')` para evitar N+1 queries
- Serializers aninhados (`RentListSerializer`, `RentDetailSerializer`) utilizam relacionamentos para incluir dados completos
- Validações de negócio (disponibilidade, datas) implementadas nos serializers

**Exemplo de Otimização:**
```python
def get_queryset(self):
    """
    Retorna queryset otimizado com select_related.
    """
    return Rental.objects.select_related(
        'client__user',  # Otimiza acesso a Client e User
        'vehicle'        # Otimiza acesso a Vehicle
    ).order_by('-start_date')
```

**Validações Automáticas:**
- Data de início não pode ser no passado
- Veículo deve estar disponível (quantity > 0)
- Data de devolução não pode ser anterior à data de início
- Aluguel já devolvido não pode ser atualizado

---

## 🧪 Testes

```bash
python manage.py test
```

---

## 📦 Dependências Principais

Veja o arquivo completo em [requirements.txt](requirements.txt)

```
Django==5.1.1
djangorestframework==3.15.2
djangorestframework-simplejwt==5.4.0
psycopg2-binary==2.9.10
pymongo==4.11.2
drf-spectacular==0.28.0
python-dotenv==1.0.1
django-cors-headers==4.4.0
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork o projeto
2. Criar uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Robson Ferreira**

- GitHub: [@RobsonFe](https://github.com/RobsonFe)
- Email: <robsonfe.dev@gmail.com>

---

## 📞 Suporte

Para dúvidas ou suporte, abra uma [issue](https://github.com/RobsonFe/easydrive/issues) no GitHub.
