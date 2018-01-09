from __future__ import print_function

from .curve import *
from .schnorr import *
from .utils import *

"""
This implements a linkable variant of the AOS 1-out-of-n ring signature
which requires only `n+1` scalars to validate in addition to the `n` public keys.

For more information, see:

 - https://eprint.iacr.org/2004/027.pdf

"""


def uaosring_randkeys(n=4):
	skeys = [randsn() for _ in range(0, n)]
	pkeys = [sbmul(sk) for sk in skeys]
	i = randint(0, n-1)
	return pkeys, (pkeys[i], skeys[i])


def uaosring_sign(pkeys, mypair, tees=None, alpha=None, message=None):
	assert len(pkeys) > 0
	message = message or hashpn(*pkeys)
	mypk, mysk = mypair
	myidx = pkeys.index(mypk)

	tees = tees or [randsn() for _ in range(0, len(pkeys))]
	cees = [0 for _ in range(0, len(pkeys))]
	alpha = alpha or randsn()

	M = hashtopoint(message)
	T = multiply(M, mysk)
	h = hashp(M, T)

	for n, i in [(n, (myidx+n) % len(pkeys)) for n in range(0, len(pkeys))]:
		Y = pkeys[i]
		t = tees[i]
		c = alpha if n == 0 else cees[i-1]

		a = add(sbmul(t), multiply(Y, c))
		b = add(multiply(M, t), multiply(T, c))
		cees[i] = hashs(h, hashp(T, a, b))

	alpha_gap = submodn(alpha, cees[myidx-1])
	tees[myidx] = addmodn(tees[myidx], mulmodn(mysk, alpha_gap))

	return pkeys, T, tees, cees[-1]


def uaosring_check(pkeys, tag, tees, seed, message=None):
	"""
	\begin{align*}
	M &= Hash(m) \\
	h &= hash(M, T) \\
	\forall\ (Y, t, i) \in ring\ [ \\
	A &= G^{t_i} \oplus Y_i^{c_{i-1}} \\
	B &= M^{t_i} \oplus T^{c_{i-1}} \\
	c_i &= hash(h, m, T, A, B) \\
	] 
	\end{align*}
	"""
	assert len(pkeys) > 0
	assert len(tees) == len(pkeys)
	message = message or hashpn(*pkeys)
	M = hashtopoint(message)
	h = hashp(M, tag)
	c = seed
	for i, y in enumerate(pkeys):
		t = tees[i]
		a = add(sbmul(t), multiply(y, c))
		b = add(multiply(M, t), multiply(tag, c))
		c = hashs(h, hashp(tag, a, b))
	return c == seed


if __name__ == "__main__":
	msg = randsn()
	keys = uaosring_randkeys(4)

	print(uaosring_check(*uaosring_sign(*keys, message=msg), message=msg))

	proof = uaosring_sign(*keys, message=msg)

	tag = quotelist([proof[1][0].n, proof[1][1].n])
	print(quotelist([item.n for sublist in proof[0] for item in sublist]) + ',' + tag + ',' + quotelist(proof[2]) + ',' + quote(proof[3]) + ',' + quote(msg))
