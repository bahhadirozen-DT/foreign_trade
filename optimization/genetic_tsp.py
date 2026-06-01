import random
import numpy as np
try:
    from deap import base, creator, tools, algorithms
except ImportError:
    pass

def calculate_distance(coord1, coord2):
    return float(np.linalg.norm(np.array(coord1) - np.array(coord2)))

def create_distance_matrix(locations):
    num_points = len(locations)
    matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            matrix[i][j] = calculate_distance(locations[i], locations[j])
    return matrix

def solve_tsp_with_genetic(locations, population_size=40, generations=80):
    num_cities = len(locations)
    dist_matrix = create_distance_matrix(locations)
    
    # DEAP çakışmalarını engellemek için try-except bloğu kullanıyoruz
    try:
        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMin)
    except Exception:
        # Eğer nesneler zaten varsa hata vermesini önleyip geçiyoruz
        pass

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(num_cities), num_cities)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalTSP(individual):
        distance = 0.0
        for i in range(len(individual) - 1):
            distance += float(dist_matrix[individual[i]][individual[i+1]])
        distance += float(dist_matrix[individual[-1]][individual[0]])
        return (distance,)

    toolbox.register("evaluate", evalTSP)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=population_size)
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=generations, verbose=False)
    
    best_ind = tools.selBest(pop, 1)[0]
    
    # Çıktıları ilkel Python tiplerine (list ve float) zorlayarak main.py'yi rahatlatıyoruz
    route_out = [int(x) for x in best_ind]
    fitness_out = float(best_ind.fitness.values[0])
    
    return route_out, fitness_out

