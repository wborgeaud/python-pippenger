from modp import ModP
from group import MultIntModP, EC
from pippenger import Pippenger
from random import randint
from ecdsa import SECP256k1, NIST192p, NIST224p, NIST256p, NIST256p, NIST384p, NIST521p 
from sympy import isprime
import pandas as pd
import time

def naive_multi_exp_ec(gs, es):
    tmp = es[0] * gs[0]
    for i in range(1, len(gs)):
        tmp += es[i] * gs[i]
    return tmp

def benchmark_ec(N, curve):
    G = EC(curve)
    order_cyclic_subgroup = curve.order

    g = curve.generator

    gs = [g*randint(1, order_cyclic_subgroup) for _ in range(N)]
    es = [randint(1,order_cyclic_subgroup) for _ in range(N)]

    start = time.time()
    Pip = Pippenger(G)
    res_pip = Pip.multiexp(gs, es)
    time_pip = time.time()-start

    start = time.time()
    res_naive = naive_multi_exp_ec(gs, es)
    time_naive = time.time()-start

    assert res_pip == res_naive

    return time_pip, time_naive

results = []
for curve in [SECP256k1, NIST192p, NIST256p, NIST384p, NIST521p]:
    print(curve.name, len(bin(curve.order)))
    for N in range(2, len(bin(curve.order))-2, 1+len(bin(curve.order))//50):
        print(N)
        time_pip, time_naive = benchmark_ec(N, curve)
        results.append({
            'curve': curve.name,
            'order': len(bin(curve.order))-2,
            'N': N,
            'PipTime': time_pip,
            'NaiveTime': time_naive,
        })

results = pd.DataFrame(results)
results.to_csv('results_ec.csv')
