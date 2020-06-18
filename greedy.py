import itertools

# wrapper for greedy_cit function.
# it enables using real value list
def greedy_cit_for_general(t, ps, k):
    range_list = []
    for val in k:
        range_list.append(len(val))
    return greedy_cit(t, ps, range_list)

# After get test suite composed of integer, 
# this function can make real value test suite
def get_real_test_suite(real_value, test_suite):
    for test in test_suite:
        for i, value in enumerate(test):
            test[i] = real_value[i][value]
    return test_suite

def greedy_cit(t, ps, k):
    ts = []
    assign = {}
    parameter_num = len(ps)
    ts = add_first_t_combination(ts, ps, k, t)
    for i in range(t + 1, parameter_num + 1):
        pi = t_way_comb(t, i, k)
        for test in ts[:]:
            print(i)
            test_added, pi = choose_value(i, test, pi, k[i-1])
            ts.append(test_added)
            ts.remove(test)
        for alpha in pi[:]:
            if exist_cover(alpha, ts):
                pi.remove(alpha)
            else:
                ts.append(fix_testcase(pi, alpha))
    return ts

def add_first_t_combination(ts, ps, k, t):
    parameter = ps[:t]
    val = []
    value_range = k[:t]
    comb = get_combination(parameter, k)
    return comb

def get_combination(parameter, k):
    if len(parameter) == 1:
        result = []
        for val in range(k[0]):
            result.append([val])
        return result
    else:
        prior_result = get_combination(parameter[1:], k[1:])
        result = []
        for val in range(k[0]):
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
        for val in range(k[0]):
            result.append([val])
        return result
    else:
        prior_result = get_combination_by_num(parameter_num - 1, k[1:])
        result = []
        for val in range(k[0]):
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
    for val in range(k[t]):
        l = [-1 for _ in range(i)]
        l[i - 1] = val
        index_list = [x for x in range(i - 1)]
        to_iter = get_comb_list(index_list, t - 1) # (1, 2) (2, 3) (1, 3)
        res = []
        for index_tuple in to_iter:
            value_range = get_value_range(k, index_tuple)
            comb_set = get_combination_by_num(t - 1, value_range)
            for comb in comb_set:
                l_copy = l[:]
                for index, l_index in enumerate(index_tuple):
                    l_copy[l_index] = comb[index]
                res.append(l_copy)
        pi = pi + res
    return pi   

def get_value_range(k, index_tuple):
    res = []
    for i in index_tuple:
        res.append(k[i])
    return res

def is_cover(param1, param2):
    is_covered = True

    for i, param in enumerate(param1):
        if param == -1:
            continue
        if param != param2[i]:
            is_covered = False
    return is_covered

def get_covered(pi, t):
    count = 0
    for one in pi:
        is_covered = True
        for i, param in enumerate(one):
            if param == -1:
                continue
            if param != t[i]:
                is_covered = False
        if is_covered:
            count += 1
    return count

def choose_value(i, test, pi, value):
    cover_num = [0 for x in range(value)] # cover_num의 index는 P-i의 값
    for x in range(value):
        t = test[:]
        t.append(x)
        cover_num[x] = get_covered(pi, t)
    add = cover_num.index(max(cover_num))
    test_add = test[:]
    test_add.append(add)
    new_pi = remove_value(test_add, pi)
    return test_add, new_pi

def remove_value(test, pi):
    new_pi = []
    for comb in pi:
        is_covered = True
        for i, param in enumerate(comb):
            if param == -1:
                continue
            if param != test[i]:
                is_covered = False
        if not is_covered:
            new_pi.append(comb)
    return new_pi

def exist_cover(alpha, ts):
    for test in ts:
        if is_cover(alpha, test):
            return True
    return False

def get_unassigned_index(alpha):
    unassigned = []
    for index, val in enumerate(alpha):
        if val == -1:
            unassigned.append(index)
    return unassigned

def check_zip(alpha1, alpha2):
    for i, j in zip(alpha1, alpha2):
        if i == j:
            continue
        if i == -1 or j == -1:
            continue
        if i != j:
            return False
    return True
        
def fix_testcase(pi, alpha):
    test = alpha
    for one in pi:
        if check_zip(test, one):
            for index, val in enumerate(test):
                if val == -1:
                    if one[index] != -1:
                        test[index] = one[index]
    unassigned = get_unassigned_index(test)
    for i in unassigned:
        test[i] = 0    
    return test
test_suite = greedy_cit_for_general(2, ["x", "y"], [["hi", "hello"], [".", ",", "?"]])
print(get_real_test_suite([["hi", "hello"], [".", ",", "?"]], test_suite))