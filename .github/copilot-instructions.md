# Instruções do Copilot para o Projeto EasyDrive

## 1. Visão Geral da Arquitetura

Este projeto é uma **API RESTful** para gerenciamento de **aluguel de veículos** construída com Django Rest Framework (DRF).

* **Stack Principal:** Python 3.x, Django 5.1.1, Django Rest Framework 3.15.2, PostgreSQL, MongoDB (logs).
* **Objetivo:** Fornecer endpoints para gerenciamento de usuários, clientes, veículos e aluguéis com autenticação JWT e logs centralizados.
* **Arquitetura:** Modular por domínio (accounts, auth, client, vehicle, rent).

## 2. Componentes Principais e Módulos

### Estrutura Modular

O projeto está organizado em módulos por domínio, cada um contendo seus próprios models, serializers, views, services e urls:

* `core/`: Configurações do Django (settings, urls, wsgi).
* `api/accounts/`: Módulo de Contas (User model, views, serializers, services, validations).
* `api/auth/`: Módulo de Autenticação (signin, signup, signout, services, validations, types).
* `api/client/`: Módulo de Clientes (Client model, views, serializers).
* `api/vehicle/`: Módulo de Veículos (Vehicle model, views, serializers).
* `api/rent/`: Módulo de Aluguéis (Rental model, views, serializers).
* `api/repositories/`: Adaptadores para MongoDB (síncrono e assíncrono).
* `api/middleware/`: Middleware customizado para logging automático.
* `api/swagger/`: Mixins para documentação Swagger/OpenAPI.
* `api/config/mongodb/`: Configurações MongoDB (connection handlers com Null Object Pattern).
* `api/utils/`: Utilitários (hooks para Swagger, helpers).

### Arquitetura de Cada Módulo

Cada módulo segue a estrutura:

```
{module}/
├── models.py          # Modelos do domínio
├── serializer.py      # Serializers DRF
├── views.py           # Views/Controllers
├── service.py         # Camada de serviço (quando necessário)
├── validation.py      # Validações customizadas (quando necessário)
├── urls.py            # Rotas do módulo
├── admin.py           # Configuração do admin Django
└── tests.py           # Testes do módulo
```

## 3. Fluxos de Trabalho do Desenvolvedor

* **Configuração do Ambiente:** 
  - Criar ambiente virtual: `python -m venv .venv`
  - Ativar (Windows PowerShell): `.venv\Scripts\Activate.ps1`
  - Instalar dependências: `pip install -r requirements.txt`
  - Configurar `.env` com variáveis de ambiente
* **Migrações:** 
  - Criar: `python manage.py makemigrations`
  - Aplicar: `python manage.py migrate`
* **Executar Servidor:** 
  - HTTP: `python manage.py runserver`
* **Testes:** Estrutura em cada módulo (`{module}/tests.py`)

## 4. Convenções e Padrões Específicos do Projeto

### **🔴 REGRAS FUNDAMENTAIS:**

1. **Comentários:**
   - ❌ **NUNCA usar comentários inline**
   - ✅ **SEMPRE usar docstrings** (Google Style ou NumPy Style)
   
2. **Código Limpo:**
   - ✅ Seguir PEP 8 e convenções do Django
   - ✅ Código claro, conciso e autoexplicativo
   - ❌ Evitar verbosidade desnecessária
   - ✅ Nomes descritivos de variáveis e funções

3. **Performance:**
   - ✅ **EVITAR N+1 QUERIES A TODO CUSTO**
   - ✅ Usar `select_related()` para ForeignKeys
   - ✅ Usar `prefetch_related()` para ManyToMany e reverse FKs
   - ✅ Otimizar querysets em métodos `get_queryset()`

### **Models (Django):**

* **Localização:** Cada módulo tem seu próprio `models.py`
* **Convenções:**
  - UUID como PK para models principais (exceto User que usa int)
  - Incluir `created_at` e `updated_at` quando apropriado
  - Implementar `__str__()` retornando representação legível
  - Lógica de negócio no método `save()` quando necessário
  
**Models Principais:**
- `api.accounts.models.User` - Usuário do sistema (AbstractBaseUser, USERNAME_FIELD = 'email')
- `api.client.models.Client` - Cliente (OneToOne com User, UUID PK)
- `api.vehicle.models.Vehicle` - Veículo (UUID PK, TypeVehicle: Carro/Moto)
- `api.rent.models.Rental` - Aluguel (FK para Client e Vehicle, UUID PK)

