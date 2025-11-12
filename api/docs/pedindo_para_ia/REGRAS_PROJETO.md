# Memória de Regras do Projeto EasyDrive

> **Fonte:** `.github/copilot-instructions.md` (linhas 1-305)
> **Última atualização:** Atualizado após refatoração modular

---

## 🎯 Visão Geral

**Projeto:** API RESTful para gerenciamento de aluguel de veículos  
**Stack:** Python 3.x, Django 5.1.1, DRF 3.15.2, PostgreSQL, MongoDB (logs)

---

## 🔴 REGRAS FUNDAMENTAIS (OBRIGATÓRIAS)

### 1. Comentários e Documentação
- ❌ **NUNCA usar comentários inline** (`# comentário`)
- ✅ **SEMPRE usar docstrings** (Google Style ou NumPy Style)
- ✅ Docstrings em todas as classes e métodos públicos
- ✅ Incluir Attributes, Args, Returns, Raises nas docstrings

### 2. Código Limpo
- ✅ Seguir PEP 8 e convenções do Django
- ✅ Código claro, conciso e autoexplicativo
- ✅ Nomes descritivos de variáveis e funções
- ❌ Evitar verbosidade desnecessária

### 3. Performance - N+1 Queries
- ✅ **EVITAR N+1 QUERIES A TODO CUSTO**
- ✅ Usar `select_related()` para ForeignKeys
- ✅ Usar `prefetch_related()` para ManyToMany e reverse FKs
- ✅ Otimizar querysets em métodos `get_queryset()`

---

## 📁 Estrutura de Diretórios (Arquitetura Modular)

```
api/
├── accounts/          # Módulo de Contas (Usuários)
│   ├── models.py      # User (AbstractBaseUser)
│   ├── serializer.py  # UserSerializer, UserUpdateSerializer
│   ├── views.py       # UserView (GET, PATCH)
│   ├── service.py     # UserService (lógica de negócio)
│   ├── validation.py  # UserValidatorMixin
│   └── urls.py        # URLs do módulo
├── auth/              # Módulo de Autenticação
│   ├── views.py       # SignInView, SignUpView, SignOutView
│   ├── service.py     # AuthenticationService
│   ├── validations.py # SiginValidationMixin
│   ├── types.py       # Type hints (TypedDict)
│   └── urls.py        # URLs do módulo
├── client/            # Módulo de Clientes
│   ├── models.py      # Client (UUID PK)
│   ├── serializer.py  # ClientSerializer, ClientDetailsSerializer
│   ├── views.py       # Views CRUD de cliente
│   └── urls.py        # URLs do módulo
├── vehicle/           # Módulo de Veículos
│   ├── models.py      # Vehicle, TypeVehicle (UUID PK)
│   ├── serializer.py  # VehicleSerializer
│   ├── views.py       # Views CRUD de veículo
│   └── urls.py        # URLs do módulo
├── rent/              # Módulo de Aluguéis
│   ├── models.py      # Rental (UUID PK)
│   ├── serializer.py  # RentSerializer, RentListSerializer
│   ├── views.py       # Views CRUD de aluguel
│   └── urls.py        # URLs do módulo
├── config/
│   └── mongodb/       # Configurações MongoDB
│       ├── connection.py      # Handler síncrono + Null Object
│       └── async_connection.py  # Handler assíncrono
├── repositories/      # Repository Pattern
│   ├── mongo_adapter.py       # Adapter síncrono
│   └── async_mongo_adapter.py # Adapter assíncrono
├── middleware/        # Middleware customizado
│   └── middlewares.py # LogErroMiddleware
├── swagger/           # Mixins Swagger
│   └── user_mixin.py  # UserCreateSwaggerMixin
├── utils/             # Utilitários
│   └── allowed_tags.py # Hook para filtrar endpoints
└── exceptions.py      # Exceções customizadas
```

---

## 🏗️ Models (Django)

**Localização:** Cada módulo tem seu próprio `models.py`

**Convenções:**
- UUID como PK para models principais (exceto User que usa int)
- Incluir `created_at` e `updated_at` quando apropriado
- Implementar `__str__()` retornando representação legível
- Lógica de negócio no método `save()` quando necessário
- Docstrings obrigatórias com Attributes

