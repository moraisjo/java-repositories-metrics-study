# RQ01 - Relação entre Popularidade e Características de Qualidade

## 1. Introdução e Hipóteses Informais

A RQ01 analisa se repositórios Java mais populares (com mais estrelas no GitHub) tendem a ter melhor qualidade de código.

Hipóteses informais adotadas antes da análise:

Neste estudo: CBO indica acoplamento entre classes, DIT indica profundidade de herança e LCOM indica falta de coesão entre métodos.

1. H1: Repositórios mais populares tenderiam a ter menor acoplamento (CBO), pois recebem mais revisão da comunidade.
2. H2: Repositórios mais populares tenderiam a ter menor profundidade de herança (DIT), por priorizarem manutenção mais simples.
3. H3: Repositórios mais populares tenderiam a ter menor falta de coesão (LCOM), por terem organização interna melhor.

## 2. Metodologia

### 2.1 Coleta e preparação dos dados

- Fonte de popularidade: `stargazerCount` (GitHub API).
- Fonte de qualidade: métricas CK por classe (`cbo`, `dit`, `lcom`).
- Unidade analítica da RQ01: repositório.

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

- `assets/rq01/rq01_resumo_por_repositorio.csv`

### 2.3 Análise estatística

- Popularidade foi considerada como `stars = stargazerCount`.
- Para facilitar a visualização, foi usado `log10(stars)` no eixo X dos gráficos.
- Para medir a relação entre popularidade e qualidade, foram calculadas correlações de Pearson e Spearman entre `stars` e a **mediana por repositório** de cada métrica (`cbo_median`, `dit_median`, `lcom_median`).
- Também foi calculado o p-valor de cada correlação, para apoiar a interpretação estatística dos resultados.

## 3. Resultados

### 3.1 Cobertura dos dados

- Repositórios no dataset consolidado da RQ01: 968.
- Repositórios com valores válidos para as correlações (por métrica): 960.

### 3.2 Correlações (popularidade vs mediana da métrica por repositório)

Pense no p-valor como um “termômetro de coincidência”. Ele responde: “Se não existisse relação nenhuma entre as coisas que estou comparando, qual seria a chance de eu ver um resultado como este só por acaso?”

> p-valor pequeno
Significa: “seria raro acontecer só por sorte”.
Então a gente começa a acreditar que pode existir relação de verdade.

> p-valor grande
Significa: “isso pode acontecer por sorte sem problema”.
Então não dá para afirmar que existe relação.


| Métrica | Pearson | p-valor (Pearson) | Spearman | p-valor (Spearman) | n |
| --- | ---: | ---: | ---: | ---: | ---: |
| CBO | -0.1025 | 0.0015 | 0.0304 | 0.3471 | 960 |
| DIT | -0.0499 | 0.1227 | -0.0336 | 0.2983 | 960 |
| LCOM | -0.0208 | 0.5196 | 0.0166 | 0.6083 | 960 |

Considerando nível de significância de 5% (0,05), apenas o p-valor de Pearson para CBO ficou abaixo desse limite. Mesmo assim, o coeficiente é pequeno em magnitude, indicando efeito fraco.

**ATENÇÃO**
- p-valor fala de confiança contra o acaso; 
- coeficiente fala de tamanho da relação.**

Arquivo CSV correspondente:

- `assets/rq01/rq01_correlacoes.csv`

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

### 3.4 Gráficos

![CBO](assets/rq01/rq01_cbo_scatter.png)

Fig. 1: Relação entre popularidade e acoplamento entre classes (CBO). Cada ponto representa um repositório. No eixo X, valores maiores indicam mais estrelas (em escala log10). No eixo Y, valores maiores indicam maior acoplamento entre classes. A linha vermelha resume a tendência geral e aparece levemente descendente, sugerindo que repositórios mais populares podem ter CBO um pouco menor, mas com efeito fraco.

![DIT](assets/rq01/rq01_dit_scatter.png)

Fig. 2: Relação entre popularidade e profundidade de herança (DIT). Cada ponto é um repositório; à direita estão os mais populares e, acima, os com maior profundidade de herança. A linha vermelha está quase horizontal, indicando que o aumento de popularidade não acompanha uma mudança relevante em DIT. Em termos práticos, o gráfico sugere relação fraca entre essas variáveis.

![LCOM](assets/rq01/rq01_lcom_scatter.png)

Fig. 3: Relação entre popularidade e falta de coesão entre métodos (LCOM). Cada ponto representa um repositório; quanto mais alto, maior a falta de coesão. A linha vermelha quase horizontal indica tendência geral fraca. Também há pontos muito acima da nuvem principal (outliers), mostrando que alguns repositórios têm valores de LCOM muito elevados em comparação com a maioria.

## 4. Discussão (Hipóteses vs Resultados)

### 4.1 Hipótese 1 (popularidade vs CBO)

Era esperado que mais estrelas viessem com menor CBO. Porém, os coeficientes ficaram muito próximos de zero (Pearson = -0.1025; Spearman = 0.0304). Isso indica relação fraca. Existe um sinal linear levemente negativo, mas sem diferença relevante na prática.

### 4.2 Hipótese 2 (popularidade vs DIT)

A expectativa de menor DIT em repositórios mais populares também não se confirmou com clareza. Os coeficientes foram baixos e próximos de zero (Pearson = -0.0499; Spearman = -0.0336). Isso sugere ausência de relação consistente.

### 4.3 Hipótese 3 (popularidade vs LCOM)

Para LCOM, os coeficientes também ficaram próximos de zero (Pearson = -0.0208; Spearman = 0.0166). Além disso, os resultados descritivos mostram alta assimetria e presença de outliers em LCOM. Por isso, a interpretação da tendência geral deve ser feita com cautela.

### 4.4 Síntese da RQ01

Com base nos dados, a popularidade (estrelas) não mostrou relação forte com as métricas analisadas (CBO, DIT e LCOM), considerando as medianas por repositório.

Na prática, os resultados sugerem que, nesta amostra, mais popularidade não significa necessariamente melhor (nem pior) qualidade estrutural nessas três dimensões.

## 5. Limitações e Ameaças à Validade (RQ01)

1. Apenas três métricas CK foram consideradas na RQ01 (CBO, DIT, LCOM).
2. Estrelas no GitHub são uma medida aproximada de popularidade e podem refletir fatores externos (marketing, domínio e histórico do projeto).
3. Há dados faltantes em parte dos repositórios para algumas estatísticas (principalmente desvios padrão), geralmente por baixa quantidade de classes válidas.
4. Correlação não implica causalidade.

## 6. Artefatos gerados para a RQ01

- Sumarização por repositório: `assets/rq01/rq01_resumo_por_repositorio.csv`
- Correlações: `assets/rq01/rq01_correlacoes.csv`
- Figuras: `assets/rq01/rq01_cbo_scatter.png`, `assets/rq01/rq01_dit_scatter.png`, `assets/rq01/rq01_lcom_scatter.png`
