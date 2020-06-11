import itertools

def greedy_cit(t, ps, k):
    value_range = k + 1
    ts = []
    assign = {}
    parameter_num = len(ps)
    ts = add_first_t_combination(ts, ps, value_range, t)
    for i in range(t + 1, parameter_num + 1):
        pi = t_way_comb(t, i, value_range)
        for test in ts[:]:
            test_added, pi = choose_value(i, test, pi, k)
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
    comb = get_combination(parameter, k)
    return comb

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

def choose_value(i, test, pi, k):
    cover_num = [0 for x in range(k)] # cover_num의 index는 P-i의 값
    for x in range(k):
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

print(greedy_cit(2, ["x", "y", "z"], 1))