import random
import math

def calculate_distance(coord1, coord2):
    # Tamamen saf Python float tipi ile Öklid mesafesi hesaplama
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def create_distance_matrix(locations):
    num_points = len(locations)
    matrix = [[0.0 for _ in range(num_points)] for _ in range(num_points)]
    for i in range(num_points):
        for j in range(num_points):
            matrix[i][j] = calculate_distance(locations[i], locations[j])
    return matrix

def solve_tsp_with_genetic(locations, population_size=40, generations=80):
    num_cities = len(locations)
    dist_matrix = create_distance_matrix(locations)
    
    def eval_tsp(individual):
        distance = 0.0
        for i in range(len(individual) - 1):
            distance += dist_matrix[individual[i]][individual[i+1]]
        distance += dist_matrix[individual[-1]][individual]
        return distance

    # 1. Başlangıç popülasyonunu oluşturma
    population = []
    for _ in range(population_size):
        ind = list(range(num_cities))
        random.shuffle(ind)
        population.append(ind)
        
    # Evrim Döngüsü
    for _ in range(generations):
        # Popülasyonu maliyete göre sıralama
        population = sorted(population, key=lambda x: eval_tsp(x))
        new_population = population[:2] # Elitizm: En iyi 2 rotayı koru
        
        while len(new_population) < population_size:
            # Turnuva Seçimi
            parent1 = min(random.sample(population, 3), key=lambda x: eval_tsp(x))
            parent2 = min(random.sample(population, 3), key=lambda x: eval_tsp(x))
            
            # Sıralı Çaprazlama (Ordered Crossover)
            size = len(parent1)
            start, end = sorted(random.sample(range(size), 2))
            child = [-1] * size
            child[start:end] = parent1[start:end]
            
            pointer = 0
            for item in parent2:
                if item not in child:
                    while child[pointer] != -1:
                        pointer += 1
                    child[pointer] = item
            
            # Mutasyon (%15 ihtimalle iki şehrin yerini değiştir)
            if random.random() < 0.15:
                idx1, idx2 = random.sample(range(num_cities), 2)
                child[idx1], child[idx2] = child[idx2], child[idx1]
                
            new_population.append(child)
        population = new_population

    best_route = min(population, key=lambda x: eval_tsp(x))
    best_fitness = float(eval_tsp(best_route))
    
    return [int(x) for x in best_route], best_fitness
