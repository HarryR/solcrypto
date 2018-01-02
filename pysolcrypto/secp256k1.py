import sys
from random import randint
from py_ecc.secp256k1.secp256k1 import add, multiply, inv, N, P, G
from .utils import hashs

assert False == "Do not use, use altbn128"

safe_ord = ord if sys.version_info.major == 2 else lambda x: x if isinstance(x, int) else ord(x)
bytes_to_int = lambda x: reduce(lambda o, b: (o << 8) + safe_ord(b), [0] + list(x))
hashsn = lambda *x: hashs(*x) % N
hashpn = lambda *x: hashsn(*[item for sublist in x for item in sublist])
randsn = lambda: randint(1, N - 1)
sbmul = lambda s: multiply(G, s)
invmulp = lambda x, y: (x * pow(y, P-2, P))
invmodn = lambda x: inv(x, N)
addmodn = lambda x, y: (x + y) % N
mulmodn = lambda x, y: (x * y) % N
submodn = lambda x, y: (x - y) % N
negp = lambda x: (x[0], -x[1])
