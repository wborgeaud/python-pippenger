from modp import ModP
from group import MultIntModP, EC
from pippenger import Pippenger
from random import randint
from ecdsa import SECP256k1
import time

def naive_multi_exp(gs, es):
    tmp = ModP(1, p)
    for i in range(len(gs)):
        tmp *= gs[i]**es[i]
    return tmp

def naive_multi_exp_ec(gs, es):
    tmp = es[0] * gs[0]
    for i in range(1, len(gs)):
        tmp += es[i] * gs[i]
    return tmp


p = 212202256221099231839682404630396606792594247691648787647152808879411708125779

order_cyclic_subgroup = 106101128110549615919841202315198303396297123845824393823576404439705854062889

G = MultIntModP(p, order_cyclic_subgroup)

g = ModP(3, p)

gs = [g**randint(1, order_cyclic_subgroup) for _ in range(250)]
es = [randint(1,order_cyclic_subgroup) for _ in range(250)]

ModP.reset()
start = time.time()
Pip = Pippenger(G)
print(Pip.multiexp(gs, es))
print(time.time()-start)
print(ModP.num_of_mult)

ModP.reset()
start = time.time()
print(naive_multi_exp(gs, es))
print(time.time()-start)
print(ModP.num_of_mult)


G = EC(SECP256k1)
order_cyclic_subgroup = SECP256k1.order

g = SECP256k1.generator

gs = [g*randint(1, order_cyclic_subgroup) for _ in range(250)]
es = [randint(1,order_cyclic_subgroup) for _ in range(250)]

start = time.time()
Pip = Pippenger(G)
print(Pip.multiexp(gs, es))
print(time.time()-start)

start = time.time()
print(naive_multi_exp_ec(gs, es))
print(time.time()-start)