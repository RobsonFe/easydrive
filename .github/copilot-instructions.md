# Instruções do Copilot para o Projeto EasyDrive

## 1. Visão Geral da Arquitetura

Este projeto é uma **API RESTful** para gerenciamento de **aluguel de veículos** construída com Django Rest Framework (DRF).

* **Stack Principal:** Python 3.x, Django 5.1.1, Django Rest Framework 3.15.2, PostgreSQL, MongoDB (logs), Redis (WebSocket), Channels (notificações em tempo real).
* **Objetivo:** Fornecer endpoints para gerenciamento de usuários, clientes, veículos e aluguéis com autenticação JWT, logs centralizados e notificações em tempo real.

## 2. Componentes Principais e Módulos

* `core/`: Configurações do Django (settings, urls, asgi, wsgi).
* `api/model/`: Modelos de domínio (`User`, `Client`, `Vehicle`, `Rental`).
* `api/serializers/`: Serializers DRF para validação e transformação de dados.
* `api/views/`: Views baseadas em GenericAPIView do DRF.
* `api/repositories/`: Adaptadores para MongoDB (síncrono e assíncrono).
* `api/middleware/`: Middleware customizado para logging automático.
* `api/swagger/`: Mixins para documentação Swagger/OpenAPI.
* `api/consumers.py`: WebSocket consumers para notificações em tempo real.
* `api/routing.py`: Rotas WebSocket.

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
  - ASGI (WebSocket): `daphne -b 0.0.0.0 -p 8000 core.asgi:application`
* **Testes:** Estrutura em `api/tests/`

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

* **Localização:** `api/model/`
* **Convenções:**
  - Usar UUID como PK para models principais (exceto User)
  - Incluir `created_at` e `updated_at` quando apropriado
  - Implementar `__str__()` retornando representação legível
  - Lógica de negócio no método `save()` quando necessário
  
**Exemplo:**
```python
class Vehicle(models.Model):
    """
    Modelo para representar veículos disponíveis para aluguel.
    
    Attributes:
        id: Identificador único UUID do veículo.
        brand: Marca do veículo.
        model: Modelo do veículo.
        quantity: Quantidade disponível em estoque.
        is_available: Calculado automaticamente baseado na quantity.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        Sobrescreve save para atualizar is_available automaticamente.
        """
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model}"
```

### **Views (DRF):**

* **Preferir:** `generics.CreateAPIView`, `ListAPIView`, `UpdateAPIView`, `DestroyAPIView`
* **Permissões:**
  - `AllowAny`: Apenas para criação de usuário e login
  - `IsAuthenticated`: Padrão para todos os endpoints protegidos
* **Estrutura:**
  - Declarar `permission_classes` explicitamente
  - Declarar `serializer_class` e `queryset`
  - Sobrescrever métodos HTTP (post, get, patch, delete) para lógica customizada
  - Usar builders para criação de objetos
  - Retornar Response com mensagens claras

**Exemplo:**
```python
class VehicleListView(generics.ListAPIView):
    """
    View para listar todos os veículos disponíveis.
    
    Retorna lista paginada de veículos ordenados por marca.
    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]
    queryset = Vehicle.objects.select_related('category').order_by('brand')
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

### **Builders (Padrão Builder):**

* **Localização:** `api/build/`
* **Uso Obrigatório:** Para criação de User, Client, Vehicle, Rental
* **Estrutura:**
  - Métodos `set_<field>()` retornam `self` para fluência
  - Método `build()` cria e retorna o objeto
  - Validações básicas no `build()`

**Exemplo:**
```python
class VehicleBuilder:
    """
    Builder para construção fluente de objetos Vehicle.
    
    Exemplo:
        vehicle = (VehicleBuilder()
            .set_brand("Toyota")
            .set_model("Corolla")
            .set_year(2024)
            .build())
    """
    def __init__(self):
        self._brand = ""
        self._model = ""
        self._year = 0
        
    def set_brand(self, brand: str) -> 'VehicleBuilder':
        """Define a marca do veículo."""
        self._brand = brand
        return self
        
    def build(self) -> Vehicle:
        """
        Constrói e retorna o objeto Vehicle.
        
        Returns:
            Instância de Vehicle.
            
        Raises:
            ValueError: Se campos obrigatórios não foram preenchidos.
        """
        if not self._brand:
            raise ValueError('Marca é obrigatória.')
        return Vehicle(brand=self._brand, model=self._model, year=self._year)
```

### **Repositories (MongoDB):**

* **Localização:** `api/repositories/`
* **Uso:** `MongoAdapter` (sync) ou `AsyncMongoAdapter` (async)
* **Métodos:** `find_one`, `find_many`, `insert_one`, `update_one`, `delete_one`, `aggregate`
* **Resilência:** Usa Null Object Pattern para falhas de conexão

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
* **Ordem:** Respeitar ordem no `settings.MIDDLEWARE`
* **Sanitização:** Remove dados sensíveis (passwords, tokens) dos logs

### **WebSocket (Channels):**

* **Consumer:** Herdar de `AsyncWebsocketConsumer`
* **Métodos:** `connect()`, `disconnect()`, `receive()`, `send_notification()`
* **Groups:** Usar `channel_layer.group_send()` para broadcast
* **Routing:** Definir em `api/routing.py`

### **Documentação Swagger:**

* **Mixins:** Usar `@extend_schema` do drf-spectacular
* **Tags:** Categorizar endpoints por domínio
* **Examples:** Fornecer exemplos de request/response
* **Filters:** Usar hook `filter_endpoints_by_allowed_tags`

## 5. Autenticação e Segurança

* **JWT:** djangorestframework-simplejwt
* **Endpoints:**
  - `/api/token/` - Obter access/refresh tokens
  - `/api/token/refresh/` - Renovar access token
  - `/api/v1/login/` - Login customizado
  - `/api/v1/logout/` - Logout com blacklist
* **Headers:** `Authorization: Bearer <access_token>`
* **Configuração:** Tokens rotativos com blacklist habilitado

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

## 7. Checklist de Implementação

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