import sys
from random import randint
from py_ecc.secp256k1.secp256k1 import add, multiply, inv, N, P, G, ecdsa_raw_recover
from .utils import hashs, tobe256
from .ecdsa import pubkey_to_ethaddr

#assert False == "Do not use, use altbn128"

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


def hackymul_raw(x, y, scalar, m=0):
	"""
	Implements the 'hacky multiply' from:
	https://ethresear.ch/t/you-can-kinda-abuse-ecrecover-to-do-ecmul-in-secp256k1-today/2384
	"""
	#m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
	v = 28 if y % 2 != 0 else 27
	s = mulmodn(scalar, x)
	return ecdsa_raw_recover(tobe256(m), (v, x, s))


def hackymul(x, y, scalar, m=0):
	return pubkey_to_ethaddr(hackymul_raw(x, y, scalar, m))
