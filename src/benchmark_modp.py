from modp import ModP
from group import MultIntModP, EC
from pippenger import Pippenger
from random import randint
from ecdsa import SECP256k1, NIST192p, NIST224p, NIST256p, NIST256p, NIST384p, NIST521p 
from sympy import isprime
import pandas as pd
import time

def naive_multi_exp(gs, es):
    tmp = gs[0]**es[0]
    for i in range(1,len(gs)):
        tmp *= gs[i]**es[i]
    return tmp

def get_good_primes(bits):
    p = 2**bits + randint(0,2**(bits//2))
    while True:
        if isprime(p) and isprime(2*p+1):
            gen = 2
            while True:
                if pow(gen, p, 2*p+1) == 1:
                    return p, 2*p+1, gen
                gen += 1
        p += 1

def benchmark_int_mod_p(N, order_cyclic_subgroup, p, gen):
    G = MultIntModP(p, order_cyclic_subgroup)

    g = ModP(gen, p)

    gs = [g**randint(1, order_cyclic_subgroup) for _ in range(N)]
    es = [randint(1,order_cyclic_subgroup) for _ in range(N)]

    ModP.reset()
    start = time.time()
    Pip = Pippenger(G)
    res_pip = Pip.multiexp(gs, es)
    time_pip = time.time()-start
    mults_pip = ModP.num_of_mult

    ModP.reset()
    start = time.time()
    res_naive = naive_multi_exp(gs, es)
    time_naive = time.time()-start
    mults_naive = ModP.num_of_mult

    assert res_pip == res_naive

    return time_pip, mults_pip, time_naive, mults_naive

results = []
for bits in [2**i for i in range(4,10)]:
    print(bits)
    order_cyclic_subgroup, p, gen = get_good_primes(bits)
    for N in range(1, bits, 1 + bits//50):
        print(N)
        time_pip, mults_pip, time_naive, mults_naive = benchmark_int_mod_p(N, order_cyclic_subgroup, p, gen)
        results.append({
            'bits': bits,
            'N': N,
            'PipTime': time_pip,
            'PipMults': mults_pip,
            'NaiveTime': time_naive,
            'NaiveMults': mults_naive,
        })

results = pd.DataFrame(results)
results.to_csv('results_intmodp.csv')