**Models Principais:**
- `api.accounts.models.User` - Usuário do sistema (AbstractBaseUser)
- `api.client.models.Client` - Cliente (OneToOne com User)
- `api.vehicle.models.Vehicle` - Veículo (TypeVehicle: Carro/Moto)
- `api.rent.models.Rental` - Aluguel (FK para Client e Vehicle)

---

## 🔍 Views (DRF)

**Preferir:** `generics.CreateAPIView`, `ListAPIView`, `UpdateAPIView`, `DestroyAPIView`, `RetrieveAPIView`, `APIView`

**Permissões:**
- `AllowAny`: Apenas para signup e login
- `IsAuthenticated`: Padrão para todos os endpoints protegidos

**Estrutura Obrigatória:**
- Declarar `permission_classes` explicitamente
- Declarar `serializer_class` e `queryset`
- Usar `select_related()`/`prefetch_related()` em list views
- Sobrescrever métodos HTTP (post, get, patch, delete) para lógica customizada
- Criar objetos diretamente usando `Model.objects.create()` ou `Model.objects.create_user()`
- Retornar Response com mensagens claras

**Service Layer:**
- Usar camada de serviço para lógica de negócio complexa
- Services em `{module}/service.py`
- Exemplos: `UserService`, `AuthenticationService`

---

## 📝 Serializers (DRF)

**Usar:** `ModelSerializer` sempre que possível

**Convenções:**
- Declarar `Meta` com `model` e `fields`
- Usar `extra_kwargs` para configurações de campos
- Validações complexas no método `validate()` ou `validate_<field>()`
- Serializers aninhados para relacionamentos (read-only)
- **Validações no serializer, NÃO na view**

**Serializers Principais:**
- `UserSerializer` - Serialização de usuário (com avatar)
- `UserUpdateSerializer` - Atualização de usuário (com validação de email)
- `ClientSerializer` - Serialização de cliente (com user_data aninhado)
- `ClientDetailsSerializer` - Detalhes completos do cliente
- `VehicleSerializer` - Serialização de veículo
- `RentSerializer` - Criação de aluguel
- `RentListSerializer` - Listagem com dados aninhados (client_data, vehicle_data)
- `RentServiceUpdateSerializer` - Atualização (devolução)

---

## 💾 Repositories (MongoDB)

**Localização:** `api/repositories/`  
**Uso:** `MongoAdapter` (sync) ou `AsyncMongoAdapter` (async)

**Métodos:** `find_one`, `find_many`, `insert_one`, `update_one`, `delete_one`, `aggregate`, `count_documents`  
**Resilência:** Usa Null Object Pattern para falhas de conexão

**Exemplo de uso:**
```python
from api.repositories.mongo_adapter import MongoAdapter

mongo = MongoAdapter(collection_name="erros")
mongo.save_error(user, endpoint, method, error, payload)
```

---

## ⚡ Performance - Banco de Dados

**🚨 CRÍTICO - SEMPRE OTIMIZAR:**

```python
# ❌ ERRADO - Causa N+1 queries ao acessar client.user ou vehicle
queryset = Rental.objects.all()

# ✅ CORRETO - Otimizado com select_related
def get_queryset(self):
    """
    Retorna queryset otimizado com select_related.
    
    Returns:
        QuerySet de Rental com relacionamentos otimizados.
    """
    return Rental.objects.select_related(
        'client__user',  # Otimiza acesso a Client e User (ForeignKey -> OneToOne)
        'vehicle'        # Otimiza acesso a Vehicle (ForeignKey)
    ).order_by('-start_date')
```

**Relacionamentos no Projeto:**
- `Rental.client` → `Client` (ForeignKey com related_name='rentals')
- `Rental.vehicle` → `Vehicle` (ForeignKey com related_name='rentals')
- `Client.user` → `User` (OneToOneField)
- Cadeia: `Rental → Client → User`

**SEMPRE usar em list views:**
- `select_related()` para ForeignKeys
- `prefetch_related()` para ManyToMany e reverse ForeignKeys

---

## 🔐 Autenticação e Segurança

**JWT:** djangorestframework-simplejwt

**Endpoints:**
- `/api/token/` - Obter access/refresh tokens (padrão DRF)
- `/api/token/refresh/` - Renovar access token
- `/api/v1/login` - Login customizado (SignInView)
- `/api/v1/signup` - Cadastro de usuário (SignUpView)
- `/api/v1/logout` - Logout com blacklist (SignOutView)

