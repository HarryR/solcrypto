import sys
from random import randint
from sha3 import keccak_256
from py_ecc import bn128
from py_ecc.bn128 import add, multiply, curve_order, G1
from py_ecc.bn128.bn128_field_elements import inv

from .utils import bytes_to_int, tobe256

randsn = lambda: randint(1, curve_order - 1)
sbmul = lambda s: multiply(G1, s)
hashs = lambda *x: bytes_to_int(keccak_256(''.join(map(tobe256, x))).digest())
hashsn = lambda *x: hashs(*x) % curve_order
hashpn = lambda *x: hashsn(*[item.n for sublist in x for item in sublist])
addmodn = lambda x, y: (x + y) % curve_order
mulmodn = lambda x, y: (x * y) % curve_order
submodn = lambda x, y: (x - y) % curve_order
invmodn = lambda x: inv(x, curve_order)
negp = lambda x: (x[0], -x[1])


if __name__ == "__main__":
	# Compatibility with: uint256(keccak256(uint256(1), uint256(2), uint256(3))) % Curve.N();
	assert hashsn(1, 2, 3) == 5999809398626971894156481321441750001229812699285374901473004231265197659290
