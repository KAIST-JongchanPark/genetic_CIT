def greedy_cit(t, ps, k):
    ts = set()
    assign = {}
    parameter_num = len(ps)
    add_first_t_combination(ts, ps)
    for i in range(t + 1, n):
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