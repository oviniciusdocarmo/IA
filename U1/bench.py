# ============================================================
# BENCHMARK / ANÁLISE PARAMÉTRICA  -  AG  vs  PSO  (TSP)
# ============================================================
#
# Reimplementa o núcleo de ag.py e pso.py (sem input()/plots)
# para permitir execuções repetidas e medição de tempo.
#
# Instância utilizada: 20 cidades (instância 2).
#
# Uso:  python bench.py
# ============================================================

import random
import math
import time
import statistics

# ============================================================
# INSTÂNCIA - 20 CIDADES
# ============================================================

cities = [
    (12, 35), (45, 68), (78, 20), (23, 82), (91, 55),
    (56, 12), (8, 67),  (34, 25), (67, 88), (95, 15),
    (15, 5),  (48, 42), (82, 73), (5, 30),  (62, 58),
    (28, 50), (73, 8),  (88, 91), (40, 95), (100, 45),
]

NUM_CITIES = len(cities)

REPS = 20          # execuções independentes por configuração
ITERS = 500        # gerações (AG) == iterações (PSO)


# ============================================================
# FUNÇÕES COMUNS
# ============================================================

def distance(c1, c2):
    return math.hypot(c2[0] - c1[0], c2[1] - c1[1])


def fitness(route):
    total = 0.0
    for i in range(NUM_CITIES):
        total += distance(cities[route[i]], cities[route[(i + 1) % NUM_CITIES]])
    return total


# ============================================================
# ALGORITMO GENÉTICO
# ============================================================

def tournament_selection(population, k=3):
    return min(random.sample(population, k), key=fitness).copy()


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    remaining = [c for c in parent2 if c not in child]
    pos = end
    for c in remaining:
        if pos >= size:
            pos = 0
        while child[pos] is not None:
            pos = (pos + 1) % size
        child[pos] = c
    return child


def mutation(route, rate):
    route = route.copy()
    if random.random() < rate:
        i, j = random.sample(range(NUM_CITIES), 2)
        route[i], route[j] = route[j], route[i]
    return route


def genetic_algorithm(population_size=50, generations=ITERS,
                      mutation_rate=0.02, crossover_rate=0.9, elite_size=2):

    population = []
    for _ in range(population_size):
        r = list(range(NUM_CITIES))
        random.shuffle(r)
        population.append(r)

    best_route, best_distance = None, float("inf")
    history = []

    for _ in range(generations):
        population.sort(key=fitness)
        d = fitness(population[0])
        if d < best_distance:
            best_distance = d
            best_route = population[0].copy()
        history.append(best_distance)

        new_pop = [ind.copy() for ind in population[:elite_size]]
        while len(new_pop) < population_size:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            child = crossover(p1, p2) if random.random() < crossover_rate else p1.copy()
            child = mutation(child, mutation_rate)
            new_pop.append(child)
        population = new_pop

    return best_route, best_distance, history


# ============================================================
# PSO DISCRETO (swap sequences)
# ============================================================

def get_swap_sequence(source, target):
    source = source.copy()
    swaps = []
    for i in range(NUM_CITIES):
        if source[i] == target[i]:
            continue
        j = source.index(target[i])
        swaps.append((i, j))
        source[i], source[j] = source[j], source[i]
    return swaps


def apply_swap_sequence(route, swaps):
    route = route.copy()
    for i, j in swaps:
        route[i], route[j] = route[j], route[i]
    return route


def mul_swaps(swaps, factor):
    if factor >= 1:
        return list(swaps)
    if factor <= 0:
        return []
    return [s for s in swaps if random.random() < factor]


def pso(num_particles=50, iterations=ITERS, w=0.8, c1=1.0, c2=1.0):

    positions, velocities = [], []
    pbest_pos, pbest_dist = [], []
    for _ in range(num_particles):
        p = list(range(NUM_CITIES))
        random.shuffle(p)
        positions.append(p)
        velocities.append([])
        pbest_pos.append(p.copy())
        pbest_dist.append(fitness(p))

    gbest_dist = min(pbest_dist)
    gbest_pos = pbest_pos[pbest_dist.index(gbest_dist)].copy()
    history = []

    for _ in range(iterations):
        for i in range(num_particles):
            r1, r2 = random.random(), random.random()
            inertia = mul_swaps(velocities[i], w)
            cognitive = mul_swaps(get_swap_sequence(positions[i], pbest_pos[i]), c1 * r1)
            social = mul_swaps(get_swap_sequence(positions[i], gbest_pos), c2 * r2)
            velocities[i] = inertia + cognitive + social
            positions[i] = apply_swap_sequence(positions[i], velocities[i])

            d = fitness(positions[i])
            if d < pbest_dist[i]:
                pbest_dist[i] = d
                pbest_pos[i] = positions[i].copy()
                if d < gbest_dist:
                    gbest_dist = d
                    gbest_pos = positions[i].copy()
        history.append(gbest_dist)

    return gbest_pos, gbest_dist, history


