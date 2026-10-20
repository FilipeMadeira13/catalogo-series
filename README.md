# Catálogo de Séries

API para cadastrar, listar e consultar séries, desenvolvida com Python, FastAPI e SQLite.

O repositório mantém o nome `catalogo-filmes`, mas a implementação atual é voltada ao gerenciamento de séries.

## Funcionalidades

- Cadastro de séries com título, gênero, ano de lançamento e número de temporadas.
- Listagem de todas as séries cadastradas.
- Consulta por título.
- Validação dos dados recebidos.
- Prevenção de títulos duplicados, desconsiderando diferenças entre maiúsculas e minúsculas e espaços nas extremidades.
- Persistência local em SQLite.
- Documentação interativa da API.

## Tecnologias

| Tecnologia | Finalidade |
| --- | --- |
| Python | Linguagem da aplicação |
| FastAPI | Construção da API HTTP |
| Pydantic | Validação dos dados |
| SQLite | Armazenamento local |
| Uvicorn | Servidor da aplicação |

As versões das dependências estão fixadas em `requirements.txt`.

## Requisitos

- Python 3.11 ou superior, conforme os requisitos das dependências atuais.
- `pip` e suporte a ambientes virtuais.
- Git para clonar o repositório.

O ambiente local inspecionado utiliza Python 3.13.0. A compatibilidade de execução com outras versões ainda não foi validada.

## Instalação

Clone o repositório e acesse a pasta:

```bash
git clone https://github.com/FilipeMadeira13/catalogo-filmes.git
cd catalogo-filmes
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

**Linux e macOS**

```bash
source .venv/bin/activate
```

**Windows — PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Execução

Na raiz do projeto, com o ambiente virtual ativado:

```bash
python -m uvicorn app.main:app --reload
```

A aplicação estará disponível em:

- API: http://127.0.0.1:8000
- Documentação interativa Swagger UI: http://127.0.0.1:8000/docs
- Documentação ReDoc: http://127.0.0.1:8000/redoc
- Especificação OpenAPI: http://127.0.0.1:8000/openapi.json

A opção `--reload` reinicia o servidor quando o código muda e é destinada ao desenvolvimento.

## Endpoints

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/` | Retorna uma mensagem sobre a aplicação |
| GET | `/series/` | Lista as séries cadastradas |
| GET | `/series/{titulo}` | Consulta uma série pelo título |
| POST | `/series/` | Cadastra uma série |

### Cadastrar uma série

```bash
curl -X POST "http://127.0.0.1:8000/series/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Breaking Bad",
    "genero": "Drama",
    "ano_lancamento": 2008,
    "temporadas": 5
  }'
```

Exemplo de resposta com status `201 Created`:

```json
{
  "mensagem": "Série criada com sucesso",
  "serie": {
    "id": 1,
    "titulo": "Breaking Bad",
    "genero": "Drama",
    "ano_lancamento": 2008,
    "temporadas": 5
  }
}
```

O identificador é gerado pelo banco de dados e pode variar.

### Listar séries

```bash
curl "http://127.0.0.1:8000/series/"
```

O resultado é uma lista de séries. Quando não há registros, a resposta é `[]`.

### Consultar pelo título

```bash
curl "http://127.0.0.1:8000/series/Breaking%20Bad"
```

A consulta utiliza o título completo, desconsiderando maiúsculas, minúsculas e espaços nas extremidades. Não há busca parcial nem remoção de acentos.

## Regras de validação

| Campo | Regra |
| --- | --- |
| `titulo` | Obrigatório; não pode ficar vazio após remover espaços nas extremidades |
| `genero` | Texto obrigatório; atualmente aceita texto vazio |
| `ano_lancamento` | Inteiro maior que 1900 |
| `temporadas` | Inteiro maior que zero |
| `id` | Gerado automaticamente no cadastro |

Os quatro campos do cadastro são obrigatórios.

### Respostas de erro

| Status HTTP | Situação |
| --- | --- |
| `404 Not Found` | Série não encontrada na consulta |
| `409 Conflict` | Já existe uma série com o título informado |
| `422 Unprocessable Entity` | Dados incompatíveis com as validações da API |

## Estrutura do projeto

```text
catalogo-filmes/
├── app/
│   ├── db/
│   │   └── local.py                 # Conexões e criação da tabela SQLite
│   ├── models/
│   │   └── serie.py                 # Modelos de entrada e resposta
│   ├── repositories/
│   │   └── serie_repositorio.py     # Consultas e cadastro no banco
│   ├── routers/
│   │   └── serie.py                 # Rotas HTTP
│   ├── utils/
│   │   ├── normalizacao.py          # Normalização de títulos
│   │   └── utils_json.py            # Utilitários JSON sem uso nas rotas atuais
│   ├── dependencias.py              # Fornecimento do banco e repositório às rotas
│   └── main.py                      # Criação da aplicação FastAPI
├── .gitignore
├── requirements.txt
└── README.md
```

As rotas recebem as requisições, os modelos validam os dados e o repositório concentra o acesso ao banco.

## Persistência

O arquivo `series.db` e a tabela `series` são criados automaticamente durante a inicialização da aplicação.

O caminho do banco é relativo ao diretório de execução. Execute o servidor na raiz do projeto para manter os dados no local esperado.

O banco local está excluído do versionamento pelo `.gitignore`.

As operações atuais utilizam SQLite. Arquivos `series.json` existentes não são importados automaticamente.

## Estado atual

O projeto está em desenvolvimento. Atualmente:

- Não há endpoints para atualizar ou excluir séries.
- Não há autenticação, paginação ou filtros por gênero e ano.
- Não foi identificada uma suíte de testes automatizados no repositório.
- Não há licença de uso definida em um arquivo `LICENSE`.

Os exemplos desta documentação descrevem o comportamento implementado; não representam evidência de testes de execução.
