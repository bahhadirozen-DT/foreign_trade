import random
import numpy as np
from deap import base, creator, tools, algorithms

def calculate_distance(coord1, coord2):
    # İki koordinat arasındaki kuş uçuşu mesafeyi hesaplar (Öklid Mesafesi)
    return np.linalg.norm(np.array(coord1) - np.array(coord2))

def create_distance_matrix(locations):
    # Lokasyonlar arası mesafe matrisi oluşturur
    num_points = len(locations)
    matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            matrix[i][j] = calculate_distance(locations[i], locations[j])
    return matrix

def solve_tsp_with_genetic(locations, population_size=50, generations=100):
    num_cities = len(locations)
    dist_matrix = create_distance_matrix(locations)
    
    # DEAP Genetik Algoritma Kurulumu
    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) # Mesafeyi minimize et
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(num_cities), num_cities)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalTSP(individual):
        # Rotanın toplam mesafesini hesaplayan fonksiyon (Fitness)
        distance = 0
        for i in range(len(individual) - 1):
            distance += dist_matrix[individual[i]][individual[i+1]]
        distance += dist_matrix[individual[-1]][individual] # Başlangıç noktasına dönüş
        return (distance,)

    toolbox.register("evaluate", evalTSP)
    toolbox.register("mate", tools.cxOrdered) # Sıralı çaprazlama
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05) # Mutasyon
    toolbox.register("select", tools.selTournament, tournsize=3) # Turnuva seçimi

    pop = toolbox.population(n=population_size)
    
    # Algoritmayı çalıştırma (Elistizm içeren basit genetik algoritma)
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=generations, verbose=False)
    
    best_ind = tools.selBest(pop, 1)
    # Geri dönüş değerini tekil bir liste ve float değer olarak zorluyoruz
    actual_route = list(best_ind[0]) if isinstance(best_ind[0], (list, tuple)) else list(best_ind)
    actual_fitness = float(best_ind[0].fitness.values[0]) if hasattr(best_ind[0], 'fitness') else float(best_ind.fitness.values[0])
    
    return actual_route, actual_fitness