# ============================================================
# INFRAESTRUTURA DE EXPERIMENTO
# ============================================================

def run_many(fn, label, **kwargs):
    """Executa fn REPS vezes com seeds 0..REPS-1 e agrega resultados."""
    dists, times, convergence = [], [], []
    for seed in range(REPS):
        random.seed(seed)
        t0 = time.perf_counter()
        _, dist, history = fn(**kwargs)
        elapsed = time.perf_counter() - t0
        dists.append(dist)
        times.append(elapsed)
        # geração/iteração em que o gbest atual foi alcançado
        convergence.append(history.index(history[-1]) + 1)

    return {
        "label": label,
        "best": min(dists),
        "mean": statistics.mean(dists),
        "std": statistics.pstdev(dists),
        "worst": max(dists),
        "time": statistics.mean(times),
        "conv": statistics.mean(convergence),
    }


def print_table(title, rows):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
    print(f"{'configuração':<24}{'melhor':>9}{'média':>9}{'desvio':>9}"
          f"{'pior':>9}{'tempo(s)':>10}{'conv.':>9}")
    print("-" * 78)
    for r in rows:
        print(f"{r['label']:<24}{r['best']:>9.2f}{r['mean']:>9.2f}{r['std']:>9.2f}"
              f"{r['worst']:>9.2f}{r['time']:>10.3f}{r['conv']:>9.0f}")


# ============================================================
# 1. AG - VARREDURA DE PARÂMETROS
# ============================================================

print(f"\nInstância: {NUM_CITIES} cidades | {REPS} execuções por configuração "
      f"| {ITERS} gerações/iterações")

ag_cx = [run_many(genetic_algorithm, f"crossover = {v}", crossover_rate=v,
                  mutation_rate=0.02, population_size=50) for v in (0.1, 0.5, 0.9)]
print_table("1a) AG - taxa de recombinação (mut=0.02, pop=50)", ag_cx)

ag_mut = [run_many(genetic_algorithm, f"mutação = {v}", mutation_rate=v,
                   crossover_rate=0.9, population_size=50) for v in (0.01, 0.1, 0.2)]
print_table("1b) AG - taxa de mutação (cx=0.9, pop=50)", ag_mut)

ag_pop = [run_many(genetic_algorithm, f"população = {v}", population_size=v,
                   crossover_rate=0.9, mutation_rate=0.02) for v in (10, 50, 100)]
print_table("1c) AG - tamanho da população (cx=0.9, mut=0.02)", ag_pop)


# ============================================================
# 2. PSO - VARREDURA DE PARÂMETROS
# ============================================================

pso_c2 = [run_many(pso, f"social c2 = {v}", c2=v, c1=1.0, w=0.8,
                   num_particles=50) for v in (0.1, 1.0, 2.0)]
print_table("2a) PSO - peso social c2 (c1=1.0, w=0.8, pop=50)", pso_c2)

pso_c1 = [run_many(pso, f"cognitivo c1 = {v}", c1=v, c2=1.0, w=0.8,
                   num_particles=50) for v in (0.1, 1.0, 2.0)]
print_table("2b) PSO - peso cognitivo c1 (c2=1.0, w=0.8, pop=50)", pso_c1)

pso_pop = [run_many(pso, f"população = {v}", num_particles=v, c1=1.0, c2=1.0,
                    w=0.8) for v in (10, 50, 100)]
print_table("2c) PSO - tamanho da população (c1=c2=1.0, w=0.8)", pso_pop)


# ============================================================
# 3. ANÁLISE COMPARATIVA (mesmo tamanho de população)
# ============================================================

for pop in (10, 50, 100):
    ag = run_many(genetic_algorithm, f"AG  (pop={pop})", population_size=pop,
                  crossover_rate=0.9, mutation_rate=0.02)
    ps = run_many(pso, f"PSO (pop={pop})", num_particles=pop,
                  c1=1.0, c2=1.0, w=0.8)
    print_table(f"3) Comparativo - população = {pop}", [ag, ps])
