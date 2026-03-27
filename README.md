# java-repositories-metrics-study

## Contexto

Este repositório está relacionado ao Laboratório 02 da disciplina de Experimentação de Software. O objetivo do estudo é analisar características de qualidade de repositórios Java open-source, relacionando métricas de produto com aspectos do processo de desenvolvimento.

O trabalho parte da coleta dos 1.000 repositórios Java mais populares do GitHub e da avaliação de métricas de qualidade calculadas com a ferramenta CK.

## Problemas principais

- Analisar a relação entre popularidade e qualidade dos repositórios.
- Verificar a relação entre maturidade e qualidade.
- Investigar a relação entre atividade e qualidade.
- Avaliar a relação entre tamanho e qualidade.
- Organizar e sumarizar os dados coletados com medidas como média, mediana e desvio padrão.

## Tecnologias

- Python 3.12.3
- GitHub REST API ou GraphQL
- CK para análise estática de código
- Arquivos CSV para armazenamento e consolidação dos resultados

## Métricas do CK e disponibilidade na GraphQL do GitHub

As métricas citadas pelo CK no contexto deste laboratório são métricas de produto do código e **não são calculadas diretamente pela GraphQL do GitHub**. A GraphQL fornece dados do repositório e do processo de desenvolvimento, que podem ser usados como variáveis independentes na análise.

### Métricas do CK

O CK cita, entre outras, as seguintes métricas de produto:

- CBO e CBO Modified
- FAN-IN e FAN-OUT
- DIT e NOC
- Number of fields
- Number of methods e Number of visible methods
- RFC
- WMC
- LOC
- LCOM, LCOM*, TCC e LCC
- Quantity of loops, comparisons, try/catches, variables e outras contagens estruturais

### Disponíveis via GraphQL do GitHub

Estas métricas não vêm do CK, mas podem ser obtidas pela API GraphQL do GitHub e usadas na correlação com as métricas de produto:

| Tipo | Exemplo de dado | Disponível na GraphQL? |
| --- | --- | --- |
| Popularidade | `stargazerCount`, `forkCount`, `watchers` | Sim |
| Atividade | commits, pull requests, issues | Sim |
| Maturidade | data de criação, última atualização, releases | Sim |
| Comunidade | contribuidores, autores, engajamento | Parcialmente |
| Linguagens | `languages` do repositório | Sim |
| Qualidade do código CK | CBO, WMC, LOC, LCOM etc. | Não |

### Resumo prático

- Use a GraphQL para coletar características do repositório e do processo.
- Use o CK para calcular as métricas de código Java.
- Depois, una os dois conjuntos de dados para analisar correlações.