# 🚗 EasyDrive API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.1-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descrição do Projeto

**EasyDrive** é uma API RESTful robusta e escalável para gerenciamento de **aluguel de veículos**, desenvolvida com Django Rest Framework. O sistema oferece gestão completa de usuários, clientes, veículos e aluguéis, com recursos avançados como:

- 🔐 Autenticação JWT com tokens rotativos
- 📊 Logging centralizado em MongoDB
- 🔔 Notificações em tempo real via WebSocket
- 📚 Documentação interativa Swagger/OpenAPI
- 🏗️ Arquitetura em camadas com padrões de projeto (Builder, Repository, Null Object)

## 🛠️ Tecnologias Utilizadas

### Backend

- **Django 5.1.1** - Framework web Python
- **Django Rest Framework 3.15.2** - API RESTful
- **PostgreSQL** - Banco de dados principal
- **MongoDB** - Armazenamento de logs
- **Redis** - Cache e gerenciamento de canais WebSocket

### Autenticação & Segurança

- **djangorestframework-simplejwt** - Autenticação JWT
- **Token Blacklist** - Logout seguro

### Comunicação em Tempo Real

- **Django Channels 4.2.2** - WebSocket
- **Daphne** - Servidor ASGI
- **channels-redis** - Backend de canais

### Documentação

- **drf-spectacular** - Swagger/OpenAPI 3.0

### Bibliotecas Adicionais

- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **psycopg2-binary** - Driver PostgreSQL
- **pymongo** - Driver MongoDB síncrono
- **motor** - Driver MongoDB assíncrono


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

**Servidor HTTP (Desenvolvimento):**

```bash
python manage.py runserver
```

**Servidor ASGI (WebSocket + HTTP):**

```bash
daphne -b 0.0.0.0 -p 8000 core.asgi:application
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

### Obter Token JWT

```http
POST /api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
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

### Login Customizado

```http
POST /api/v1/login/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

### Logout

```http
POST /api/v1/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```


---

## 🛣️ Endpoints Principais

### 👤 Usuários

#### Criar Usuário (Público)

```http
POST /api/v1/user/create/
Content-Type: application/json

{
  "username": "johndoe",
  "name": "John Doe",
  "email": "john@example.com",
  "password": "senha123",
  "cpf": "12345678900",
  "address": "Rua Exemplo, 123",
  "phone": "81999999999"
}
```

#### Listar Usuários

```http
GET /api/v1/user/list/
Authorization: Bearer {access_token}
```

#### Atualizar Usuário

```http
PATCH /api/v1/user/update/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "John Updated",
  "phone": "81988888888"
}
```

#### Deletar Usuário

```http
DELETE /api/v1/delete/user/{id}
Authorization: Bearer {access_token}
```

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

#### Deletar Cliente

```http
DELETE /api/v1/delete/client/{uuid}
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
DELETE /api/v1/delete/vehicle/{uuid}
Authorization: Bearer {access_token}
```


---

### **📝 Aluguéis**

#### **Criar Aluguel**
```http
POST /api/v1/rent/create/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
  "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
  "start_date": "2024-11-26"
  }
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

#### **Listar Aluguéis**
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
      "client_data": {
        "id": "5191d544-20b2-47bf-885a-9f8772daf3b8",
        "total_rentals": 5,
        "user_data": {
          "id": 2,
          "username": "RobsonFe",
          "name": "Robson Ferreira da Silva",
          "email": "robson12ferreira@gmail.com"
        }
      },
      "vehicle_data": {
        "id": "be5fa173-7ee2-4137-b3ca-1a18d6726c1f",
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2023,
        "quantity": 8,
        "is_available": true
      }
    }
  ]
}
```

#### **Finalizar Aluguel (Devolução)**
```http
PATCH /api/v1/update/rent/{uuid}
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
    "end_date": "30-11-2024",
    "returned": true,
    "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
    "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e"
  }
}
```

#### **Deletar Aluguel**
```http
DELETE /api/v1/delete/rent/{uuid}
Authorization: Bearer {access_token}
```

---

### **📊 Logs (MongoDB)**

#### **Listar Logs de Erros**
```http
GET /api/v1/mongo/list/
Authorization: Bearer {access_token}
```

---

## 🔔 WebSocket - Notificações em Tempo Real

### Conectar ao WebSocket

```javascript
const socket = new WebSocket('ws://127.0.0.1:8000/ws/vehicle/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Notificação:', data);
};

