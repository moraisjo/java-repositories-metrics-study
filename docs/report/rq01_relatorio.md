# RQ01 - Relação entre Popularidade e Características de Qualidade

## 1. Introdução e Hipóteses Informais

A RQ01 investiga se repositórios Java mais populares (com mais estrelas no GitHub) tendem a apresentar melhores características de qualidade de código.

Hipóteses informais adotadas antes da análise:

1. Repositórios mais populares tenderiam a ter menor acoplamento (CBO), por receberem maior escrutínio da comunidade.
2. Repositórios mais populares tenderiam a manter menor profundidade de herança (DIT), por priorizarem simplicidade de manutenção.
3. Repositórios mais populares tenderiam a ter menor falta de coesão (LCOM), por terem código mais organizado.

## 2. Metodologia

### 2.1 Coleta e preparação dos dados

- Fonte de popularidade: `stargazerCount` (GitHub API).
- Fonte de qualidade: métricas CK por classe (`cbo`, `dit`, `lcom`).
- Unidade analítica da RQ01: repositório.

Foram considerados apenas os repositórios com `ckMetricsGenerated=true`.

### 2.2 Sumarização por repositório

Para cada repositório, as métricas CK em nível de classe foram agregadas por:

- média;
- mediana;
- desvio padrão amostral.

Isto foi feito separadamente para CBO, DIT e LCOM. Assim, cada repositório passou a ter, por métrica, os campos:

- `<metrica>_mean`
- `<metrica>_median`
- `<metrica>_std`

O arquivo completo com essa sumarização por repositório está em:

- `assets/rq01/rq01_resumo_por_repositorio.csv`

### 2.3 Análise estatística

- Popularidade foi tratada como `stars = stargazerCount`.
- Para visualização, também foi usado `log10(stars)` no eixo X dos gráficos.
- Para medir associação entre popularidade e qualidade, foram calculadas correlações de Pearson e Spearman entre `stars` e a **mediana por repositório** de cada métrica (`cbo_median`, `dit_median`, `lcom_median`).

## 3. Resultados

### 3.1 Cobertura dos dados

- Repositórios no dataset consolidado da RQ01: 968.
- Repositórios com valores válidos para as correlações (por métrica): 960.

### 3.2 Correlações (popularidade vs mediana da métrica por repositório)

| Métrica | Pearson | Spearman | n |
| --- | ---: | ---: | ---: |
| CBO | -0.1025 | 0.0304 | 960 |
| DIT | -0.0499 | -0.0336 | 960 |
| LCOM | -0.0208 | 0.0166 | 960 |

Arquivo CSV correspondente:

- `assets/rq01/rq01_correlacoes.csv`

### 3.3 Medidas centrais das estatísticas por repositório

Resumo da distribuição das estatísticas (média, mediana, desvio padrão) calculadas por repositório:

| Métrica | Estatística por repositório | n | Média (entre repositórios) | Mediana (entre repositórios) | Desvio padrão (entre repositórios) |
| --- | --- | ---: | ---: | ---: | ---: |
| CBO | mean | 960 | 5.339 | 5.276 | 1.872 |
| CBO | median | 960 | 3.535 | 3.000 | 1.727 |
| CBO | std | 951 | 6.247 | 6.009 | 2.630 |
| DIT | mean | 960 | 1.451 | 1.388 | 0.343 |
| DIT | median | 960 | 1.090 | 1.000 | 0.302 |
| DIT | std | 951 | 1.058 | 0.769 | 2.178 |
| LCOM | mean | 960 | 116.138 | 23.793 | 1765.278 |
| LCOM | median | 960 | 1.460 | 0.000 | 16.209 |
| LCOM | std | 951 | 3282.823 | 130.539 | 76753.952 |

### 3.4 Gráficos

![CBO](assets/rq01/rq01_cbo_scatter.png)

![DIT](assets/rq01/rq01_dit_scatter.png)

![LCOM](assets/rq01/rq01_lcom_scatter.png)

## 4. Discussão (Hipóteses vs Resultados)

### 4.1 Hipótese 1 (popularidade vs CBO)

Esperava-se uma relação negativa perceptível (mais estrelas, menor CBO). O resultado mostra coeficientes muito próximos de zero (Pearson = -0.1025; Spearman = 0.0304), indicando associação linear e monotônica muito fracas. Há sinal linear levemente negativo, mas sem efeito prático forte.

### 4.2 Hipótese 2 (popularidade vs DIT)

A expectativa de menor DIT em repositórios mais populares também não se confirmou de forma clara. Os coeficientes foram baixos e próximos de zero (Pearson = -0.0499; Spearman = -0.0336), sugerindo ausência de relação consistente.

### 4.3 Hipótese 3 (popularidade vs LCOM)

Para LCOM, os coeficientes também ficaram próximos de zero (Pearson = -0.0208; Spearman = 0.0166). Além disso, os resultados descritivos indicam alta assimetria e presença de outliers em LCOM, o que reforça cautela na interpretação de tendência global.

### 4.4 Síntese da RQ01

Com base nos dados obtidos, a popularidade (estrelas) não apresentou relação forte com as métricas de qualidade analisadas (CBO, DIT, LCOM) quando observadas por meio das medianas por repositório.

Em termos práticos, os resultados sugerem que, nesta amostra, maior popularidade não implica necessariamente melhor (ou pior) qualidade estrutural nessas três dimensões específicas.

## 5. Limitações e Ameaças à Validade (RQ01)

1. Apenas três métricas CK foram consideradas na RQ01 (CBO, DIT, LCOM).
2. Estrelas no GitHub são uma proxy imperfeita de popularidade e podem refletir fatores externos (marketing, domínio, histórico do projeto).
3. Há dados faltantes em parte dos repositórios para algumas estatísticas (especialmente desvios padrão), tipicamente por baixa quantidade de classes válidas.
4. Correlação não implica causalidade.

## 6. Artefatos gerados para a RQ01

- Sumarização por repositório: `assets/rq01/rq01_resumo_por_repositorio.csv`
- Correlações: `assets/rq01/rq01_correlacoes.csv`
- Figuras: `assets/rq01/rq01_cbo_scatter.png`, `assets/rq01/rq01_dit_scatter.png`, `assets/rq01/rq01_lcom_scatter.png`
