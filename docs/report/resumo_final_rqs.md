# Resumo Final das RQs (RQ01-RQ04)

## 1) Contexto rapido: o que sao as metricas CK usadas

Neste estudo, a qualidade estrutural do codigo Java foi observada com tres metricas CK:

- CBO (Coupling Between Objects): mede acoplamento entre classes.
  Quanto maior, mais dependencias entre classes.
- DIT (Depth of Inheritance Tree): mede profundidade da heranca.
  Quanto maior, mais niveis na hierarquia.
- LCOM (Lack of Cohesion of Methods): mede falta de coesao interna.
  Quanto maior, pior a coesao entre metodos de uma classe.

Leitura simples: em geral, valores altos podem indicar maior complexidade de manutencao, mas sempre com contexto do sistema.

## 2) Metodologia usada para responder as questoes de pesquisa

### 2.1 Base e unidade de analise

- Fonte de dados: repositorios Java com metricas CK geradas.
- Unidade de analise: repositorio (nao classe).
- Cobertura principal das analises: 968 repositorios no consolidado, com 960 validos nas correlacoes principais.

### 2.2 Como os dados foram preparados

As metricas CK vieram em nivel de classe. Para comparar repositorios, foi feita agregacao por repositorio:

- media da metrica
- mediana da metrica
- desvio padrao da metrica

Para os testes de correlacao, foi usada principalmente a mediana por repositorio (ex.: cbo_median, dit_median, lcom_median).

### 2.3 Variaveis explicativas por RQ

- RQ01 (Popularidade): stargazerCount (estrelas).
- RQ02 (Maturidade): idade do repositorio em anos (age/365.25).
- RQ03 (Atividade): releasesCount.
- RQ04 (Tamanho): LOC total por repositorio; comentarios nao puderam ser analisados por falta de dados validos.

### 2.4 Estrategia analitica

Para cada RQ, foi feita correlacao entre variavel explicativa e qualidade (CBO, DIT, LCOM):

- Correlacao de Pearson (tendencia linear)
- Correlacao de Spearman (tendencia monotonicamente crescente/decrescente)
- p-valor para cada coeficiente

Nos graficos, quando necessario, a variavel do eixo X foi transformada com log10 para facilitar visualizacao (ex.: estrelas, releases, LOC).

## 3) Conceitos estatisticos usados (explicacao didatica)

### 3.1 Correlacao (r)

Correlacao indica se duas variaveis mudam juntas.

- Sinal:
  - positivo: uma sobe, a outra tende a subir
  - negativo: uma sobe, a outra tende a cair
- Tamanho (magnitude):
  - perto de 0: relacao fraca
  - mais longe de 0: relacao mais forte

Ponto importante: correlacao nao prova causa e efeito.

### 3.2 Pearson vs Spearman

- Pearson: olha relacao linear (tipo "reta").
- Spearman: olha ordem/ranking (se cresce ou decresce de forma monotona), sendo mais robusto quando ha assimetria e outliers.

Usar os dois ajuda a evitar conclusoes precipitadas quando os dados nao seguem um padrao perfeito.

### 3.3 p-valor e significancia

Pense no p-valor como um "termometro do acaso":

- p pequeno (ex.: < 0,05): menos provavel ser so sorte.
- p grande: nao da para descartar que seja acaso.

Aqui foi usado nivel de significancia de 5% (0,05).

### 3.4 Efeito estatistico x efeito pratico

Um resultado pode ser estatisticamente significativo (p < 0,05), mas com correlacao pequena.

Traduzindo: pode existir sinal estatistico, mas impacto pratico fraco.

### 3.5 Mediana, media, desvio padrao e outliers

- Media: valor medio geral.
- Mediana: valor central (mais resistente a extremos).
- Desvio padrao: dispersao dos dados.
- Outliers: valores muito fora do padrao.

## 4) Sintese final em linguagem direta

- As relacoes encontradas entre popularidade, maturidade, atividade e tamanho com as metricas CK foram, em geral, fracas.
- Quando apareceu significancia estatistica, o tamanho dos coeficientes normalmente foi pequeno.
- Em termos praticos: nesta amostra, fatores do repositorio (estrelas, idade, releases, LOC) nao explicam fortemente a qualidade estrutural medida por CBO, DIT e LCOM.