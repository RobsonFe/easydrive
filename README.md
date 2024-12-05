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
  "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
  "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
  "start_date": "2024-11-26"
}
```

# Documentação da API

## Visão Geral

Esta API REST gerencia aluguéis de veiculos com os seguintes campos: `client`, `vehicle`, e `start_date`. Abaixo estão descritos os principais endpoints da API.

## Endpoints

### 1. **Alugar um Carro**

- **URL:** `/api/v1/rent/create/`
- **Método:** `POST`
- **Descrição:** Aluga um Veiculo.
- **Corpo da Requisição:**
  ```json
  {
    "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
    "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
    "start_date": "2024-11-26"
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `201 Created`
  - **Exemplo de Corpo da Resposta:**
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
- **Respostas de Erro Comuns:**
  - **Código:** `400 Bad Request` – Se houver erro de validação nos dados.

### 2. **Listar Tarefas**

- **URL:** `/api/v1/rent/list/`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de todos os aluguéis.
- **Parâmetros de Consulta (Opcional):**
  - `page`: Número da página para paginação (padrão: 1).
  - `limit`: Número de resultados por página (padrão: 10).
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
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
            "total_rentals": 0,
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
            "quantity": 0,
            "type_vehicle": "Carro",
            "description": "",
            "is_available": true
          }
        },
        {
          "id": "1a5edbc0-7f25-496f-8f8d-57d8a1d0f64d",
          "start_date": "03-11-2024",
          "end_date": "04-11-2024",
          "client_data": {
            "id": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
            "total_rentals": 0,
            "user_data": {
              "id": 3,
              "username": "JohnWick",
              "name": "John Wick",
              "email": "john@gmail.com"
            }
          },
          "vehicle_data": {
            "id": "be5fa173-7ee2-4137-b3ca-1a18d6726c1f",
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2023,
            "quantity": 0,
            "type_vehicle": "Carro",
            "description": "",
            "is_available": true
          }
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