**Exemplo:**
```python
class Vehicle(models.Model):
    """
    Modelo para representar veículos disponíveis para aluguel.
    
    Attributes:
        id: Identificador único UUID do veículo.
        brand: Marca do veículo.
        model: Modelo do veículo.
        year: Ano do veículo.
        quantity: Quantidade disponível em estoque.
        type_vehicle: Tipo do veículo (Carro ou Moto).
        description: Descrição do veículo.
        is_available: Calculado automaticamente baseado na quantity.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    type_vehicle = models.CharField(max_length=10, choices=TypeVehicle.choices, default=TypeVehicle.CAR)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        Sobrescreve save para atualizar is_available automaticamente.
        """
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} - {self.model} - {self.year}"
```

### **Views (DRF):**

* **Preferir:** `generics.CreateAPIView`, `ListAPIView`, `UpdateAPIView`, `DestroyAPIView`, `RetrieveAPIView`, `APIView`
* **Permissões:**
  - `AllowAny`: Apenas para signup e login
  - `IsAuthenticated`: Padrão para todos os endpoints protegidos
* **Estrutura:**
  - Declarar `permission_classes` explicitamente
  - Declarar `serializer_class` e `queryset`
  - Sobrescrever métodos HTTP (post, get, patch, delete) para lógica customizada
  - Criar objetos diretamente usando `Model.objects.create()` ou `Model.objects.create_user()`
  - Retornar Response com mensagens claras
  - Usar Service Layer para lógica de negócio complexa

**Exemplo:**
```python
class VehicleListView(generics.ListAPIView):
    """
    View para listar todos os veículos disponíveis.
    
    Retorna lista paginada de veículos ordenados por marca.
    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]
    queryset = Vehicle.objects.all().order_by('brand')
    serializer_class = VehicleSerializer

    def get_queryset(self):
        """
        Otimiza queryset com select_related para evitar N+1.
        """
        return super().get_queryset()
```

### **Serializers (DRF):**

* **Usar:** `ModelSerializer` sempre que possível
* **Convenções:**
  - Declarar `Meta` com `model` e `fields`
  - Usar `extra_kwargs` para configurações de campos
  - Validações complexas no método `validate()` ou `validate_<field>()`
  - Serializers aninhados para relacionamentos (read-only)
  
**Exemplo:**
```python
class RentSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e leitura de aluguéis.
    
    Valida que a data de início não seja no passado.
    """
    class Meta:
        model = Rental
        fields = '__all__'
        
    def validate_start_date(self, value):
        """
        Valida que a data de início não seja no passado.
        
        Args:
            value: Data de início do aluguel.
            
        Returns:
            Data validada.
            
        Raises:
            ValidationError: Se a data for no passado.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'A data de início não pode ser no passado.'
            )
        return value
```

### **Service Layer Pattern:**

* **Localização:** `{module}/service.py`
* **Uso:** Para lógica de negócio complexa que não pertence ao model ou view
* **Exemplos:**
  - `UserService` (api.accounts.service) - Gerenciamento de avatar
  - `AuthenticationService` (api.auth.service) - Signin/signup

**Exemplo:**
```python
class UserService:
    """
    Camada de serviço para operações do usuário.
    """
    def update_avatar(self, user: User, avatar) -> User:
        """
        Atualiza avatar se arquivo for enviado.
        
        Args:
            user: Instância do usuário.
            avatar: Arquivo de imagem do avatar.
            
        Returns:
            User modificado (não salva).
        """
        # Lógica de atualização de avatar
        return user
```

### **Repositories (MongoDB):**

* **Localização:** `api/repositories/`
* **Uso:** `MongoAdapter` (sync) ou `AsyncMongoAdapter` (async)
* **Métodos:** `find_one`, `find_many`, `insert_one`, `update_one`, `delete_one`, `aggregate`, `count_documents`
* **Resilência:** Usa Null Object Pattern para falhas de conexão

**Exemplo:**
```python
from api.repositories.mongo_adapter import MongoAdapter

mongo = MongoAdapter(collection_name="erros")
mongo.save_error(user, endpoint, method, error, payload)
```

### **Performance (Banco de Dados):**

**🚨 CRÍTICO - EVITAR N+1:**

```python
# ❌ ERRADO - Causa N+1
class RentListView(generics.ListAPIView):
    queryset = Rental.objects.all()
    
# ✅ CORRETO - Otimizado
class RentListView(generics.ListAPIView):
    queryset = Rental.objects.select_related(
        'client__user', 
        'vehicle'
    ).prefetch_related(
        'vehicle__category'
    ).order_by('start_date')
```

