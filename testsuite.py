import random


class TestSuite():
    def __init__(self, base, additional):
        self.base = base
        self.additional = additional
        self.fitness_value = None

    def assign_fitness_value(self, fitness_value):
        self.fitness_value = fitnes_value

    def make_test_suite(self):
        self.test_suite = self.base + self.additional

    def eval_variety(self, parameter_num, parameter_range):
        appear_time = []

        for ith_param in range(parameter_num):
            value_list = [1 for _ in range(parameter_range+1)]
            appear_time.append(value_list)

        for testcase in self.additional:
            for ind in range(len(testcase)):
                appear_time[ind][testcase[ind]] += 1

        score = 1
        for ith_param in appear_time:
            for ind in range(len(ith_param)):
                # if ith_param[ind] != 1:
                score = score * \
                    ((ith_param[ind]*parameter_num)/len(self.additional))
                # prevent the fitness value become too big or too small for temprorary
                # if there are better standard, need to modify

        self.fitness_value = score

    # assume soft_list format [constraint1 = [[parameter index,lower range, upper range], [], ...], constraint2 = []...]
    # if test case satisfy constraint condition, multiply fitness value 1.3
    def eval_soft_constraint(self, soft_list):
        for constraint in soft_list:
            for testcase in self.additional:
                for (ind, condition) in enumerate(constraint):
                    if testcase[condition[0]] < condition[1] or condition[2] < testcase[condition[0]]:
                        break
                    if ind == (len(constraint)-1):
                        self.fitness_value = self.fitness_value * 1.3

    # hard_list format is same as soft_list
    # if test case satisfy hard constraint condition, set fitness value to 0 and return

    def eval_hard_constraint(self, hard_list):
        for constraint in hard_list:
            for testcase in self.additional:
                for (ind, condition) in enumerate(constraint):
                    if testcase[condition[0]] < condition[1] or condition[2] < testcase[condition[0]]:
                        break
                    if ind == (len(constraint)-1):
                        self.fitness_value = 0
                        return

    def print_fit_val(self):
        print(self.fitness_value)
