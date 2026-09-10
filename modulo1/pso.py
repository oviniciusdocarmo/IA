# ============================================================
# PSO (PARTICLE SWARM OPTIMIZATION) PARA O CAIXEIRO VIAJANTE (TSP)
# ============================================================
#
# O PSO clássico trabalha com vetores contínuos. Para o TSP,
# usamos a versão DISCRETA baseada em "sequências de troca"
# (swap sequences), proposta por Wang et al.
#
#   - Posição  (x) : uma rota, ou seja, uma permutação das cidades
#   - Velocidade (v): uma lista de trocas (i, j) a aplicar na rota
#   - pbest   (p)  : melhor rota que a partícula já encontrou
#   - gbest   (g)  : melhor rota encontrada por todo o enxame
#
# Equação de atualização (adaptada):
#
#   v(t+1) = w*v(t)  +  c1*r1*(p - x)  +  c2*r2*(g - x)
#   x(t+1) = x(t) + v(t+1)
#
# onde:
#   (p - x)      -> sequência de trocas que transforma x em p
#   coef * seq   -> mantém cada troca da sequência com prob. = coef
#   seqA + seqB  -> concatenação das sequências de trocas
#   x + v        -> aplica a sequência de trocas v sobre a rota x
# ============================================================

import random
import math
import matplotlib.pyplot as plt

# ============================================================
# DADOS DO PROBLEMA
# ============================================================
# 12 cidades representadas por coordenadas (x, y)

cities = [
    (0, 0),   # Cidade 0
    (2, 6),   # Cidade 1
    (5, 3),   # Cidade 2
    (8, 7),   # Cidade 3
    (6, 1),   # Cidade 4
    (1, 4),   # Cidade 5
    (9, 2),   # Cidade 6
    (4, 8),   # Cidade 7
    (7, 5),   # Cidade 8
    (3, 1),   # Cidade 9
    (10, 6),  # Cidade 10
    (5, 9)    # Cidade 11
]


# ============================================================
# Instancia 2: 20 cidades
# ============================================================

# cities = [
#     (12, 35),   # Cidade 0
#     (45, 68),   # Cidade 1
#     (78, 20),   # Cidade 2
#     (23, 82),   # Cidade 3
#     (91, 55),   # Cidade 4
#     (56, 12),   # Cidade 5
#     (8, 67),    # Cidade 6
#     (34, 25),   # Cidade 7
#     (67, 88),   # Cidade 8
#     (95, 15),   # Cidade 9
#     (15, 5),    # Cidade 10
#     (48, 42),   # Cidade 11
#     (82, 73),   # Cidade 12
#     (5, 30),    # Cidade 13
#     (62, 58),   # Cidade 14
#     (28, 50),   # Cidade 15
#     (73, 8),    # Cidade 16
#     (88, 91),   # Cidade 17
#     (40, 95),   # Cidade 18
#     (100, 45)   # Cidade 19
# ]


NUM_CITIES = len(cities)

# ============================================================
# FUNÇÃO DE DISTÂNCIA
# ============================================================

def distance(city1, city2):

    x1, y1 = city1
    x2, y2 = city2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

# ============================================================
# FITNESS
# ============================================================
# Quanto menor a distância total percorrida, melhor a solução.

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
# OPERAÇÕES COM SEQUÊNCIAS DE TROCA (velocidade)
# ============================================================

def get_swap_sequence(source, target):
    """
    Retorna a lista de trocas (i, j) que transforma a rota
    'source' na rota 'target'. Corresponde à operação (target - source).
    """

    source = source.copy()
    swaps = []

    for i in range(NUM_CITIES):

        # Se a cidade nesta posição já está correta, segue em frente
        if source[i] == target[i]:
            continue

        # Descobre onde está, em 'source', a cidade que deveria
        # ocupar a posição i
        j = source.index(target[i])

        # Registra a troca e a aplica em 'source'
        swaps.append((i, j))
        source[i], source[j] = source[j], source[i]

    return swaps


def apply_swap_sequence(route, swaps):
    """
    Aplica, na ordem, todas as trocas (i, j) sobre a rota.
    Corresponde à operação (rota + velocidade).
    """

    route = route.copy()

    for i, j in swaps:
        route[i], route[j] = route[j], route[i]

    return route


def multiply_swap_sequence(swaps, factor):
    """
    Multiplica um coeficiente por uma sequência de trocas:
    cada troca é mantida com probabilidade igual a 'factor'.

      factor >= 1  -> mantém toda a sequência
      factor <= 0  -> descarta toda a sequência
    """

    if factor >= 1:
        return list(swaps)

    if factor <= 0:
        return []

    return [
        swap
        for swap in swaps
        if random.random() < factor
    ]

# ============================================================
# PARTÍCULA
# ============================================================

