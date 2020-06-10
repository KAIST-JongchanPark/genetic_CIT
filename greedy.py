import itertools

def greedy_cit(t, ps, k):
    value_range = k + 1
    ts = []
    assign = {}
    parameter_num = len(ps)
    add_first_t_combination(ts, ps, value_range, t)
    for i in range(t + 1, parameter_num + 1):
        pi = t_way_comb(t, i, value_range)
        for test in ts:
            test_added = choose_value(i, test, p)
            remove_value(test_added, p)
        for alpha in p:
            if exist_cover(alpha, ts):
                remove_test_set_from_phi(p, alpha)
            else:
                fix_testcase(p, alpha, ts)
    return ts

def add_first_t_combination(ts, ps, k, t):
    parameter = ps[:t]
    val = []
    comb = get_combination(parameter, k)

def get_combination(parameter, k):
    if len(parameter) == 1:
        result = []
        for val in range(k):
            result.append([val])
        return result
    else:
        prior_result = get_combination(parameter[1:], k)
        result = []
        for val in range(k):
            buf = []
            for one in prior_result:
                a = one[:]
                a.insert(0, val)
                buf.append(a)
            result = result + buf
        return result

def get_combination_by_num(parameter_num, k):
    if parameter_num == 1:
        result = []
        for val in range(k):
            result.append([val])
        return result
    else:
        prior_result = get_combination_by_num(parameter_num - 1, k)
        result = []
        for val in range(k):
            buf = []
            for one in prior_result:
                a = one[:]
                a.insert(0, val)
                buf.append(a)
            result = result + buf
        return result

def get_comb_list(l, r):
    return list(itertools.combinations(l, r))

def t_way_comb(t, i, k):
    pi = []
    comb_set = get_combination_by_num(t - 1, k)
    for val in range(k):
        l = [-1 for _ in range(i)]
        l[i - 1] = val
        index_list = [x for x in range(i - 1)]
        to_iter = get_comb_list(index_list, t - 1) # (1, 2) (2, 3) (1, 3)
        res = []
        for index_tuple in to_iter:
            for comb in comb_set:
                l_copy = l[:]
                for index, l_index in enumerate(index_tuple):
                    l_copy[l_index] = comb[index]
                res.append(l_copy)
        pi = pi + res
    return pi   
