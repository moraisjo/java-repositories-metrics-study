# RQ02 - Relação entre Maturidade do Repositório e Características de Qualidade

## 1. Introdução e Hipóteses Informais

A RQ02 analisa se repositórios Java mais maduros (com maior idade em anos) tendem a apresentar melhor qualidade de código.

Conceitos:
a. CBO: acoplamento entre classes,
b. DIT: profundidade de herança,
c. LCOM: falta de coesão entre métodos.

Hipóteses informais adotadas antes da análise:
1. H1: Repositórios mais maduros tenderiam a ter menor acoplamento (CBO), por acumular refatorações ao longo do tempo.
2. H2: Repositórios mais maduros tenderiam a ter menor profundidade de herança (DIT), por priorizarem manutenção mais simples.
3. H3: Repositórios mais maduros tenderiam a ter menor falta de coesão (LCOM), por evoluírem com melhor organização interna.

## 2. Metodologia

### 2.1 Coleta e preparação dos dados

- Fonte de maturidade: `age` (idade em dias) convertido para anos (`age_years = age / 365.25`).
- Fonte de qualidade: métricas CK por classe (`cbo`, `dit`, `lcom`).
- Unidade analítica da RQ02: repositório.

Foram usados apenas os repositórios com `ckMetricsGenerated=true`.

### 2.2 Sumarização por repositório

Para cada repositório, as métricas CK em nível de classe foram agregadas por:

- média;
- mediana;
- desvio padrão amostral.

Esse cálculo foi feito separadamente para CBO, DIT e LCOM. Assim, cada repositório ficou com os campos:

- `<metrica>_mean`
- `<metrica>_median`
- `<metrica>_std`

O arquivo completo com essa sumarização por repositório está em:

- `assets/rq02/rq02_resumo_por_repositorio.csv`

### 2.3 Análise estatística

- Maturidade foi considerada como `maturity_years = age_years`.
- Para medir a relação entre maturidade e qualidade, foram calculadas correlações de Pearson e Spearman entre `maturity_years` e a **mediana por repositório** de cada métrica (`cbo_median`, `dit_median`, `lcom_median`).
- Também foi calculado o p-valor de cada correlação, para apoiar a interpretação estatística dos resultados.

## 3. Resultados

### 3.1 Cobertura dos dados

- Repositórios no dataset consolidado da RQ02: 968.
- Repositórios com valores válidos para as correlações (por métrica): 960.

### 3.2 Correlações (maturidade vs mediana da métrica por repositório)

Pense no p-valor como um "termômetro de coincidência". Ele responde: "Se não existisse relação nenhuma entre as coisas que estou comparando, qual seria a chance de eu ver um resultado como este só por acaso?"

> p-valor pequeno
Significa: "seria raro acontecer só por sorte".
Então a gente começa a acreditar que pode existir relação de verdade.

> p-valor grande
Significa: "isso pode acontecer por sorte sem problema".
Então não dá para afirmar que existe relação.

| Métrica | Pearson | p-valor (Pearson) | Spearman | p-valor (Spearman) | n |
| --- | ---: | ---: | ---: | ---: | ---: |
| CBO | 0.0099 | 0.7590 | 0.0229 | 0.4783 | 960 |
| DIT | 0.0871 | 0.0069 | 0.0959 | 0.0029 | 960 |
| LCOM | 0.0161 | 0.6183 | 0.0852 | 0.0082 | 960 |

Considerando nível de significância de 5% (0,05):

- DIT apresentou associação positiva fraca com maturidade em Pearson e Spearman.
- LCOM apresentou associação positiva fraca apenas em Spearman.
- CBO não apresentou evidência estatística de associação.

Mesmo nos casos com p-valor abaixo de 0,05, os coeficientes são pequenos em magnitude, indicando efeito fraco.

**ATENÇÃO**
- p-valor fala de confiança contra o acaso;
- coeficiente fala de tamanho da relação.

Arquivo CSV correspondente:

- `assets/rq02/rq02_correlacoes.csv`

### 3.3 Medidas centrais das estatísticas por repositório

Resumo das estatísticas (média, mediana e desvio padrão) calculadas por repositório:

