# Memória de Regras do Projeto EasyDrive

> **Fonte:** `.github/copilot-instructions.md` (linhas 1-305)
> **Última atualização:** Criado como referência rápida das regras fundamentais

---

## 🎯 Visão Geral

**Projeto:** API RESTful para gerenciamento de aluguel de veículos  
**Stack:** Python 3.x, Django 5.1.1, DRF 3.15.2, PostgreSQL, MongoDB (logs), Redis (WebSocket), Channels

---

## 🔴 REGRAS FUNDAMENTAIS (OBRIGATÓRIAS)

### 1. Comentários e Documentação
- ❌ **NUNCA usar comentários inline** (`# comentário`)
- ✅ **SEMPRE usar docstrings** (Google Style ou NumPy Style)
- ✅ Docstrings em todas as classes e métodos públicos

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

## 📁 Estrutura de Diretórios

```
api/
├── model/          # Modelos Django (User, Client, Vehicle, Rental)
├── serializers/    # Serializers DRF
├── views/          # Views baseadas em GenericAPIView
├── build/          # Builders (Padrão Builder) - OBRIGATÓRIO
├── repositories/   # Adaptadores MongoDB (sync/async)
├── middleware/     # Middleware customizado
├── swagger/        # Documentação Swagger/OpenAPI
├── consumers.py    # WebSocket consumers
└── routing.py      # Rotas WebSocket
```

---

## 🏗️ Models (Django)

**Localização:** `api/model/`

**Convenções:**
- UUID como PK para models principais (exceto User)
- Incluir `created_at` e `updated_at` quando apropriado
- Implementar `__str__()` retornando representação legível
- Lógica de negócio no método `save()` quando necessário
- Docstrings obrigatórias com Attributes

---

## 🔍 Views (DRF)

**Preferir:** `generics.CreateAPIView`, `ListAPIView`, `UpdateAPIView`, `DestroyAPIView`

**Permissões:**
- `AllowAny`: Apenas para criação de usuário e login
- `IsAuthenticated`: Padrão para todos os endpoints protegidos

**Estrutura Obrigatória:**
- Declarar `permission_classes` explicitamente
- Declarar `serializer_class` e `queryset`
- Usar `select_related()`/`prefetch_related()` em list views
- Sobrescrever métodos HTTP (post, get, patch, delete) para lógica customizada
- Usar builders para criação de objetos
- Retornar Response com mensagens claras

---

## 📝 Serializers (DRF)

**Usar:** `ModelSerializer` sempre que possível

**Convenções:**
- Declarar `Meta` com `model` e `fields`
- Usar `extra_kwargs` para configurações de campos
- Validações complexas no método `validate()` ou `validate_<field>()`
- Serializers aninhados para relacionamentos (read-only)
- **Validações no serializer, NÃO na view**

---

## 🔨 Builders (Padrão Builder)

**Localização:** `api/build/`  
**Uso Obrigatório:** Para criação de User, Client, Vehicle, Rental

**Estrutura:**
- Métodos `set_<field>()` retornam `self` para fluência
- Método `build()` cria e retorna o objeto
- Validações básicas no `build()`
- Docstrings com exemplos de uso

---

## 💾 Repositories (MongoDB)

**Localização:** `api/repositories/`  
**Uso:** `MongoAdapter` (sync) ou `AsyncMongoAdapter` (async)

**Métodos:** `find_one`, `find_many`, `insert_one`, `update_one`, `delete_one`, `aggregate`  
**Resilência:** Usa Null Object Pattern para falhas de conexão

---

## ⚡ Performance - Banco de Dados

**🚨 CRÍTICO - SEMPRE OTIMIZAR:**

```python
# ❌ ERRADO - Causa N+1
queryset = Rental.objects.all()

# ✅ CORRETO - Otimizado
queryset = Rental.objects.select_related(
    'client__user', 
    'vehicle'
).prefetch_related(
    'vehicle__category'
).order_by('start_date')
```

---

## 🔐 Autenticação e Segurança

**JWT:** djangorestframework-simplejwt

**Endpoints:**
- `/api/token/` - Obter access/refresh tokens
- `/api/token/refresh/` - Renovar access token
- `/api/v1/login/` - Login customizado
- `/api/v1/logout/` - Logout com blacklist

**Headers:** `Authorization: Bearer <access_token>`  
**Configuração:** Tokens rotativos com blacklist habilitado

---

## 🌐 WebSocket (Channels)

**Consumer:** Herdar de `AsyncWebsocketConsumer`  
**Métodos:** `connect()`, `disconnect()`, `receive()`, `send_notification()`  
**Groups:** Usar `channel_layer.group_send()` para broadcast  
**Routing:** Definir em `api/routing.py`

---

## 📚 Documentação Swagger

- Usar `@extend_schema` do drf-spectacular
- Tags: Categorizar endpoints por domínio
- Examples: Fornecer exemplos de request/response
- Filters: Usar hook `filter_endpoints_by_allowed_tags`

---

## 🔧 Middleware

**LogErroMiddleware:** Captura erros automáticos e salva no MongoDB  
**Ordem:** Respeitar ordem no `settings.MIDDLEWARE`  
**Sanitização:** Remove dados sensíveis (passwords, tokens) dos logs

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
- [ ] Builders usados para criação de objetos

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
# HTTP
python manage.py runserver

# ASGI (WebSocket)
daphne -b 0.0.0.0 -p 8000 core.asgi:application
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
3. **SEMPRE** usar builders para criação de objetos
4. **SEMPRE** declarar permissões explicitamente nas views
5. **SEMPRE** fazer validações no serializer, não na view
6. **NUNCA** causar N+1 queries
7. **NUNCA** adicionar funcionalidades além do pedido
8. **SEMPRE** escrever testes automatizados para novas funcionalidades

---

**Referência completa:** `.github/copilot-instructions.md`

