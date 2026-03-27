# LAB02 — Características de Qualidade de Sistemas Java

**Disciplina:** Laboratório de Experimentação de Software  
**Curso:** Engenharia de Software  
**Professor:** Danilo de Quadros Maia Filho  
**Valor:** 20 pontos

---

## Integrantes

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/moraisjo">
        <img src="https://avatars.githubusercontent.com/u/92741380?v=4" width="100px;" alt="Joana Morais"/><br />
        <sub><b>Joana Morais</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/zezit">
        <img src="https://avatars.githubusercontent.com/u/95448020?v=4" width="100px;" alt="José Dias"/><br />
        <sub><b>José Dias</b></sub>
      </a>
    </td>
  </tr>
</table>

---

## Descrição

Este laboratório tem como objetivo analisar características de qualidade de repositórios Java open-source hospedados no GitHub. Por meio da API GraphQL do GitHub e da ferramenta CK (Code Metrics), serão coletados dados dos **1.000 repositórios Java com maior número de estrelas** para responder às seguintes questões de pesquisa:

| # | Questão de Pesquisa |
|---|---|
| RQ01 | Qual a relação entre a popularidade dos repositórios e as suas características de qualidade? |
| RQ02 | Qual a relação entre a maturidade do repositório e as suas características de qualidade? |
| RQ03 | Qual a relação entre a atividade dos repositórios e as suas características de qualidade? |
| RQ04 | Qual a relação entre o tamanho dos repositórios e as suas características de qualidade? |

### Métricas Utilizadas

#### Métricas do Processo (GitHub API)
- **Popularidade:** `stargazerCount`, `forkCount`, `watchers`
- **Maturidade:** `createdAt`, `updatedAt`, `releases`
- **Atividade:** Pull requests aceitas, issues fechadas/total
- **Tamanho:** LOC, número de arquivos

#### Métricas de Produto (CK Tool)
- CBO (Coupling Between Objects)
- DIT (Depth of Inheritance Tree)
- WMC (Weighted Methods per Class)
- LOC (Lines of Code)
- LCOM (Lack of Cohesion of Methods)
- RFC (Response for a Class)

---

## Configuração do Ambiente

### Pré-requisitos

- **Python 3.10+**
- **Git**
- **Java 11+** (para executar a ferramenta CK)
- **Maven** (para build da ferramenta CK)
- **GitHub Personal Access Token** (para acesso à API GraphQL)

### Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositório>
cd <nome-do-repositório>

# 2. Crie e ative um ambiente virtual
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### Configuração do Token GitHub

O script utiliza requisição HTTP direta para acessar a API GraphQL do GitHub. Configure seu token de uma das seguintes formas:

**Opção 1: Arquivo .env (Recomendado)**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione seu token
# GITHUB_TOKEN=ghp_seu_token_aqui
```

**Opção 2: Variável de ambiente**
```bash
export GITHUB_TOKEN=ghp_seu_token_aqui
```

**Opção 3: Arquivo ~/.bashrc**
Adicione a seguinte linha ao seu arquivo `~/.bashrc`:
```bash
export GITHUB_TOKEN=ghp_seu_token_aqui
```

**Como obter um token:**
1. Acesse [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Clique em "Generate new token (classic)"
3. Selecione o escopo `public_repo`
4. Copie o token gerado

> **⚠️ IMPORTANTE:** Nunca versione o arquivo `.env` com seu token real. O arquivo `.env` já está no `.gitignore`.

---

## Como Executar

### 1. Coleta de Dados do GitHub

Execute o script pipeline para coletar dados dos repositórios:

```bash
# Coletar 1000 repositórios (padrão)
python src/pipeline.py

# Especificar quantidade de repositórios
python src/pipeline.py --limit 500

# Especificar arquivo de saída
python src/pipeline.py --output data/my_repos.csv

