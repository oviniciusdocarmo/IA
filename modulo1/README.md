# Análise Paramétrica — AG vs PSO no Caixeiro Viajante (TSP)

## Configuração dos experimentos

| Item | Valor |
|---|---|
| Instância | 20 cidades (instância 2) |
| Execuções por configuração | 20 (seeds `0..19`) |
| Gerações (AG) / Iterações (PSO) | 500 |
| Referência de ótimo | **433.01** — melhor solução encontrada em todas as execuções do AG |
| Script | [`bench.py`](bench.py) — `python bench.py` reproduz todas as tabelas |

**Métricas das tabelas:** `melhor` / `média` / `pior` = distância total da rota (menor é melhor);
`desvio` = desvio-padrão da distância entre as 20 execuções (robustez);
`tempo(s)` = tempo médio por execução;
`conv.` = geração/iteração média em que a melhor solução final foi alcançada pela primeira vez (velocidade de convergência).

Ao variar um parâmetro, os demais ficam fixos nos valores-base:
**AG** `crossover=0.9, mutação=0.02, pop=50, elite=2, seleção=torneio`;
**PSO** `c1=1.0, c2=1.0, w=0.8, pop=50`.

---

## 1. Algoritmo Genético

### 1a) Taxa de recombinação — 0.1 / 0.5 / 0.9

| configuração | melhor | média | desvio | pior | tempo(s) | conv. |
|---|--:|--:|--:|--:|--:|--:|
| crossover = 0.1 | 433.01 | 481.50 | 33.98 | 559.21 | 0.97 | 394 |
| crossover = 0.5 | 433.01 | 463.30 | 19.58 | 509.33 | 1.06 | 326 |
| crossover = 0.9 | 433.01 | 439.29 | 10.11 | 473.69 | 1.15 | 253 |

**Comportamento:** quanto maior a taxa, melhor e mais **consistente** o resultado — a média cai de 481 → 439 e o desvio de 34 → 10. O crossover OX é o principal operador de busca aqui; com taxa baixa o AG depende quase só da mutação por troca (swap), explora pouco e converge tarde (conv. 394). Taxa alta também converge mais cedo, com custo de tempo desprezível.
**Melhor escolha: 0.9.**

### 1b) Taxa de mutação — 0.01 / 0.1 / 0.2

| configuração | melhor | média | desvio | pior | tempo(s) | conv. |
|---|--:|--:|--:|--:|--:|--:|
| mutação = 0.01 | 433.01 | 442.82 | 9.40 | 465.96 | 1.15 | 243 |
| mutação = 0.1 | 433.01 | 441.18 | 11.62 | 482.16 | 1.14 | 294 |
| mutação = 0.2 | 433.01 | 448.27 | 14.41 | 471.13 | 1.16 | 281 |

**Comportamento:** impacto pequeno nesta instância. `0.01` e `0.1` são praticamente equivalentes (média ~441–443); `0.2` piora um pouco (448) e aumenta o desvio — mutação alta demais degrada rotas boas do elitismo, pois a troca é aleatória e sem direção. Tempo estável.
**Melhor escolha: 0.01–0.1.**

### 1c) Tamanho da população — 10 / 50 / 100

| configuração | melhor | média | desvio | pior | tempo(s) | conv. |
|---|--:|--:|--:|--:|--:|--:|
| população = 10 | 444.78 | 498.37 | 30.18 | 547.16 | 0.20 | 348 |
| população = 50 | 433.01 | 439.29 | 10.11 | 473.69 | 1.14 | 253 |
| população = 100 | 433.01 | 441.29 | 12.47 | 465.96 | 2.32 | 121 |

**Comportamento:** `pop=10` é claramente insuficiente — nunca atinge 433.01 (melhor 444.78, média 498). `50` e `100` atingem o ótimo de referência; `100` converge muito mais cedo (conv. 121 vs 253) mas custa **2× o tempo** sem melhorar a média.
**Melhor custo-benefício: 50.**

---

## 2. PSO (discreto, *swap sequences*)

### 2a) Peso social c2 — 0.1 / 1.0 / 2.0

| configuração | melhor | média | desvio | pior | tempo(s) | conv. |
|---|--:|--:|--:|--:|--:|--:|
| social c2 = 0.1 | 530.65 | 668.14 | 49.04 | 743.71 | 0.48 | 254 |
| social c2 = 1.0 | 632.59 | 715.42 | 34.62 | 763.16 | 0.61 | 203 |
| social c2 = 2.0 | 610.26 | 700.48 | 35.25 | 760.20 | 0.65 | 216 |

**Comportamento:** contraintuitivo — `c2` **baixo** (0.1) dá o melhor resultado (média 668) e `c2` alto piora (700–715). Com peso social grande, todas as partículas são puxadas para o `gbest` já nas primeiras iterações, perdem diversidade e ficam presas (convergência prematura). O PSO por sequências de troca é muito sensível a isso.

