# Projeto EasyDrive

## Descrição do Projeto

Esse projeto consiste em uma API feita em Django Rest Framework integrada com o banco de dados PostgreSQL, para gerenciar alugueis de carros, com documentação no Swagger e OpenAPI.

## Tecnologias Utilizadas no Projeto

- Django Rest Framework para o desenvolvimento de aplicações em Python.
- Banco de dados PostgreSQL.
- Swagger e OpenAPI para documentação da API.

## Front-End

Para o front-end, em NextJS, com o Flowbite e Tailwind para a criação de interfaces interativas
<br>
[Projeto Front-end](https://github.com/RobsonFe/)

## **Instalação**

Para instalar todas as ferramentas necessárias, basta utilizar o `requirements.txt`.

```python
pip install -r requirements.txt
```

## Endpoints da API

### **Link da Documentação da API**

<br>

- [Documentação da API](http://127.0.0.1:8000/docs/)

<br>

- [Documentação da API ALternativa](http://127.0.0.1:8000/redoc/)

<br>

---

- Schema

```json
{
  "title": "Estudar Python",
  "status": "Em andamento",
  "priority": "Alta"
}
```

# Documentação da API

## Visão Geral

Esta API REST gerencia tarefas com os seguintes campos: `title`, `status`, `priority`, e `notion_page_id`. Abaixo estão descritos os principais endpoints da API.

## Endpoints

### 1. **Criar Tarefa**

- **URL:** `/api/v1/notion/create/`
- **Método:** `POST`
- **Descrição:** Cria uma nova tarefa.
- **Corpo da Requisição:**
  ```json
  {
    "title": "Estudar Django",
    "status": "Em andamento",
    "priority": "Alta"
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `201 Created`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "_id": "unique_task_id",
      "title": "Aprendendo Python",
      "status": "Em andamento",
      "priority": "Alta",
      "notion_page_id": "generated_notion_page_id",
      "__v": 0
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `400 Bad Request` – Se houver erro de validação nos dados.

### 2. **Listar Tarefas**

- **URL:** `/api/v1/notion/list`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de todas as tarefas.
- **Parâmetros de Consulta (Opcional):**
  - `page`: Número da página para paginação (padrão: 1).
  - `limit`: Número de resultados por página (padrão: 10).
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "count": 3,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": "2044b453-8ef4-45dc-860e-d2abd0b13672",
          "title": "Aprendendo Python",
          "status": "Concluído",
          "priority": "Alta"
        },
        {
          "id": "3e150ad4-77ac-405c-a3cc-f0c843ccf288",
          "title": "Aprendendo Django Rest Framework",
          "status": "Em andamento",
          "priority": "Alta"
        },
        {
          "id": "c6c86d4a-50a6-48dc-8e8f-b15a9e72f16e",
          "title": "Estudando Django",
          "status": "Não iniciada",
          "priority": "Atenção"
        }
      ]
    }
    ```

### 3. **Obter Detalhes de uma Tarefa**

- **URL:** `/api/v1/notion/findby/{id}`
- **Método:** `GET`
- **Descrição:** Retorna os detalhes de uma tarefa específica.
- **Parâmetros de Caminho:**
  - `id`: O ID da tarefa a ser retornada.
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "id": "3e150ad4-77ac-405c-a3cc-f0c843ccf288",
      "title": "Aprendendo Django Rest Framework",
      "status": "Em andamento",
      "priority": "Alta"
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `404 Not Found` – Se a tarefa com o ID fornecido não for encontrada.

### 4. **Atualizar Tarefa**

- **URL:** `/api/v1/notion/atualizar/{id}`
- **Método:** `PUT`
- **Descrição:** Atualiza uma tarefa existente.
- **Parâmetros de Caminho:**
  - `id`: O ID da tarefa a ser atualizada.
- **Corpo da Requisição:**
  ```json
  {
    "id": "3e150ad4-77ac-405c-a3cc-f0c843ccf288",
    "title": "Aprendendo Django Rest Framework",
    "status": "Em andamento",
    "priority": "Alta"
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "id": "3e150ad4-77ac-405c-a3cc-f0c843ccf288",
      "title": "Aprendendo Django Rest Framework",
      "status": "Concluído",
      "priority": "Alta",
      "notion_page_id": "d9053095-4fe1-4e53-90b6-1bdb126fc838",
      "updatedAt": "2024-08-20T14:00:00Z",
      "__v": 0
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `400 Bad Request` – Se houver erro de validação nos dados.
  - **Código:** `404 Not Found` – Se a tarefa com o ID fornecido não for encontrada.

### 5. **Deletar Tarefa**

- **URL:** `/api/v1/notion/delete/{id}`
- **Método:** `DELETE`
- **Descrição:** Remove uma tarefa específica.
- **Parâmetros de Caminho:**
  - `id`: O ID da tarefa a ser removida.
- **Resposta de Sucesso:**
  - **Código:** `204 No Content`
- **Respostas de Erro Comuns:**
  - **Código:** `404 Not Found` – Se a tarefa com o ID fornecido não for encontrada.

## License

Licença [MIT licensed](LICENSE).