# Forçar re-coleta mesmo se o arquivo já existir
python src/pipeline.py --force
```

**Opções disponíveis:**
- `--limit N`: Número de repositórios a coletar (padrão: 1000)
- `--output FILE`: Arquivo CSV de saída (padrão: data/repositories.csv)
- `--force`: Forçar re-coleta mesmo se já existir arquivo com dados suficientes

O script irá:
- Coletar dados dos N repositórios Java com mais estrelas
- Salvar os resultados em formato CSV no caminho especificado
- Pular a coleta se o arquivo já existir com dados suficientes (use `--force` para ignorar)

**Dados coletados:**
- `nameWithOwner`: Nome completo do repositório (owner/repo)
- `url`: URL do repositório
- `createdAt`: Data de criação
- `updatedAt`: Data da última atualização
- `stargazerCount`: Número de estrelas
- `forkCount`: Número de forks
- `watchersCount`: Número de watchers
- `releasesCount`: Número de releases
- `mergedPullRequestsCount`: Número de pull requests aceitos
- `closedIssuesCount`: Número de issues fechadas
- `totalIssuesCount`: Número total de issues
- `primaryLanguage`: Linguagem principal

### 2. Análise com CK Tool

A ferramenta CK está disponível em `source-code-ck/ck/`. Para utilizá-la:

```bash
# Clonar e analisar um repositório específico
cd source-code-ck/ck/
java -jar target/ck-*.jar /path/to/java/project true 0 false /output/path/
```

*(Integração automatizada em desenvolvimento)*

### 3. Geração de Visualizações

*(A ser implementado)*

---

## Estrutura do Projeto

```
.
├── .env.example                  # Exemplo de configuração de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências Python
├── README.md                     # Este arquivo
├── data/                         # Dados brutos coletados
│   └── repositories.csv         # Dados do GitHub (CSV)
├── docs/                         # Documentação do projeto
│   └── LABORATÓRIO 02...pdf     # Especificação do laboratório
├── reports/                      # Relatórios e visualizações
│   └── figures/                 # Gráficos gerados (a ser criado)
├── source-code-ck/              # Ferramenta CK
│   └── ck/                      # Repositório da ferramenta CK
└── src/                         # Código-fonte
    ├── pipeline.py              # Script de coleta de repositórios
    └── github_query.graphql     # Query GraphQL para busca de repositórios
```

---

## Troubleshooting

### Erro: `GITHUB_TOKEN não encontrado`
**Problema:** O script não consegue encontrar o token de autenticação do GitHub.

**Soluções:**
1. Crie um arquivo `.env` na raiz do projeto: `cp .env.example .env`
2. Adicione seu token ao arquivo `.env`: `GITHUB_TOKEN=ghp_seu_token_aqui`
3. Ou configure a variável de ambiente: `export GITHUB_TOKEN=ghp_seu_token_aqui`
4. Se usar `~/.bashrc`, reinicie o terminal ou execute `source ~/.bashrc`

### Erro: `401 Unauthorized` ou `403 Forbidden`
**Problema:** Token inválido, expirado ou sem permissões adequadas.

**Soluções:**
- Verifique se o token tem o escopo `public_repo`
- Gere um novo token em [github.com/settings/tokens](https://github.com/settings/tokens)
- Certifique-se de que o token não expirou
- Verifique se copiou o token completo (inicia com `ghp_`)

### Erro: `RuntimeError` ao buscar repositórios
**Problema:** Erro de comunicação com a API do GitHub.

**Possíveis causas e soluções:**
- **Sem conexão com internet:** Verifique sua conexão
- **Token inválido:** Confirme que o token está configurado corretamente
- **Rate limit excedido:** Aguarde 1 hora ou use outro token
  - Verifique seu rate limit em: https://api.github.com/rate_limit
- **API temporariamente indisponível:** Aguarde e tente novamente

### Erro: `ModuleNotFoundError`
**Problema:** Dependências Python não instaladas.

**Solução:**
```bash
# Certifique-se de que o ambiente virtual está ativado
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Erro: `FileNotFoundError: Query file not found`
**Problema:** Arquivo `github_query.graphql` não encontrado.

**Solução:**
- Certifique-se de que está executando o script a partir da raiz do projeto
- Verifique se o arquivo `src/github_query.graphql` existe

---

## Referências

- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [CK Metrics Tool](https://github.com/mauricioaniche/ck)
- [Laboratório 01](../lab-1/README.md)