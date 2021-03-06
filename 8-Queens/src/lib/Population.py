import random
import numpy as np
from lib.Individual import Individual
from lib.helper import translate_to_perm

class Population:
    def __init__(self, params):
        self.params = params
        self.population = list(Individual(fitness_method = params['fitness']) for i in range(params['population_size']))

    def print_population(self):
        print('Population:')
        for person in self.population:
            print(person.x, translate_to_perm(person.x), person.fitness())

    # TODO: Melhor de 2 de 5 escolhidos aleatoriamente
    def parent_selection(self):
        if self.params['parent_selection'] == 'Tournament Selection':
            parents = random.sample(self.population, 5)
            parents.sort(reverse=True)
            return [parents[0], parents[1]]

    # TODO: Recombinação: “cut-and-crossfill” crossover
    #implement cut and crossfill with p1 and p2
    def crossover(self, p1, p2):
        if self.params['crossover'] == 'Cut and Crossfill':
            perm1 = translate_to_perm(p1.x)
            perm2 = translate_to_perm(p2.x)
            
            crossfill_pt = random.randint(0, 7)
            
            son1, son2 = perm1[:crossfill_pt], perm2[:crossfill_pt]
            
            pos = crossfill_pt
            while len(son1) != len(perm1):
                if perm2[pos] not in son1:
                    son1.append(perm2[pos])
                pos = (pos + 1) % len(perm2)

            pos = crossfill_pt
            while len(son2) != len(perm2):
                if perm1[pos] not in son2:
                    son2.append(perm1[pos])
                pos = (pos + 1) % len(perm1)

            r = random.uniform(0, 1)
            if r <= 0.9:
                return [Individual(self.params['fitness'], son1), Individual(self.params['fitness'], x = son2)]
            else:
                return [p1, p2]

    # select the fittest individuals
    def survival_selection(self):
        if self.params['survival_selection'] == 'worst replacement':
            self.population.sort(reverse=True)
            self.population = self.population[:self.params['population_size']]

    def population_fitness_analysis(self):
        fitness = [x.fitness() for x in self.population]
        return (np.mean(fitness), np.std(fitness), np.min(fitness), np.max(fitness))

    def get_fittest_individual(self):
        self.population.sort(reverse=True)
        return self.population[0]

    def get_worst_individual(self):
        self.population.sort()
        return self.population[0]

    def evolve(self, verbose = False):
        params = self.params
        curr_iter = 0
        n_iter = 10000
        iter_converged = -1

        ans_mean, ans_std, ans_min, ans_max = [], [], [], []
        number_converged = []
        mean, std, min_val, max_val = self.population_fitness_analysis()
        ans_mean.append(mean)
        ans_std.append(std)
        ans_min.append(min_val)
        ans_max.append(max_val)
        while self.get_worst_individual().fitness() != 0:
            if self.get_fittest_individual().fitness() == 0 and iter_converged == -1:
                iter_converged = curr_iter
                number_converged = len([x for x in self.population if x.fitness() == 65])
            #self.print_population()

            curr_iter += 1

            # select the 2 fittest individuals 
            parents = self.parent_selection()

            #create children
            offspring_crossover = self.crossover(parents[0], parents[1])

            #possibly mutate children
            offspring_mutation = [x.mutation(params['mutation']) for x in offspring_crossover]
            
            #add children to the population
            self.population.extend(offspring_mutation)
            
            #self.print_population()

            #select new generation
            self.survival_selection()

            mean, std, min_val, max_val = self.population_fitness_analysis()
            ans_mean.append(mean)
            ans_std.append(std)
            ans_min.append(min_val)
            ans_max.append(max_val)

        if verbose:
            #print('----------------')
            print('Converged iteration {}:\nBest individual has fitness {}.\nWorst individual has fitness {}.\nMean fitness is {}.\nStd is {}.'.format(iter_converged, max_val, min_val, mean, std))
            #print('----------------')

        
        converged = self.get_fittest_individual().fitness() == 0
        return {"iter_converged" : iter_converged, "mean" : ans_mean, "std" : ans_std, "min" : ans_min, "max" : ans_max, 
                "converged" : converged, "number_converged": number_converged, "all_converged": curr_iter}