**Headers:** `Authorization: Bearer <access_token>`  
**Configuração:** Tokens rotativos com blacklist habilitado
- Access token: 24 horas
- Refresh token: 8 dias

**User Model:** `api.accounts.User` (AbstractBaseUser, USERNAME_FIELD = 'email')

---

## 📚 Documentação Swagger

- Usar `@extend_schema` do drf-spectacular
- Tags: Categorizar endpoints por domínio
- Examples: Fornecer exemplos de request/response
- Filters: Usar hook `filter_endpoints_by_allowed_tags`

**Mixin disponível:**
- `UserCreateSwaggerMixin` - Documentação para criação de usuário

---

## 🔧 Middleware

**LogErroMiddleware:** Captura erros automáticos e salva no MongoDB  
**Localização:** `api/middleware/middlewares.py`

**Funcionalidades:**
- `process_request()`: Captura payload (sanitiza senhas/tokens)
- `process_exception()`: Captura exceções não tratadas → MongoDB
- `process_response()`: Captura respostas HTTP >= 400 → MongoDB

**Sanitização:**
- Remove: `password`, `senha`, `token`, `apikey`, `secret`, `access_token`, `refresh_token`, etc.
- Substitui por `"********"`

**Ordem:** Respeitar ordem no `settings.MIDDLEWARE`

---

## ✅ Checklist de Implementação

Antes de criar qualquer código, verificar:

- [ ] Docstrings em todas as classes e métodos públicos
- [ ] Sem comentários inline
- [ ] `select_related`/`prefetch_related` em list views
- [ ] Permissões explícitas nas views
- [ ] Validações no serializer, não na view
- [ ] Response com mensagens claras
- [ ] Tratamento de exceções adequado
- [ ] Código PEP 8 compliant
- [ ] Nomes descritivos e autoexplicativos
- [ ] Criar objetos diretamente (sem Builders)
- [ ] Testes automatizados para novas funcionalidades

---

## 🚀 Comandos Úteis

**Ambiente:**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

**Migrações:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Servidor:**
```bash
python manage.py runserver
```

---

## 📋 Variáveis de Ambiente (.env)

```env
# PostgreSQL
NOME_DO_BANCO=easydrive
USUARIO_DO_BANCO=postgres
SENHA_DO_BANCO=admin
HOST_DO_BANCO=localhost
PORTA_DO_BANCO=5432

# MongoDB
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_HOST=localhost
MONGO_DB_NAME=ativosdb
```

---

## ⚠️ LEMBRETES CRÍTICOS

1. **SEMPRE** usar docstrings, nunca comentários inline
2. **SEMPRE** otimizar queries com `select_related`/`prefetch_related`
3. **SEMPRE** criar objetos diretamente (Model.objects.create())
4. **SEMPRE** declarar permissões explicitamente nas views
5. **SEMPRE** fazer validações no serializer, não na view
6. **NUNCA** causar N+1 queries
7. **NUNCA** adicionar funcionalidades além do pedido
8. **SEMPRE** escrever testes automatizados para novas funcionalidades
9. **SEMPRE** usar Service Layer para lógica de negócio complexa
10. **SEMPRE** respeitar a arquitetura modular (cada domínio em seu módulo)

---

## 🏛️ Arquitetura Modular

O projeto está organizado em módulos por domínio:

1. **api.accounts** - Gerenciamento de usuários
2. **api.auth** - Autenticação (signin, signup, signout)
3. **api.client** - Gerenciamento de clientes
4. **api.vehicle** - Gerenciamento de veículos
5. **api.rent** - Gerenciamento de aluguéis

Cada módulo contém:
- `models.py` - Modelos do domínio
- `serializer.py` - Serializers DRF
- `views.py` - Views/Controllers
- `service.py` - Camada de serviço (quando necessário)
- `validation.py` - Validações customizadas (quando necessário)
- `urls.py` - Rotas do módulo
- `admin.py` - Configuração do admin Django
- `tests.py` - Testes do módulo

**Ordem de dependências no INSTALLED_APPS:**
1. `api.accounts` (base - define User)
2. `api.vehicle` (sem dependências de outros módulos)
3. `api.client` (depende de accounts)
4. `api.rent` (depende de vehicle e client)

---

**Referência completa:** `.github/copilot-instructions.md`