### 2b) Peso cognitivo c1 — 0.1 / 1.0 / 2.0

| configuração | melhor | média | desvio | pior | tempo(s) | conv. |
|---|--:|--:|--:|--:|--:|--:|
| cognitivo c1 = 0.1 | 569.66 | 682.95 | 55.58 | 764.38 | 0.50 | 308 |
| cognitivo c1 = 1.0 | 632.59 | 715.42 | 34.62 | 763.16 | 0.61 | 203 |
| cognitivo c1 = 2.0 | 638.38 | 711.56 | 31.04 | 748.16 | 0.65 | 213 |

**Comportamento:** mesmo padrão do peso social — `c1` baixo (0.1) é melhor (média 683) que `c1` alto (711–715). Pesos grandes produzem sequências de troca longas por iteração, o passo fica grande demais e o movimento vira quase aleatório, estagnando cedo.

### 2c) Tamanho da população — 10 / 50 / 100

| configuração | melhor | média | desvio | pior | tempo(s) | conv. |
|---|--:|--:|--:|--:|--:|--:|
| população = 10 | 696.58 | 750.26 | 34.93 | 806.12 | 0.12 | 249 |
| população = 50 | 632.59 | 715.42 | 34.62 | 763.16 | 0.61 | 203 |
| população = 100 | 560.52 | 681.26 | 52.57 | 758.00 | 1.21 | 255 |

**Comportamento:** aqui o aumento **ajuda de forma monotônica** (melhor 697 → 632 → 560; média 750 → 715 → 681). Mais partículas = mais diversidade inicial, o que compensa parcialmente a convergência prematura. Tempo cresce quase linear.
**Melhor PSO:** população grande + pesos `c1`/`c2` pequenos — mas ainda assim não alcança o AG.

---

## 3. Análise comparativa (mesma população nos dois algoritmos)

Base: **AG** `crossover=0.9, mutação=0.02`; **PSO** `c1=c2=1.0, w=0.8`; 500 gerações/iterações; 20 execuções.

### 3a) População = 10

| algoritmo | melhor | média | desvio | tempo(s) |
|---|--:|--:|--:|--:|
| **AG** | **444.78** | **498.37** | 30.18 | 0.19 |
| PSO | 696.58 | 750.26 | 34.93 | 0.13 |

O **AG chega muito mais perto** do ótimo (≈445 vs ≈697; referência 433.01). O PSO é ~35 % mais rápido, mas com qualidade muito inferior.
**Vencedor: AG.**

### 3b) População = 50

| algoritmo | melhor | média | desvio | tempo(s) |
|---|--:|--:|--:|--:|
| **AG** | **433.01** | **439.29** | 10.11 | 1.13 |
| PSO | 632.59 | 715.42 | 34.62 | 0.61 |

O **AG atinge a melhor solução conhecida (433.01)** e é muito estável (desvio 10). O PSO fica ~46 % acima, na metade do tempo.
**Vencedor: AG** (o PSO só ganha em tempo).

### 3c) População = 100

| algoritmo | melhor | média | desvio | tempo(s) |
|---|--:|--:|--:|--:|
| **AG** | **433.01** | **441.29** | 12.47 | 2.33 |
| PSO | 560.52 | 681.26 | 52.57 | 1.19 |

O **AG novamente atinge 433.01**. O PSO melhora com mais partículas, mas segue ~29 % acima do ótimo. O AG custa ~2× o tempo do PSO.
**Vencedor: AG.**

---

## Conclusão

- **Qualidade:** o **AG vence em todas as populações testadas** (10, 50 e 100). Já com `pop=50` ele atinge a melhor solução conhecida (433.01) e é muito robusto (desvio ~10). O PSO discreto por *swap sequences* nunca chega perto: fica 29–46 % acima do ótimo mesmo no melhor caso.
- **Tempo:** o **PSO é cerca de 2× mais rápido por execução** (pop=50: PSO ≈0.6 s, AG ≈1.1 s), porque o AG ordena toda a população e aplica OX a cada filho. Essa vantagem não compensa a diferença de qualidade.
- **Parâmetros do AG:** taxa de recombinação alta (0.9) é o fator mais importante — melhora a média e reduz drasticamente a variância. Mutação entre 0.01 e 0.1. População 50 é o melhor custo-benefício; 100 só converge mais cedo, sem ganho de qualidade.
- **Parâmetros do PSO:** ao contrário do esperado, **pesos `c1` e `c2` baixos (≈0.1)** funcionam melhor — pesos altos causam convergência prematura no `gbest` e estagnação. Aumentar a população é o único ajuste que melhora o resultado de forma consistente.
- **Recomendação:** para este TSP, usar o **AG com `crossover=0.9`, `mutação≈0.05`, `pop=50`**. O PSO só seria preferível se o tempo fosse crítico e uma solução ~30 % pior fosse aceitável.