socket.onopen = function() {
    console.log('WebSocket conectado!');
};

socket.onclose = function() {
    console.log('WebSocket desconectado!');
};
```

### Evento de Aluguel

Quando um veículo é alugado, uma notificação é enviada para todos os clientes conectados:

```json
{
  "vehicle_brand": "Toyota",
  "vehicle_model": "Corolla",
  "vehicle_year": 2024,
  "vehicle_quantity": 4,
  "vehicle_type_vehicle": "Carro",
  "vehicle_description": "Veículo sedan econômico",
  "status": "alugado",
  "timestamp": "2024-11-04T15:30:45.123456"
}
```


---

## 🏗️ Arquitetura do Projeto

```
easydrive/
├── api/
│   ├── build/               # Builders (Padrão Builder)
│   │   ├── user_builder.py
│   │   ├── client_builder.py
│   │   ├── vehicle_builder.py
│   │   └── rent_builder.py
│   ├── config/
│   │   └── mongodb/         # Configurações MongoDB
│   │       ├── connection.py
│   │       └── async_connection.py
│   ├── exepctions/
│   │   └── constants/       # Validações customizadas
│   ├── middleware/          # Middlewares customizados
│   │   └── middlewares.py
│   ├── migrations/          # Migrações Django
│   ├── model/               # Models Django
│   │   ├── user_model.py
│   │   ├── client_model.py
│   │   ├── vehicle_model.py
│   │   └── rent_model.py
│   ├── repositories/        # Repository Pattern
│   │   ├── mongo_adapter.py
│   │   └── async_mongo_adapter.py
│   ├── serializers/         # DRF Serializers
│   │   ├── user_serializer.py
│   │   ├── client_serializer.py
│   │   └── authentication_serializer.py
│   ├── swagger/             # Mixins Swagger
│   │   └── user_mixin.py
│   ├── tests/               # Testes automatizados
│   ├── utils/               # Utilitários
│   ├── views/               # Views DRF
│   │   ├── views.py
│   │   └── authentication_view.py
│   ├── consumers.py         # WebSocket Consumers
│   ├── routing.py           # Rotas WebSocket
│   └── urls.py              # URLs da API
├── core/
│   ├── asgi.py              # Configuração ASGI
│   ├── settings.py          # Configurações Django
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # Configuração WSGI
├── .env                     # Variáveis de ambiente
├── .gitignore
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```

---

## 🎨 Padrões de Projeto

### Builder Pattern

Utilizado para construção fluente de objetos:

- `UserBuilder`
- `ClientBuilder`
- `VehicleBuilder`
- `RentBuilder`

### Repository Pattern

Abstração para acesso ao MongoDB:

- `MongoAdapter` (síncrono)
- `AsyncMongoAdapter` (assíncrono)

### Null Object Pattern

Resiliência para falhas de conexão MongoDB:

- `NullCollection`
- `NullDBConnection`

---

## 🔧 Funcionalidades Avançadas

### 1. Logging Automático

Middleware `LogErroMiddleware` captura automaticamente:

- Erros HTTP (status >= 400)
- Exceções não tratadas
- Salva logs no MongoDB com sanitização de dados sensíveis

### 2. Validações Customizadas

- Data de início não pode ser no passado
- CPF e email únicos
- Validação de disponibilidade de veículos

### 3. Gestão de Estoque

- Decremento automático ao criar aluguel
- Incremento automático na devolução
- Flag `is_available` atualizado automaticamente

### 4. Notificações em Tempo Real

- WebSocket com Django Channels
- Broadcast de eventos de aluguel
- Suporte a múltiplos clientes conectados


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
channels==4.2.2
daphne==4.1.2
redis==5.2.1
drf-spectacular==0.28.0
python-dotenv==1.0.1
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