| Métrica | Descrição métrica | Estatística por repositório | n | Média (entre repositórios) | Mediana (entre repositórios) | Desvio padrão (entre repositórios) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| CBO | Acoplamento entre classes | mean | 960 | 5.339 | 5.276 | 1.872 |
| CBO | Acoplamento entre classes | median | 960 | 3.535 | 3.000 | 1.727 |
| CBO | Acoplamento entre classes | std | 951 | 6.247 | 6.009 | 2.630 |
| DIT | Profundidade de herança | mean | 960 | 1.451 | 1.388 | 0.343 |
| DIT | Profundidade de herança | median | 960 | 1.090 | 1.000 | 0.302 |
| DIT | Profundidade de herança | std | 951 | 1.058 | 0.769 | 2.178 |
| LCOM | Falta de coesão entre métodos | mean | 960 | 116.138 | 23.793 | 1765.278 |
| LCOM | Falta de coesão entre métodos | median | 960 | 1.460 | 0.000 | 16.209 |
| LCOM | Falta de coesão entre métodos | std | 951 | 3282.823 | 130.539 | 76753.952 |

### 3.4 Gráficos (diagramas de dispersão)

![CBO](assets/rq02/rq02_cbo_scatter.png)

Fig. 1: Relação entre maturidade (idade em anos) e acoplamento entre classes (CBO). Cada ponto representa um repositório. No eixo X, valores maiores indicam repositórios mais maduros. A linha vermelha aparece praticamente horizontal, indicando ausência de tendência relevante entre maturidade e CBO.

![DIT](assets/rq02/rq02_dit_scatter.png)

Fig. 2: Relação entre maturidade (idade em anos) e profundidade de herança (DIT). A linha vermelha mostra leve inclinação positiva, consistente com correlações positivas fracas. Em termos práticos, o efeito observado é pequeno.

![LCOM](assets/rq02/rq02_lcom_scatter.png)

Fig. 3: Relação entre maturidade (idade em anos) e falta de coesão entre métodos (LCOM). A linha de tendência é discretamente positiva, mas há alta dispersão e presença de outliers, o que recomenda cautela na interpretação.

## 4. Discussão (Hipóteses vs Resultados)

### 4.1 Hipótese 1 (maturidade vs CBO)

A hipótese de menor CBO em repositórios mais maduros não se confirmou. Os coeficientes ficaram próximos de zero (Pearson = 0.0099; Spearman = 0.0229), sem significância estatística. Isso sugere ausência de relação consistente entre maturidade e CBO nesta amostra.

### 4.2 Hipótese 2 (maturidade vs DIT)

A expectativa de menor DIT em repositórios mais maduros também não se confirmou no sinal esperado. As correlações foram positivas e fracas (Pearson = 0.0871; Spearman = 0.0959), ambas com p-valor abaixo de 0,05. Há evidência estatística de associação, mas com tamanho de efeito pequeno.

### 4.3 Hipótese 3 (maturidade vs LCOM)

Para LCOM, Pearson ficou próximo de zero (0.0161), enquanto Spearman foi positivo e fraco (0.0852), com p-valor abaixo de 0,05. Isso indica possível tendência monotônica fraca. Contudo, a forte assimetria e os outliers de LCOM exigem interpretação conservadora.

### 4.4 Síntese da RQ02

Com base nos dados, a maturidade do repositório (idade em anos) mostrou, no máximo, relações fracas com as métricas de qualidade analisadas (CBO, DIT e LCOM), considerando as medianas por repositório.

Na prática, os resultados sugerem que ser mais antigo não implica necessariamente melhor (nem pior) qualidade estrutural nessas três dimensões.

## 5. Limitações e Ameaças à Validade (RQ02)

1. Apenas três métricas CK foram consideradas na RQ02 (CBO, DIT, LCOM).
2. Idade do repositório é uma proxy de maturidade e não captura diretamente fatores como volume de refatoração, churn e governança.
3. Há dados faltantes em parte dos repositórios para algumas estatísticas (principalmente desvios padrão), geralmente por baixa quantidade de classes válidas.
4. LCOM apresenta forte assimetria e outliers, afetando interpretação em métodos sensíveis à escala.
5. Correlação não implica causalidade.

## 6. Artefatos gerados para a RQ02

- Sumarização por repositório: `assets/rq02/rq02_resumo_por_repositorio.csv`
- Correlações: `assets/rq02/rq02_correlacoes.csv`
- Figuras: `assets/rq02/rq02_cbo_scatter.png`, `assets/rq02/rq02_dit_scatter.png`, `assets/rq02/rq02_lcom_scatter.png`
