import random
import numpy as np
import itertools
from lib.Population import Population

class Result:
    def __init__(self, crossover, mutation, parent_selection, survival_selection, population_size, fitness, a, b, c, d, e):
        self.crossover = crossover
        self.mutation = mutation
        self.parent_selection = parent_selection
        self.survival_selection = survival_selection
        self.population_size = population_size
        self.fitness = fitness

        self.cnt_converged = a 
        self.iter_converged = b 
        self.individuals_converged = c 
        self.mean_fitness = d
        self.all_converged = e

    def print_result(self):
        print('----------------')
        print('Representation:')
        print('Crossover:', self.crossover)
        print('Mutation:', self.mutation)
        print('Parent Selection:', self.parent_selection)
        print('Survival Selection:', self.survival_selection)
        print('Population Size:', self.population_size)
        print('Fitness:', self.fitness)
        print('')
        print('Resultados:')
        print('Em quantas execuções o algoritmo convergiu (nº/30 execuções)')
        print(self.cnt_converged)
        print('Em que iteração o algoritmo convergiu (média e desvio padrão)')
        print(self.iter_converged)
        print('Número de indivíduos que convergiram por execução')
        print(self.individuals_converged)
        print('Fitness médio alcançado nas 30 execuções (média e desvio padrão)')
        print(self.mean_fitness)
        print('Média do número de iterações para todos os individuos convergirem')
        print(self.all_converged)

def sort_cnt_converged(a):
    return a.cnt_converged

def sort_iter_converged(a):
    return a.iter_converged[0]

def sort_individuals_converged(a):
    return a.individuals_converged

def sort_mean_fitness(a):
    return a.mean_fitness[0]

def sort_all_converged(a):
    return a.all_converged

def print_best_results(results):
    print('Primeira Implementação')
    results[0].print_result()

    print('\n\nCombinação que mais convergiu nas execuções')
    x = sorted(results, key=sort_cnt_converged, reverse=True)
    x[0].print_result()

    print('\n\nCombinação que convergiu mais rapidamente em média')
    x = sorted(results, key=sort_iter_converged)
    x[0].print_result()

    print('\n\nCombinação que mais individuos convergiram na ultima iteração em média')
    x = sorted(results, key=sort_individuals_converged, reverse=True)
    x[0].print_result()

    print('\n\nCombinação com o maior fitness médio nas execuções')
    x = sorted(results, key=sort_mean_fitness, reverse=True)
    x[0].print_result()

    print('\n\nCombinação com o menor número de iterações para todos convergirem em média')
    x = sorted(results, key=sort_all_converged)
    x[0].print_result()

def main():
    crossover_params = ['Cut and Crossfill']
    mutation_params = ['swap', 'shuffle']
    parent_selection_params = ['Tournament Selection']
    survival_selection_params = ['worst replacement']
    population_size = [100]
    fitness_params = ['cnt_clash']

    results = []
    number_executions = 2

    for x in itertools.product(crossover_params, mutation_params, parent_selection_params, survival_selection_params, population_size, fitness_params):
        params = {'crossover': x[0], 'mutation': x[1], 'parent_selection': x[2], 'survival_selection': x[3], 'population_size': x[4], 'fitness': x[5]}
        
        cnt_converged = 0
        iter_converged, number_converged, fitness_mean, all_converged = [], [], [], []
        for i in range(number_executions):
            population = Population(params)
            ans = population.evolve(verbose = False)

            cnt_converged += int(ans['converged'])
            iter_converged.append(ans['iter_converged'])
            number_converged.append(ans['number_converged'])
            fitness_mean.append(ans['mean'])
            all_converged.append(ans['all_converged'])
            
            print(i, ans['all_converged'])

        a = cnt_converged / number_executions
        b = (np.mean(iter_converged), np.std(iter_converged))
        c = np.mean(number_converged)
        d = (np.mean(fitness_mean[:][-1]), np.std(fitness_mean[:][-1]))
        e = np.mean(all_converged)

        results.append(Result(params['crossover'], params['mutation'], params['parent_selection'], 
                              params['survival_selection'], params['population_size'], params['fitness'], a, b, c, d, e))


    print_best_results(results)

if __name__ == "__main__":
    main()