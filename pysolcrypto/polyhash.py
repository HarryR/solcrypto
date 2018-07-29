from py_ecc.bn128 import *
from random import randint


def polyhash(k, x):
    r"""
        {f_k}(x) = \sum_{i=0}^{t} x_i \cdot k^i

    If implemented on Ethereum, uses only `addmod` and `mulmod` opcodes
    """
    assert k > 0 and k < field_modulus
    x = [FQ(ord(_)) for _ in x]
    k = FQ(k)
    f = FQ(0)
    for (i, x_i) in enumerate(x):
        f += x_i * k
        k *= k
    return f


if __name__ == "__main__":
    k = randint(1, field_modulus - 1)
    print(polyhash(k, 'hello world'))
