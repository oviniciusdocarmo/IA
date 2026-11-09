# ============================================================
# ALGORITMO GENÉTICO PARA O PROBLEMA DO CAIXEIRO VIAJANTE (TSP)
# ============================================================

import random
import math
import matplotlib.pyplot as plt

# ============================================================
# DADOS DO PROBLEMA
# ============================================================
# 12 cidades representadas por coordenadas (x, y)

# cities = [
# (0, 0), # Cidade 0
# (2, 6), # Cidade 1
# (5, 3), # Cidade 2
# (8, 7), # Cidade 3
# (6, 1), # Cidade 4
# (1, 4), # Cidade 5
# (9, 2), # Cidade 6
# (4, 8), # Cidade 7
# (7, 5), # Cidade 8
# (3, 1), # Cidade 9
# (10, 6), # Cidade 10
# (5, 9) # Cidade 11
# ]

cities = [
    (12, 35),   # Cidade 0
    (45, 68),   # Cidade 1
    (78, 20),   # Cidade 2
    (23, 82),   # Cidade 3
    (91, 55),   # Cidade 4
    (56, 12),   # Cidade 5
    (8, 67),    # Cidade 6
    (34, 25),   # Cidade 7
    (67, 88),   # Cidade 8
    (95, 15),   # Cidade 9
    (15, 5),    # Cidade 10
    (48, 42),   # Cidade 11
    (82, 73),   # Cidade 12
    (5, 30),    # Cidade 13
    (62, 58),   # Cidade 14
    (28, 50),   # Cidade 15
    (73, 8),    # Cidade 16
    (88, 91),   # Cidade 17
    (40, 95),   # Cidade 18
    (100, 45)   # Cidade 19
]

NUM_CITIES = len(cities)

# ============================================================
# FUNÇÃO DE DISTÂNCIA
# ============================================================

def distance(city1, city2):
  x1, y1 = city1
  x2, y2 = city2

  return math.sqrt(
    (x2 - x1)**2 +
    (y2 - y1)**2
)
# ============================================================
# FITNESS
# ============================================================
# Quanto menor a distância total, melhor é a solução.

def fitness(route):

    total_distance = 0

    for i in range(NUM_CITIES):

        current_city = route[i]

        next_city = route[
            (i + 1) % NUM_CITIES
        ]

        total_distance += distance(
            cities[current_city],
            cities[next_city]
        )

    return total_distance
# ============================================================
# POPULAÇÃO INICIAL
# ============================================================

def create_population(population_size):

    population = []

    for _ in range(population_size):

        # Cria uma rota contendo todas as cidades
        route = list(range(NUM_CITIES))

        # Embaralha a rota aleatoriamente
        random.shuffle(route)

        population.append(route)

    return population
# ============================================================
# SELEÇÃO POR TORNEIO
# ============================================================

def tournament_selection(
population,
tournament_size=3):

# Seleciona aleatoriamente alguns indivíduos
  candidates = random.sample(
    population,
    tournament_size
)

# O indivíduo com menor distância vence
  winner = min(
    candidates,
    key=fitness
)

# Retorna uma cópia do vencedor
  return winner.copy()
# ============================================================
# SELEÇÃO POR ROLETA
# ============================================================
# Na roleta, indivíduos melhores recebem maior probabilidade
# de serem selecionados.


# Como nosso fitness representa uma DISTÂNCIA, valores menores
# são melhores. Por isso, precisamos transformar a distância
# em uma medida de aptidão.


# Uma possibilidade simples é:


# aptidão = 1 / distância


# Assim:


# distância pequena -> aptidão grande
# distância grande -> aptidão pequena
def roulette_selection(population):

    # Calcula a aptidão de cada indivíduo
    fitness_values = [
        1 / fitness(individual)
        for individual in population
    ]

    # Soma das aptidões
    total_fitness = sum(
        fitness_values
    )

    # Escolhe aleatoriamente um ponto
    # dentro da soma das aptidões
    selection_point = random.uniform(
        0,
        total_fitness
    )

    cumulative = 0

    # Percorre a população acumulando
    # as probabilidades
    for individual, individual_fitness in zip(
        population,
        fitness_values
    ):

        cumulative += individual_fitness

        if cumulative >= selection_point:

            return individual.copy()

    # Segurança contra possíveis erros
    return population[-1].copy()


# ============================================================
# FUNÇÃO DE SELEÇÃO
# ============================================================

# Esta função permite escolher qual estratégia será utilizada.

def select_parent(
    population,
    selection_method
):

    if selection_method == "torneio":

        return tournament_selection(
            population
        )

    elif selection_method == "roleta":

        return roulette_selection(
            population
        )

    else:

        raise ValueError(
            "Método de seleção inválido."
        )
# ============================================================
# CROSSOVER - ORDER CROSSOVER (OX)
# ============================================================

def crossover(parent1, parent2):

  size = len(parent1)

# Escolhe dois pontos de corte
  start, end = sorted(random.sample(range(size),2))

# Inicialmente, o filho está vazio
  child = [None] * size

# Copia uma parte do primeiro pai
  child[start:end] = parent1[start:end]

# Identifica os elementos do segundo pai
# que ainda não estão no filho
  remaining = [
    city
    for city in parent2
    if city not in child
]

  position = end

