def greedy_cit(t, ps):
    ts = set()
    assign = {}
    ordered_ps = list(ps)
    parameter_num = len(ordered_ps)
    add_first_t_combination(ts, ordered_ps)
    for i in range(t + 1, n):
        