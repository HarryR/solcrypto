from functools import reduce
import binascii
from os import urandom
from py_ecc.bn128 import *
from sha3 import keccak_256

"""
Implements BLS signatture aggregation as described at:

	https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html

---------

Roughly based on the following code:

	>>> from py_ecc.bn128 import *
	>>> from random import randint                            

	>>> sk1, sk2 = randint(1,curve_order-1), randint(1, curve_
	... order-1)                                              

	>>> pk1, pk2 = multiply(G2, sk1), multiply(G2, sk2)       

	>>> H = multiply(G1, randint(1, curve_order-1))           

	>>> sig1, sig2 = multiply(H, sk1), multiply(H, sk2)       

	>>> aggpk = add(pk1, pk2)                                 

	>>> aggsig = add(sig1, sig2)                              

	>>> pairing(aggpk, H) == pairing(G2, aggsig)              
	True


"""

addmodp = lambda x, y: (x + y) % field_modulus

mulmodp = lambda x, y: (x * y) % field_modulus

safe_ord = lambda x: x if isinstance(x, int) else ord(x)

bytes_to_int = lambda x: reduce(lambda o, b: (o << 8) + safe_ord(b), [0] + list(x))

def int_to_big_endian(lnum):
    if lnum == 0:
        return b'\0'
    s = hex(lnum)[2:].rstrip('L')
    if len(s) & 1:
        s = '0' + s
    return binascii.unhexlify(s)

zpad = lambda x, l: b'\x00' * max(0, l - len(x)) + x

tobe256 = lambda v: zpad(int_to_big_endian(v), 32)

def g2_to_list(point):
    return [_.n for _ in point[0].coeffs + point[1].coeffs]

def g1_to_list(point):
	return [_.n for _ in point]

fmt_list = lambda point: '[' + ', '.join([('"' + hex(_) + '"') for _ in point]) + ']'

def randn():
	return int.from_bytes(urandom(64), 'big') % curve_order

def hashs(*x):
    data = b''.join(map(tobe256, x))
    return bytes_to_int(keccak_256(data).digest())

def evalcurve_g1(x):	
	beta = addmodp(mulmodp(mulmodp(x, x), x), 3)
	assert field_modulus % 4 == 3
	a = (field_modulus+1)//4 # fast square root, using exponentation, assuming (p%4 == 3)
	y = pow(beta, a, field_modulus)
	return (beta, y)

def isoncurve_g1(x, y):
	return mulmodp(y, y) == addmodp(mulmodp(mulmodp(x, x), x), 3)

def hash_to_g1(x):
	# XXX: todo, re-hash on every round
	assert isinstance(x, int)
	x = x % field_modulus
	while True:
		beta, y = evalcurve_g1(x)
		if beta == mulmodp(y, y):
			assert isoncurve_g1(x, y)
			return FQ(x), FQ(y)
		x = addmodp(x, 1)

def hash_g2(x):
	xy_ints = [_.n for _ in (x[0].coeffs + x[1].coeffs)]
	return hashs(*xy_ints)

def bls_keygen():
	sk = randn()
	pk = multiply(G2, sk)
	return sk, pk

def bls_prove_key(sk):
	pk = multiply(G2, sk)
	msg = hash_g2(pk)
	return bls_sign(sk, msg)

def bls_verify_key(pk, sig):
	msg = hash_g2(pk)
	return bls_verify(pk, msg, sig)

def bls_sign(sk, msg):
	H_m = hash_to_g1(msg)
	sig = multiply(H_m, sk)
	return sig

def bls_verify(pk, msg, sig) -> bool:
	H_m = hash_to_g1(msg)
	return pairing(pk, H_m) * pairing(neg(G2), sig) == FQ12.one()

def bls_agg_verify(pks, msg, sigs) -> bool:
	H_m = hash_to_g1(msg)
	agg_pk = reduce(add, pks)
	agg_sig = reduce(add, sigs)
	return pairing(agg_pk, H_m) * pairing(neg(G2), agg_sig) == FQ12.one()
