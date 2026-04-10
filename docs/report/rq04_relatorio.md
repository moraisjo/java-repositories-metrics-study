# RQ04 - Relacao entre Tamanho dos Repositorios e Caracteristicas de Qualidade

## 1. Introducao e Hipoteses Informais

A RQ04 analisa se repositorios Java maiores tendem a apresentar diferencas de qualidade estrutural.

Conceitos:
a. CBO: acoplamento entre classes,
b. DIT: profundidade de heranca,
c. LCOM: falta de coesao entre metodos.

Variaveis de tamanho consideradas:
1. LOC (linhas de codigo),
2. linhas de comentarios.

Hipoteses informais adotadas antes da analise:
1. H1: Repositorios com maior LOC tenderiam a ter maior CBO.
2. H2: Repositorios com maior LOC tenderiam a ter maior DIT.
3. H3: Repositorios com maior LOC tenderiam a ter maior LCOM.
4. H4: Repositorios com mais linhas de comentarios tenderiam a ter menor CBO.
5. H5: Repositorios com mais linhas de comentarios tenderiam a ter menor DIT.
6. H6: Repositorios com mais linhas de comentarios tenderiam a ter menor LCOM.

## 2. Metodologia

### 2.1 Coleta e preparacao dos dados

- Fonte de tamanho: metricas CK por classe.
- LOC por repositorio: soma de `loc` das classes do repositorio.
- Linhas de comentarios por repositorio: tentativa de leitura de colunas de comentarios no CK (`commentLines`, `comment_lines`, `commentsLines`, `comments_lines`, `loc_comments`, `commentLoc`, `cloc`).
- Fonte de qualidade: metricas CK por classe (`cbo`, `dit`, `lcom`).
- Unidade analitica da RQ04: repositorio.

Foram usados apenas os repositorios com `ckMetricsGenerated=true`.

### 2.2 Sumarizacao por repositorio

Para cada repositorio, as metricas CK em nivel de classe foram agregadas por:

- media;
- mediana;
- desvio padrao amostral.

Esse calculo foi feito separadamente para CBO, DIT e LCOM. Assim, cada repositorio ficou com os campos:

- `<metrica>_mean`
- `<metrica>_median`
- `<metrica>_std`

Tambem foram calculados:

- `total_loc`: soma de `loc` por repositorio;
- `total_comment_lines`: soma da coluna de comentarios (quando existente).

O arquivo completo com essa sumarizacao por repositorio esta em:

- `assets/rq04/rq04_resumo_por_repositorio.csv`

### 2.3 Analise estatistica

- Para visualizacao, foi usada a transformacao `log10(tamanho + 1)` no eixo X dos graficos.
- Para medir a relacao entre tamanho e qualidade, foram calculadas correlacoes de Pearson e Spearman entre cada variavel de tamanho e a **mediana por repositorio** de cada metrica (`cbo_median`, `dit_median`, `lcom_median`).
- Tambem foi calculado o p-valor de cada correlacao.

## 3. Resultados

### 3.1 Cobertura dos dados

- Repositorios no dataset consolidado da RQ04: 968.
- Repositorios com LOC valido: 968.
- Repositorios com linhas de comentarios validas: 0.
- Repositorios com valores validos para correlacoes LOC vs qualidade (por metrica): 960.
- Repositorios com valores validos para correlacoes comentarios vs qualidade (por metrica): 0.

### 3.2 Correlacoes (tamanho vs mediana da metrica por repositorio)

Pense no p-valor como um "termometro de coincidencia". Ele responde: "Se nao existisse relacao nenhuma entre as coisas que estou comparando, qual seria a chance de eu ver um resultado como este so por acaso?"

> p-valor pequeno
Significa: "seria raro acontecer so por sorte".
Entao a gente comeca a acreditar que pode existir relacao de verdade.

> p-valor grande
Significa: "isso pode acontecer por sorte sem problema".
Entao nao da para afirmar que existe relacao.

| Variavel de tamanho | Metrica | Pearson | p-valor (Pearson) | Spearman | p-valor (Spearman) | n |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| LOC | CBO | 0.1617 | 0.0000 | 0.2942 | 0.0000 | 960 |
| LOC | DIT | -0.0187 | 0.5638 | -0.0372 | 0.2494 | 960 |
| LOC | LCOM | 0.0197 | 0.5420 | 0.1588 | 0.0000 | 960 |
| COMMENT_LINES | CBO | NaN | NaN | NaN | NaN | 0 |
| COMMENT_LINES | DIT | NaN | NaN | NaN | NaN | 0 |
| COMMENT_LINES | LCOM | NaN | NaN | NaN | NaN | 0 |

Considerando nivel de significancia de 5% (0,05):

