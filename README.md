# Projeto EasyDrive

## Descrição do Projeto

O **EasyDrive** é uma aplicação de API desenvolvida em **Django Rest Framework** e integrada com o banco de dados **PostgreSQL**. O sistema tem como objetivo gerenciar o aluguel de carros, permitindo o CRUD de veículos, clientes e aluguéis, além de fornecer a documentação interativa via **Swagger** e **OpenAPI**.

A aplicação oferece recursos para o **administrador** gerenciar os aluguéis e os **clientes** visualizarem seus aluguéis passados e futuros.

## Tecnologias Utilizadas no Projeto

- **Django Rest Framework** para o desenvolvimento da API.
- **Banco de dados PostgreSQL** para persistência de dados.
- **Swagger e OpenAPI** para a documentação da API.
- **Next.js** para o front-end da aplicação.
- **Flowbite** e **TailwindCSS** para a criação de interfaces interativas e responsivas no front-end.

## Front-End

O front-end foi desenvolvido com **Next.js**, utilizando **Flowbite** e **TailwindCSS** para construção de interfaces de usuário dinâmicas e responsivas.

[Projeto Front-end](https://github.com/RobsonFe/)

## Instalação

Para instalar as dependências do projeto, basta rodar o seguinte comando para instalar todos os pacotes necessários:

```bash
pip install -r requirements.txt
```

Além disso, é necessário configurar o banco de dados PostgreSQL. Abaixo estão os passos para a configuração do ambiente:

1. Crie um banco de dados PostgreSQL.
2. Altere as configurações de conexão no arquivo `settings.py` do Django para refletir seu banco de dados local.
3. Rode as migrações com o comando:
   ```bash
   python manage.py migrate
   ```

## Endpoints da API

### Link da Documentação da API

- [Documentação da API Swagger](http://127.0.0.1:8000/docs/)
- [Documentação da API (Alternativa)](http://127.0.0.1:8000/redoc/)

---

### Exemplo de Payload para Aluguel de Carro

```json
{
  "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
  "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e",
  "start_date": "2024-11-26"
}
```

## Endpoints da API

### 1. **Alugar um Carro**

- **URL:** `/api/v1/rent/create/`
- **Método:** `POST`
- **Descrição:** Cria um novo aluguel de carro.
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

### 2. **Listar Todos os Aluguéis**

- **URL:** `/api/v1/rent/list/`
- **Método:** `GET`
- **Descrição:** Retorna uma lista paginada de todos os aluguéis.
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
            "is_available": true
          }
        }
      ]
    }
    ```

### 3. **Obter Detalhes de um Aluguel**

- **URL:** `/api/v1/rent/detail/{id}/`
- **Método:** `GET`
- **Descrição:** Retorna os detalhes de um aluguel específico pelo ID.
- **Parâmetros de Caminho:**
  - `id`: ID do aluguel.
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "id": "5adb384a-5e82-44cc-8fd7-11e73ef2074e",
      "start_date": "26-11-2024",
      "end_date": null,
      "returned": false,
      "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
      "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e"
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `404 Not Found` – Se o aluguel com o ID fornecido não for encontrado.

### 4. **Atualizar um Aluguel**

- **URL:** `/api/v1/rent/update/{id}/`
- **Método:** `PUT`
- **Descrição:** Atualiza os dados de um aluguel.
- **Parâmetros de Caminho:**
  - `id`: ID do aluguel a ser atualizado.
- **Corpo da Requisição:**
  ```json
  {
    "end_date": "30-11-2024",
    "returned": true
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "message": "Aluguel atualizado com sucesso!",
      "result": {
        "id": "5adb384a-5e82-44cc-8fd7-11e73ef2074e",
        "start_date": "26-11-2024",
        "end_date": "30-11-2024",
        "returned": true,
        "client": "0d4c67db-954d-466b-b4ea-2d9b137c4c3f",
        "vehicle": "0e59edda-1ef4-49cd-b05f-85603fbafa1e"
      }
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `400 Bad Request` – Se houver erro de validação nos dados.

### 5. **Deletar um Aluguel**

- **URL:** `/api/v1/rent/delete/{id}/`
- **Método:** `DELETE`
- **Descrição:** Deleta um aluguel pelo ID.
- **Resposta de Sucesso:**
  - **Código:** `204 No Content`
- **Respostas de Erro Comuns:**
  - **Código:** `404 Not Found` – Se o aluguel com o ID fornecido não for encontrado.

## License

Este projeto é licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
