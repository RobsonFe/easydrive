### 1\. O que é um Snippet de Usuário do VS Code para Pedir Tarefas ao Copilot

  * **O que ele é?** É um **Snippet de Usuário do VS Code**.
  * **Onde ele fica?** Ele fica "escondido" nas pastas de configuração *do seu editor de código pessoal*, não no seu repositório Git.
  * **O que ele faz?** Ele é um atalho de produtividade *para você*. Quando você digita um prefixo (como `!tarefa`) e aperta `TAB`, ele cola automaticamente o seu template de pedido (o conteúdo do seu `docs/index.md`) na sua tela de chat.

Ele serve para você não ter que ir até o arquivo `docs/index.md`, copiar o conteúdo e colar no chat toda vez que for pedir algo.

### 2\. Passo a Passo: Como Criar o Snippet no VS Code

Aqui está o guia para configurar esse "atalho" no seu VS Code:

1.  No VS Code, abra a Paleta de Comandos:
      * `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
2.  Digite **"Snippets"** na barra de pesquisa.
3.  Selecione a opção **"Snippets: Configurar Snippets de Usuário"**.
4.  Uma nova caixa de pesquisa aparecerá. Digite **`markdown.json`** e pressione `Enter`. (Se ele perguntar, escolha "Novo Arquivo de Snippets Global..." e nomeie-o `markdown.json`).
5.  O VS Code abrirá um arquivo chamado `markdown.json`. Ele estará quase vazio, provavelmente com apenas `{ }` e alguns comentários.
6.  **Copie e cole o código JSON abaixo** para dentro das chaves `{ }`:

<!-- end list -->

```json
{
  "Tarefa EasyDrive": {
    "prefix": "!tarefa",
    "body": [
      "# Prefeito, vamos implementar uma nova funcionalidade no Easydrive",
      "",
      "## 1. Objetivo da Tarefa",
      "> ${1:Descreva o que você quer aqui.}",
      "",
      "## 2. Contexto e Localização",
      "> Arquivos que serão modificados:",
      "> - ${2:apps/modulo/arquivo.py}",
      "",
      "## 3. Requisitos Detalhados",
      "* ${3:Requisito 1}",
      "* ${4:Requisito 2}",
      "",
      "---",
      "**Importante:** Siga rigorosamente TODAS as regras e padrões (Docstrings, Type Hints, N+1, Builders, etc) definidos no arquivo de instruções do projeto (`.github/copilot-instructions.md`)."
    ],
    "description": "Gera um template de prompt para pedir uma nova tarefa no EasyDrive."
  }
}
```

7.  **Salve** o arquivo `markdown.json` e **feche-o**.

**Pronto\!** Agora, em qualquer chat do Copilot ou em qualquer arquivo Markdown (`.md`), digite `!tarefa` e aperte `TAB`. O template aparecerá magicamente.

-----

### 3\. Onde Colocar Cada Arquivo

Esta é a parte mais importante para a automação funcionar.

  * **O seu template de tarefa (`docs/index.md`):**

      * **Onde está:** `docs/index.md`
      * **Está correto?** Sim, é um ótimo lugar para *documentar* o template. Mas, com o snippet que criamos, você não vai precisar abrir esse arquivo no dia-a-dia.
      * **Devo colocar nas instruções do GitHub?** **Não.** Mantenha-o separado. As "Instruções" são o manual; o "Template de Tarefa" é o formulário.

  * **O seu guia do projeto (`Instruções do Copilot para o Projeto EasyDrive`):**

      * **Onde está:** Você não especificou, mas *talvez* esteja no mesmo `docs/index.md` ou em outro arquivo.

      * **Onde DEVE estar:** Para que o GitHub Copilot o leia *automaticamente*, você **DEVE** criar uma pasta `.github` na raiz do seu projeto e salvar esse arquivo com o nome exato:

        **`.github/copilot-instructions.md`**

      * **Ação:** Copie todo o conteúdo do seu excelente guia "Instruções do Copilot para o Projeto EasyDrive" e salve-o nesse novo caminho.

### Resumo do Fluxo de Trabalho Ideal

1.  **Configuração (Feita uma vez):**
      * Você salva seu guia do projeto em `.github/copilot-instructions.md`.
      * Você salva o snippet JSON no seu VS Code.
2.  **Uso Diário (Seu novo "pedir corretamente"):**
      * Abra o arquivo `prompt.md`.
      * Digite `!tarefa` e pressione `TAB`.
      * O template aparece. Preencha as seções 1, 2 e 3.
      * Envie o prompt.

A IA irá (1) ler sua tarefa, e (2) ler automaticamente o `.github/copilot-instructions.md` para entender as regras de arquitetura (Builders, N+1, Docstrings, etc.) e aplicá-las à sua tarefa.
