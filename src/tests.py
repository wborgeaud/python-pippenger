from modp import ModP
from group import MultIntModP, EC
from pippenger import Pippenger
from random import randint
from ecdsa import SECP256k1, NIST192p, NIST224p, NIST256p, NIST384p, NIST521p
from ecdsa.ellipticcurve import Point
from sympy import isprime
import time
import unittest
from math import log2, floor

def naive_multi_exp(gs, es, p):
    tmp = ModP(1, p)
    for i in range(len(gs)):
        tmp *= gs[i]**es[i]
    return tmp

def naive_multi_exp_ec(gs, es):
    tmp = Point(None, None, None)
    for i in range(len(gs)):
        tmp += es[i] * gs[i]
    return tmp

def get_good_primes(start):
    p = start
    while True:
        if isprime(p) and isprime(2*p+1):
            gen = 2
            while True:
                if pow(gen, p, 2*p+1) == 1:
                    return p, 2*p+1, gen
                gen += 1
        p += 1

class TestsIntModP(unittest.TestCase):
    def test_all_values_of_N(self):
        order_cyclic_subgroup, p, gen = get_good_primes(2**32)
        G = MultIntModP(p, order_cyclic_subgroup)
        Pip = Pippenger(G)
        g = ModP(gen, p)
        for N in range(floor(log2(order_cyclic_subgroup))):
            gs = [g**randint(1, order_cyclic_subgroup) for _ in range(N)]
            es = [randint(1,order_cyclic_subgroup) for _ in range(N)]
            with self.subTest(N=N):
                self.assertEqual(Pip.multiexp(gs, es), naive_multi_exp(gs, es, p))
    
    def test_all_values_of_p(self):
        start = 5
        for _ in range(50):
            order_cyclic_subgroup, p, gen = get_good_primes(start)
            G = MultIntModP(p, order_cyclic_subgroup)
            Pip = Pippenger(G)
            g = ModP(gen, p)
            for N in range(floor(log2(order_cyclic_subgroup))):
                gs = [g**randint(1, order_cyclic_subgroup) for _ in range(N)]
                es = [randint(1,order_cyclic_subgroup) for _ in range(N)]
                with self.subTest(N=N, order=order_cyclic_subgroup):
                    self.assertEqual(Pip.multiexp(gs, es), naive_multi_exp(gs, es,p))
            start = order_cyclic_subgroup + 1
            
class TestsEC(unittest.TestCase):
    def test_all_values_of_N(self):
        CURVE = NIST192p
        G = EC(CURVE)
        order_cyclic_subgroup = CURVE.order
        g = CURVE.generator
        Pip = Pippenger(G)
        for N in range(0, floor(log2(order_cyclic_subgroup)), 20):
            gs = [g*randint(1, order_cyclic_subgroup) for _ in range(N)]
            es = [randint(1,order_cyclic_subgroup) for _ in range(N)]
            with self.subTest(N=N):
                self.assertEqual(Pip.multiexp(gs, es), naive_multi_exp_ec(gs, es))
    
    def test_all_curves(self):
        curves = [SECP256k1, NIST192p, NIST224p, NIST256p, NIST384p, NIST521p]
        for curve in curves:
            G = EC(curve)
            order_cyclic_subgroup = curve.order
            g = curve.generator
            Pip = Pippenger(G)
            for _ in range(10):
                N = randint(0, floor(log2(order_cyclic_subgroup)))
                gs = [g*randint(1, order_cyclic_subgroup) for _ in range(N)]
                es = [randint(1,order_cyclic_subgroup) for _ in range(N)]
                with self.subTest(N=N):
                    self.assertEqual(Pip.multiexp(gs, es), naive_multi_exp_ec(gs, es))
            order_cyclic_subgroup, p, gen = get_good_primes(start)
            G = MultIntModP(p, order_cyclic_subgroup)
            Pip = Pippenger(G)
            g = ModP(gen, p)
            for N in range(floor(log2(order_cyclic_subgroup))):
                gs = [g**randint(1, order_cyclic_subgroup) for _ in range(N)]
                es = [randint(1,order_cyclic_subgroup) for _ in range(N)]
                self.assertEqual(Pip.multiexp(gs, es), naive_multi_exp(gs, es, p))
            start = order_cyclic_subgroup + 1
        

if __name__ == '__main__':
    unittest.main()