### **Middleware:**

* **LogErroMiddleware:** Captura erros automáticos e salva no MongoDB
* **Localização:** `api/middleware/middlewares.py`
* **Funcionalidades:**
  - `process_request()`: Captura payload (sanitiza senhas/tokens)
  - `process_exception()`: Captura exceções não tratadas → MongoDB
  - `process_response()`: Captura respostas HTTP >= 400 → MongoDB
* **Ordem:** Respeitar ordem no `settings.MIDDLEWARE`
* **Sanitização:** Remove dados sensíveis (passwords, tokens) dos logs

### **Documentação Swagger:**

* **Mixins:** Usar `@extend_schema` do drf-spectacular
* **Tags:** Categorizar endpoints por domínio
* **Examples:** Fornecer exemplos de request/response
* **Filters:** Usar hook `filter_endpoints_by_allowed_tags`
* **Mixin disponível:** `UserCreateSwaggerMixin` (api.swagger.user_mixin)

## 5. Autenticação e Segurança

* **JWT:** djangorestframework-simplejwt
* **Endpoints:**
  - `/api/token/` - Obter access/refresh tokens (padrão DRF)
  - `/api/token/refresh/` - Renovar access token
  - `/api/v1/login` - Login customizado (SignInView)
  - `/api/v1/signup` - Cadastro de usuário (SignUpView)
  - `/api/v1/logout` - Logout com blacklist (SignOutView)
* **Headers:** `Authorization: Bearer <access_token>`
* **Configuração:** Tokens rotativos com blacklist habilitado
  - Access token: 24 horas
  - Refresh token: 8 dias
* **User Model:** `api.accounts.User` (AbstractBaseUser, USERNAME_FIELD = 'email')

## 6. Variáveis de Ambiente

Sempre usar `.env` para configurações sensíveis:

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

## 7. Arquitetura Modular e Dependências

### Ordem de Dependências no INSTALLED_APPS:

1. `api.accounts` (base - define User)
2. `api.vehicle` (sem dependências de outros módulos)
3. `api.client` (depende de accounts)
4. `api.rent` (depende de vehicle e client)

### Estrutura de URLs:

O arquivo `api/urls.py` centraliza todas as rotas dos módulos:

```python
from django.urls import include, path

urlpatterns = [
    path('', include('api.accounts.urls')),
    path('', include('api.auth.urls')),
    path('', include('api.client.urls')),
    path('', include('api.vehicle.urls')),
    path('', include('api.rent.urls')),
]
```

## 8. Checklist de Implementação

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
- [ ] Criar objetos diretamente (Model.objects.create() ou Model.objects.create_user())
- [ ] Usar Service Layer para lógica de negócio complexa
- [ ] Respeitar arquitetura modular (cada domínio em seu módulo)
- [ ] Testes automatizados para novas funcionalidades

## 9. Padrões de Projeto

### Repository Pattern
- `MongoAdapter` (síncrono) - `api/repositories/mongo_adapter.py`
- `AsyncMongoAdapter` (assíncrono) - `api/repositories/async_mongo_adapter.py`
- Métodos: find_one, find_many, insert_one, update_one, delete_one, aggregate, count_documents

### Null Object Pattern
- `NullCollection`, `NullDBConnection` - Resiliência para falhas de conexão MongoDB
- `AsyncNullCollection`, `AsyncNullDBConnection` - Versões assíncronas
- Localização: `api/config/mongodb/connection.py` e `async_connection.py`

### Service Layer Pattern
- `UserService` - `api/accounts/service.py` (gerenciamento de avatar)
- `AuthenticationService` - `api/auth/service.py` (signin/signup)

## 10. Lembretes Críticos

1. **SEMPRE** usar docstrings, nunca comentários inline
2. **SEMPRE** otimizar queries com `select_related`/`prefetch_related`
3. **SEMPRE** criar objetos diretamente (sem Builders)
4. **SEMPRE** declarar permissões explicitamente nas views
5. **SEMPRE** fazer validações no serializer, não na view
6. **NUNCA** causar N+1 queries
7. **NUNCA** adicionar funcionalidades além do pedido
8. **SEMPRE** escrever testes automatizados para novas funcionalidades
9. **SEMPRE** usar Service Layer para lógica de negócio complexa
10. **SEMPRE** respeitar a arquitetura modular (cada domínio em seu módulo)

## Referências

- README completo: `README.md`
- Resumo rápido: `api/docs/pedindo_para_ia/REGRAS_PROJETO.md`
- Regras do Cursor: `.cursorrules`
