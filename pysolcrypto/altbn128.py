import sys
from random import randint
from hashlib import sha256
from py_ecc import bn128
from py_ecc.bn128 import add, multiply, curve_order, G1
from py_ecc.bn128.bn128_field_elements import inv

safe_ord = ord if sys.version_info.major == 2 else lambda x: x if isinstance(x, int) else ord(x)
bytes_to_int = lambda x: reduce(lambda o, b: (o << 8) + safe_ord(b), [0] + list(x))
randsn = lambda: randint(1, curve_order - 1)
sbmul = lambda s: multiply(G1, s)
hashsn = lambda *x: bytes_to_int(sha256('.'.join(['%X' for _ in range(0, len(x))]) % x).digest()) % curve_order
hashpn = lambda *x: hashsn(*[item.n for sublist in x for item in sublist])
addmodn = lambda x, y: (x + y) % curve_order
mulmodn = lambda x, y: (x * y) % curve_order
submodn = lambda x, y: (x - y) % curve_order
invmodn = lambda x: inv(x, curve_order)
negp = lambda x: (x[0], -x[1])
