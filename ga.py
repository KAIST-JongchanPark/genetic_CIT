from testsuite import TestSuite
import random


class GA():
    # Range for budget
    # len(base) < budget == len(base) + len(additional) < len(greedy_suite)
    def __init__(self, greedy_suite, base, parameter_num, parameter_range, budget, population_num, mutation_rate):
        self.greedy_suite = greedy_suite
        self.base = base
        self.parameter_num = parameter_num
        # maximum value of the parameter
        self.parameter_range = parameter_range
        self.budget = budget
        self.mutation_rate = mutation_rate
        self.population_num = population_num
        self.fitness_result = []
        self.population = []

    # must do this

    def delete_base_from_greedy(self):
        for i in range(len(self.base)):
            target = self.base[i]
            if(target in self.greedy_suite):
                self.greedy_suite.remove(target)
    # 수정 필요

    def initial_population(self):
        # Using Approach 1: randomly choosing from the greedy - test suite
        initial_population = []
        for i in range(self.population_num):
            gene = random.choices(
                self.greedy_suite, k=self.budget - len(self.base))
            new_suite = TestSuite(self.base, gene)
            initial_population.append(new_suite)
        self.population = initial_population

    def fitness_calculate(self, soft_list, hard_list):

        #print("fitness calculating this population")
        # for i in range(len(self.population)):
        #    print(self.population[i].additional)
        self.fitness_result = []
        for i in range(self.population_num):
            self.population[i].eval_variety(
                self.parameter_num, self.parameter_range)
            self.population[i].eval_soft_constraint(soft_list)
            self.population[i].eval_hard_constraint(hard_list)
            self.fitness_result.append(self.population[i].fitness_value)

    def select_parent(self):
        result = random.choices(
            self.population, weights=self.fitness_result, k=2)

        return result

    def make_children(self, parent1, parent2):
        # Sort the list lexicographically
        # For now, just take half / half
        sorted_parent1 = sorted(parent1.additional, key=lambda elem: elem)
        sorted_parent2 = sorted(parent2.additional, key=lambda elem: elem)

        child1 = []
        child2 = []

        assert(self.budget - len(self.base) == len(parent1.additional))
        assert(self.budget - len(self.base) == len(parent2.additional))
        additional_length = self.budget - len(self.base)
        for i in range(additional_length):
            if(i < int(additional_length / 2)):
                child1.append(sorted_parent1[i])
                child2.append(sorted_parent2[i])
            else:
                child1.append(sorted_parent2[i])
                child2.append(sorted_parent1[i])

        return child1

    def mutate_test_suite(self, test_suite):
        # iterate for each parameter
        mutant = []
        for i in range(len(test_suite[0])):
            new_dict = {}
            for j in range(len(test_suite)):
                if(test_suite[j][i] not in new_dict.keys()):
                    new_dict[test_suite[j][i]] = 0
                else:
                    new_dict[test_suite[j][i]] = new_dict[test_suite[j][i]] + 1
            minimum_cnt = -1
            minimum_var = None
            for j in range(len(new_dict.keys())):
                temp = list(new_dict.keys())[j]
                temp_cnt = new_dict[temp]
                if(minimum_cnt < 0 or temp_cnt < minimum_cnt):
                    minimum_cnt = temp_cnt
                    minimum_var = temp

            mutant.append(minimum_var)
        del test_suite[0]
        test_suite.append(mutant)
        return test_suite

    def mutate_population(self, new_population):
        mutated_population = []
        for i in range(len(new_population)):
            target_test_suite = new_population[i].additional
            if(random.random() < self.mutation_rate):
                new_test_suite = self.mutate_test_suite(target_test_suite)
                mutated_population.append(TestSuite(self.base, new_test_suite))
            else:
                mutated_population.append(
                    TestSuite(self.base, target_test_suite))

        return mutated_population

    def next_generation(self):

        elite_num = int(self.population_num * 4 / 10)

        children_num = int(self.population_num * 4 / 10)

        random_children_num = self.population_num - elite_num - children_num

        sorted_population = sorted(
            self.population, key=lambda test_suite: test_suite.fitness_value)
        elite_children = sorted_population[self.population_num - elite_num:]
        print(sorted_population[-1].fitness_value)
       # for i in range(len(sorted_population)):
        #    print(sorted_population[i].fitness_value)

        children = []
        for i in range(children_num):
            [parent1, parent2] = self.select_parent()
            child = self.make_children(parent1, parent2)
            children.append(TestSuite(self.base, child))

        random_children = []
        for i in range(random_children_num):
            random_child = random.choice(self.population)
            random_children.append(random_child)

        new_population = elite_children + children + random_children

        mutated_population = self.mutate_population(new_population)

    #    print("previous generation")
    #    for i in range(len(self.population)):
    #        print(self.population[i].additional)
    #    print("next_generation")
    #    for i in range(len(self.population)):
    #        print(new_population[i].additional)

        self.population = mutated_population

    def adjust(self):

        for i in range(len(self.population)):
            target_test_suite = self.population[i].additional
            target_set = set(tuple(element) for element in target_test_suite)
            target_lst = [list(t) for t in set(tuple(element)
                                               for element in target_set)]
            need_cnt = len(target_test_suite) - len(target_lst)
            for j in range(need_cnt):
                new_case = random.choice(self.greedy_suite)
                while(new_case in target_lst):
                    new_case = random.choice(self.greedy_suite)
                target_lst.append(new_case)

            self.population[i].additional = target_lst
