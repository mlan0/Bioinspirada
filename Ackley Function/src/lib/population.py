
import random
import numpy as np
from .individual import Individual
from .helper import plot_result

#pop 500 mi = 30 lamb 50
#pop 1000 mi 30 lamb 100
class Population:
    def __init__(self, params):
        self.params = params
        self.population_size = params['population_size']
        self.population = [Individual(mutation=params['mutation']) for i in range(params['population_size'])]
        self.mi = 30
        self.lamb = 50

    def print_population(self):
        for individual in self.population:
            print(individual.x)

    def parent_selection(self):
        return list(random.sample(self.population, self.mi))

    def crossover_parent(self, p1, p2):
        n = len(p1.x)
        x_child = []
        if self.params['crossover'] == 'mid_fixed_parents':
            for i in range(n):
                x_child.append((p1.x[i] + p2.x[i]) / 2.0)
        return Individual(x = x_child, mutation = self.params['mutation'])

    def crossover(self, parents):
        children = []
        while len(children) != self.lamb:
            p1, p2 = random.sample(parents, 2)
            children.append(self.crossover_parent(p1, p2))
        return children

    def survival_selection(self, parents, offspring):
        aux = []
        if self.params['survival_selection'] == 'mi+lambda':
            aux = parents.copy()
            aux.extend(offspring)
        if self.params['survival_selection'] == 'mi,lambda':
            aux = offspring
        aux.sort()
        return aux[:len(parents)]

    def metrics(self):
        vals = [x.fitness() for x in self.population]
        return {"best" : np.min(vals), "mean" : np.mean(vals), "std" : np.std(vals)}

    def evolve(self, verbose = False):
        
        params = self.params
        curr_iter = 0
        next_swap = 1000
        stats = self.metrics()
        
        all_bests, all_means, all_stds = [], [], []
        
        all_bests.append(stats['best'])
        all_means.append(stats['mean'])
        all_stds.append(stats['std'])

        while stats['best'] != 0 and curr_iter < 10000:
            curr_iter += 1

            # select mi parents
            parents = self.parent_selection()

            # generate lambda children
            offspring_crossover = self.crossover(parents)
            
            # possibly mutate children
            offspring_mutation = [(x.mutate(params['mutation']) if np.random.uniform(0, 1) < self.params['mutation_prob'] else x) for x in offspring_crossover]

            new_pop = []
            for ind in self.population:
                if ind not in parents:
                    new_pop.append(ind)

            new_pop.extend(self.survival_selection(parents, offspring_mutation))
            
            self.population = new_pop

            stats = self.metrics()
            
            all_bests.append(stats['best'])
            all_means.append(stats['mean'])
            all_stds.append(stats['std'])
            
            if curr_iter % 20 == 0:
                print(curr_iter, self.mi, len(self.population), stats['best'])
            
            if curr_iter == next_swap:
                if self.params['survival_selection'] == 'mi,lambda':
                    self.params['survival_selection'] = 'mi+lambda'
                    self.mi = 30
                    self.lamb = 50
                    next_swap = curr_iter + 400
                    #for ind in self.population:
                        #ind.sigma = self.sigma = random.uniform(0.1, 0.25)
                    if self.params['mutation'] == 'individual_std':
                        self.population = [x.update_sigma(2.0 / 3) for x in self.population]
                elif self.params['survival_selection'] == 'mi+lambda':
                    self.params['survival_selection'] = 'mi,lambda'
                    self.mi = 15
                    self.lamb = 80
                    next_swap = curr_iter + 600
                    #for ind in self.population:
                        #ind.sigma = self.sigma = random.uniform(0.1, 0.25)
                    if self.params['mutation'] == 'individual_std':
                        self.population = [x.update_sigma(1.5) for x in self.population]
        
        print('CHEGOUUUU ', self.metrics()['best'])
        plot_result(all_bests, all_means, all_stds, 'ackley result')
        
            
        return self