# Insere os elementos restantes
  for city in remaining:

    if position >= size:
        position = 0

    while child[position] is not None:

        position = (
            position + 1
        ) % size

    child[position] = city

  return child
# ============================================================
# MUTAÇÃO - SWAP
# ============================================================

def mutation(
route,
mutation_rate):

  route = route.copy()

# Decide se ocorrerá mutação
  if random.random() < mutation_rate:

    # Escolhe duas posições
    i, j = random.sample(
        range(NUM_CITIES),
        2
    )

    # Troca as duas cidades
    route[i], route[j] = \
        route[j], route[i]

  return route
# ============================================================
# VISUALIZAÇÃO DA ROTA
# ============================================================

def plot_route(
route,
title):

  x = [
    cities[i][0]
    for i in route
]

  y = [
    cities[i][1]
    for i in route
]

# Retorna à cidade inicial
  x.append(x[0])
  y.append(y[0])

  plt.figure(
    figsize=(8, 6)
)

  plt.plot(
    x,
    y,
    marker='o'
)

# Identificação das cidades
  for i, (cx, cy) in enumerate(cities):

    plt.text(
        cx,
        cy,
        f"  {i}",
        fontsize=12
    )

  plt.title(title)
  plt.xlabel("X")
  plt.ylabel("Y")
  plt.grid()

  plt.show()
# ============================================================
# ALGORITMO GENÉTICO
# ============================================================

def genetic_algorithm(

    population_size=10,

    generations=500,

    mutation_rate=0.02,

    crossover_rate=0.90,

    elite_size=2,

    selection_method="torneio"):

# --------------------------------------------------------
# 1. Criar população inicial
# --------------------------------------------------------

  population = create_population(population_size)

  best_route = None

  best_distance = float("inf")

  history = []


# --------------------------------------------------------
# 2. Evolução
# --------------------------------------------------------

  for generation in range(
        generations):

    # Avaliar população
    population.sort(
        key=fitness
    )

    # Melhor solução da geração
    current_best = population[0]

    current_distance = fitness(
        current_best
    )

    # Atualizar melhor solução global
    if current_distance < best_distance:

        best_distance = \
            current_distance

        best_route = \
            current_best.copy()

    history.append(
        best_distance
    )


    # ----------------------------------------------------
    # 3. Elitismo
    # ----------------------------------------------------

    new_population = [

        individual.copy()

        for individual in
        population[:elite_size]

    ]


    # ----------------------------------------------------
    # 4. Gerar descendentes
    # ----------------------------------------------------

    while len(new_population) < \
            population_size:

        # Seleção do primeiro pai
        parent1 = select_parent(
            population,
            selection_method
        )

        # Seleção do segundo pai
        parent2 = select_parent(
            population,
            selection_method
        )


        # ------------------------------------------------
        # Crossover
        # ------------------------------------------------

        if random.random() < \
                crossover_rate:

            child = crossover(
                parent1,
                parent2
            )

        else:

            child = parent1.copy()


        # ------------------------------------------------
        # Mutação
        # ------------------------------------------------

        child = mutation(
            child,
            mutation_rate
        )


        # Adicionar filho à nova população
        new_population.append(
            child
        )


    # ----------------------------------------------------
    # 5. Substituir população
    # ----------------------------------------------------

    population = new_population


  return (
    best_route,
    best_distance,
    history
)
# ============================================================
# EXECUÇÃO DO PROGRAMA
# ============================================================

print("=" * 60)
print("ALGORITMO GENÉTICO - PROBLEMA DO CAIXEIRO VIAJANTE")
print("=" * 60)

print("\nEscolha o método de seleção:")
print("1 - Torneio")
print("2 - Roleta")

selection_option = input(
"\nDigite sua opção (1 ou 2): "
)

if selection_option == "1":

  selection_method = "torneio"

elif selection_option == "2":

  selection_method = "roleta"

else:

  print(
    "Opção inválida. "
    "Será utilizado o método de torneio."
)

selection_method = "torneio"

# ============================================================
# EXECUTAR O ALGORITMO
# ============================================================

best_route, best_distance, history = genetic_algorithm(
    population_size=10,
    generations=500,
    mutation_rate=0.02,
    crossover_rate=0.90,
    elite_size=2,
    selection_method=selection_method
)
# ============================================================
# RESULTADO
# ============================================================

print("\n" + "=" * 60)
print("RESULTADO")
print("=" * 60)

print(
"\nMétodo de seleção:",
selection_method
)

print(
"\nMelhor rota:"
)

print(
best_route
)

print(
f"\nDistância total: "
f"{best_distance:.2f}"
)

# ============================================================
# VISUALIZAR MELHOR ROTA
# ============================================================

plot_route(

best_route,

"Melhor rota encontrada pelo "
"Algoritmo Genético"

)

# ============================================================
# EVOLUÇÃO DO FITNESS
# ============================================================

plt.figure(
figsize=(8, 5)
)

plt.plot(
history
)

plt.xlabel(
"Geração"
)

plt.ylabel(
"Melhor distância"
)

plt.title(
"Evolução da solução ao longo "
"das gerações"
)

plt.grid()

plt.show()