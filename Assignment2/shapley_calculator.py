#!/usr/bin python

from __future__ import print_function
import numpy as np
import sys
from itertools import chain, combinations


# Pre-compute factorials upto a maximum number N in the game
def factorial(N):
    lookup_fact = np.zeros((N+1,)).astype(np.int32)
    lookup_fact[0] = 1
    for i in xrange(1, N+1):
        lookup_fact[i] = i * lookup_fact[i-1]
    return lookup_fact


# Generates all subsets
def gen_subsets(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# Calculate shapley value
def shapley_calculator(value_dict, N, facts):
    i = 1
    shapley_values = []
    ind = 0
    for i in xrange(1, N+1):
        y = 0
        for s, v in value_dict.items():
            if i in s:
                x = v
                x -= value_dict[tuple([a for a in s if a != i])]
                x *= facts[len(s) - 1]
                x *= facts[N - len(s)]
                x /= float(facts[N])
                y += x
        shapley_values.append(y)
        ind += 1
    return shapley_values


def main():
    inp_path = sys.argv[1]
    f = open(inp_path, 'r')
    N = 0
    inp = map(lambda x: x.rstrip(), f.readlines())
    N = int(inp[0])
    values = map(lambda x: int(x), inp[1].split(','))
    main_list = range(1, N+1)
    player_value = {}
    for i, item in enumerate(gen_subsets(main_list)):
        if len(item) >= 1:
            player_value[item] = values[i-1]
    player_value[()] = 0
    fact_table = factorial(N)
    sv = shapley_calculator(player_value, N, fact_table)
    print("The sharpley value vector is :\n")
    for i, x in enumerate(sv):
        print("For player %d, the allocation is %.2f" % (i, x))

if __name__ == "__main__":
    main()