class Particle:

    def __init__(self):

        # Posição = rota aleatória (permutação das cidades)
        self.position = list(range(NUM_CITIES))
        random.shuffle(self.position)

        # Velocidade = sequência de trocas (inicialmente vazia)
        self.velocity = []

        # Melhor posição pessoal (pbest)
        self.best_position = self.position.copy()
        self.best_distance = fitness(self.position)

# ============================================================
# ENXAME INICIAL
# ============================================================

def create_swarm(num_particles):

    return [
        Particle()
        for _ in range(num_particles)
    ]

# ============================================================
# VISUALIZAÇÃO DA ROTA
# ============================================================

def plot_route(route, title):

    x = [cities[i][0] for i in route]
    y = [cities[i][1] for i in route]

    # Retorna à cidade inicial para fechar o ciclo
    x.append(x[0])
    y.append(y[0])

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o')

    # Identificação das cidades
    for i, (cx, cy) in enumerate(cities):
        plt.text(cx, cy, f"  {i}", fontsize=12)

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()

    plt.show()

# ============================================================
# PSO - PROBLEMA DO CAIXEIRO VIAJANTE
# ============================================================

def pso(
    num_particles=30,
    iterations=500,
    w=0.8,
    c1=1.0,
    c2=1.0
):

    # --------------------------------------------------------
    # 1. Criar enxame inicial
    # --------------------------------------------------------

    swarm = create_swarm(num_particles)

    # --------------------------------------------------------
    # 2. Inicializar o melhor global (gbest)
    # --------------------------------------------------------

    global_best_position = None
    global_best_distance = float("inf")

    for particle in swarm:

        if particle.best_distance < global_best_distance:
            global_best_distance = particle.best_distance
            global_best_position = particle.best_position.copy()

    history = []

    # --------------------------------------------------------
    # 3. Repetir até satisfazer o critério de parada
    # --------------------------------------------------------

    for _ in range(iterations):

        for particle in swarm:

            # ------------------------------------------------
            # 3.1 Calcular a nova velocidade
            #
            # v = w*v  +  c1*r1*(pbest - x)  +  c2*r2*(gbest - x)
            # ------------------------------------------------

            r1 = random.random()
            r2 = random.random()

            # Componente de inércia
            inertia = multiply_swap_sequence(
                particle.velocity,
                w
            )

            # Componente cognitiva (rumo ao pbest)
            cognitive = multiply_swap_sequence(
                get_swap_sequence(
                    particle.position,
                    particle.best_position
                ),
                c1 * r1
            )

            # Componente social (rumo ao gbest)
            social = multiply_swap_sequence(
                get_swap_sequence(
                    particle.position,
                    global_best_position
                ),
                c2 * r2
            )

            particle.velocity = inertia + cognitive + social

            # ------------------------------------------------
            # 3.2 Atualizar a posição
            #
            # x = x + v
            # ------------------------------------------------

            particle.position = apply_swap_sequence(
                particle.position,
                particle.velocity
            )

            # ------------------------------------------------
            # 3.3 Avaliar e atualizar pbest / gbest
            # ------------------------------------------------

            current_distance = fitness(particle.position)

            if current_distance < particle.best_distance:

                particle.best_distance = current_distance
                particle.best_position = particle.position.copy()

                if current_distance < global_best_distance:

                    global_best_distance = current_distance
                    global_best_position = particle.position.copy()

        history.append(global_best_distance)

    return (
        global_best_position,
        global_best_distance,
        history
    )

# ============================================================
# EXECUÇÃO DO PROGRAMA
# ============================================================

print("=" * 60)
print("PSO - PROBLEMA DO CAIXEIRO VIAJANTE")
print("=" * 60)

NUM_PARTICLES = 30
ITERATIONS = 500
W = 0.8
C1 = 1.0
C2 = 1.0

print("\nParâmetros:")
print(f"  Partículas .......... {NUM_PARTICLES}")
print(f"  Iterações ........... {ITERATIONS}")
print(f"  Inércia (w) ......... {W}")
print(f"  Coef. cognitivo (c1)  {C1}")
print(f"  Coef. social (c2) ... {C2}")

best_route, best_distance, history = pso(
    num_particles=NUM_PARTICLES,
    iterations=ITERATIONS,
    w=W,
    c1=C1,
    c2=C2
)

# ============================================================
# RESULTADO
# ============================================================

print("\n" + "=" * 60)
print("RESULTADO")
print("=" * 60)

print("\nMelhor rota:")
print(best_route)

print(f"\nDistância total: {best_distance:.2f}")

# ============================================================
# VISUALIZAR MELHOR ROTA
# ============================================================

plot_route(
    best_route,
    "Melhor rota encontrada pelo PSO"
)

# ============================================================
# EVOLUÇÃO DO FITNESS
# ============================================================

plt.figure(figsize=(8, 5))
plt.plot(history)
plt.xlabel("Iteração")
plt.ylabel("Melhor distância")
plt.title("Evolução da solução ao longo das iterações")
plt.grid()
plt.show()
