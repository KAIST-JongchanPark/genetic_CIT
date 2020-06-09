def greedy_cit(t, ps, k):
    ts = []
    assign = {}
    parameter_num = len(ps)
    add_first_t_combination(ts, ps, k + 1, t)
    for i in range(t + 1, parameter_num):
        p = t_way_comb(t, i)
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
    comb = func(parameter, k)

def func(parameter, k):
    if len(parameter) == 1:
        result = []
        for val in range(k):
            result.append([val])
        return result
    else:
        prior_result = func(parameter[1:], k)
        result = []
        for val in range(k):
            buf = []
            for one in prior_result:
                a = one[:]
                a.insert(0, val)
                buf.append(a)
            result = result + buf
        return result

print(add_first_t_combination(set(), ["x", "y", "z"], 3, 3))
