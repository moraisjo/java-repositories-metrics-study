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

**Opção 1: Variável de ambiente**
```bash
export GITHUB_TOKEN=seu_token_aqui_ghp_xxxxxxxxxxxxxxxxx
```

**Opção 2: Arquivo ~/.bashrc**
Adicione a seguinte linha ao seu arquivo `~/.bashrc`:
```bash
export GITHUB_TOKEN=seu_token_aqui_ghp_xxxxxxxxxxxxxxxxx
```

**Como obter um token:**
1. Acesse [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Clique em "Generate new token (classic)"
3. Selecione o escopo `public_repo`
4. Copie o token gerado

---

## Como Executar

### 1. Coleta de Dados do GitHub

Execute o script pipeline para coletar dados dos repositórios:

```bash
python src/pipeline.py
```

O script irá:
- Coletar dados dos 1000 repositórios Java com mais estrelas
- Salvar os resultados em formato JSON no stdout

Para salvar em arquivo:

```bash
python src/pipeline.py > data/repos.json
```

### 2. Análise com CK Tool

*(A ser implementado)*

### 3. Geração de Visualizações

*(A ser implementado)*

---

## Estrutura do Projeto

```
.
├── requirements.txt              # Dependências Python
├── README.md                     # Este arquivo
├── data/                         # Dados brutos coletados
│   └── repos.json               # Dados do GitHub (JSON)
├── docs/                         # Documentação do projeto
│   └── LABORATÓRIO 02...pdf     # Especificação do laboratório
├── reports/                      # Relatórios e visualizações
│   └── figures/                 # Gráficos gerados
├── source-code-ck/              # Ferramenta CK
└── src/
    └── pipeline.py              # Script de coleta de repositórios
```

---

## Troubleshooting

### Erro: `GITHUB_TOKEN não encontradas`
- Configure a variável de ambiente: `export GITHUB_TOKEN=seu_token`
- Ou adicione ao `~/.bashrc`: `export GITHUB_TOKEN=seu_token`
- Reinicie o terminal ou execute `source ~/.bashrc` após editar

### Erro: `401 Unauthorized` ou `403 Forbidden`
- Seu token expirou ou é inválido
- Verifique se o token tem o escopo `public_repo`
- Gere um novo token em [github.com/settings/tokens](https://github.com/settings/tokens)

### Erro: `RuntimeError` ao buscar repositórios
- Verifique sua conexão com a internet
- Confirme que o token está configurado corretamente
- Verifique se você não excedeu o rate limit da API do GitHub

---

## Referências

- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [CK Metrics Tool](https://github.com/mauricioaniche/ck)
- [Laboratório 01](../lab-1/README.md)