- Para LOC, CBO apresentou associacao positiva fraca com significancia estatistica em Pearson e Spearman.
- Para LOC, DIT nao apresentou evidencia estatistica de associacao.
- Para LOC, LCOM apresentou associacao monotonicamente positiva fraca em Spearman, sem evidencia linear em Pearson.
- Para linhas de comentarios, nao foi possivel calcular correlacoes (n=0).

Mesmo nos casos com p-valor abaixo de 0,05, os coeficientes observados para LOC sao pequenos em magnitude, indicando efeito fraco.

**ATENCAO**
- p-valor fala de confianca contra o acaso;
- coeficiente fala de tamanho da relacao.

Arquivo CSV correspondente:

- `assets/rq04/rq04_correlacoes.csv`

### 3.3 Medidas centrais das estatisticas por repositorio

Resumo das estatisticas (media, mediana e desvio padrao) calculadas por repositorio:

| Metrica | Descricao metrica | Estatistica por repositorio | n | Media (entre repositorios) | Mediana (entre repositorios) | Desvio padrao (entre repositorios) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| CBO | Acoplamento entre classes | mean | 960 | 5.339 | 5.276 | 1.872 |
| CBO | Acoplamento entre classes | median | 960 | 3.535 | 3.000 | 1.727 |
| CBO | Acoplamento entre classes | std | 951 | 6.247 | 6.009 | 2.630 |
| DIT | Profundidade de heranca | mean | 960 | 1.451 | 1.388 | 0.343 |
| DIT | Profundidade de heranca | median | 960 | 1.090 | 1.000 | 0.302 |
| DIT | Profundidade de heranca | std | 951 | 1.058 | 0.769 | 2.178 |
| LCOM | Falta de coesao entre metodos | mean | 960 | 116.138 | 23.793 | 1765.278 |
| LCOM | Falta de coesao entre metodos | median | 960 | 1.460 | 0.000 | 16.209 |
| LCOM | Falta de coesao entre metodos | std | 951 | 3282.823 | 130.539 | 76753.952 |

### 3.4 Graficos (diagramas de dispersao)

![LOC_CBO](assets/rq04/rq04_loc_cbo_scatter.png)

Fig. 1: Relacao entre tamanho em LOC (escala log10(LOC+1) no eixo X) e CBO. A linha vermelha apresenta inclinacao positiva leve, coerente com associacao positiva fraca.

![LOC_DIT](assets/rq04/rq04_loc_dit_scatter.png)

Fig. 2: Relacao entre tamanho em LOC e DIT. A linha de tendencia aparece praticamente horizontal, consistente com correlacoes fracas e nao significativas.

![LOC_LCOM](assets/rq04/rq04_loc_lcom_scatter.png)

Fig. 3: Relacao entre tamanho em LOC e LCOM. A tendencia linear e fraca, com alta dispersao e outliers; em Spearman ha associacao monotonicamente positiva fraca.

## 4. Discussao (Hipoteses vs Resultados)

### 4.1 Hipoteses para LOC (H1-H3)

- H1 (LOC vs CBO): parcialmente suportada, com associacao positiva fraca (Pearson = 0.1617; Spearman = 0.2942).
- H2 (LOC vs DIT): nao suportada, com coeficientes proximos de zero e sem significancia estatistica.
- H3 (LOC vs LCOM): parcialmente suportada apenas em Spearman (0.1588), com efeito fraco.

### 4.2 Hipoteses para linhas de comentarios (H4-H6)

Nao foi possivel testar H4, H5 e H6 com a base consolidada atual porque nao houve disponibilidade de valores para `COMMENT_LINES` (n=0).

### 4.3 Sintese da RQ04

Com base nos dados, o tamanho por LOC apresentou, no maximo, relacoes fracas com as metricas de qualidade analisadas (CBO, DIT e LCOM), considerando as medianas por repositorio.

Para linhas de comentarios, a analise quantitativa nao pode ser concluida com os dados atualmente disponiveis.

## 5. Limitacoes e Ameacas a Validade (RQ04)

1. Apenas tres metricas CK foram consideradas na RQ04 (CBO, DIT, LCOM).
2. O tamanho por LOC foi obtido por agregacao de `loc` por classe; isso nao diferencia codigo gerado automaticamente e codigo manual.
3. Linhas de comentarios nao estavam disponiveis na base consolidada usada na analise (n=0).
4. LCOM apresenta forte assimetria e outliers, afetando interpretacoes em metodos sensiveis a escala.
5. Correlacao nao implica causalidade.

## 6. Artefatos gerados para a RQ04

- Sumarizacao por repositorio: `assets/rq04/rq04_resumo_por_repositorio.csv`
- Correlacoes: `assets/rq04/rq04_correlacoes.csv`
- Figuras: `assets/rq04/rq04_loc_cbo_scatter.png`, `assets/rq04/rq04_loc_dit_scatter.png`, `assets/rq04/rq04_loc_lcom_scatter.png`
