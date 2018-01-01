from __future__ import print_function

from .secp256k1 import *


"""
This implements a Borromean style ring signature which requires 
only `n+1` scalars to validate in addition to the `n` public keys.

When verifying the ring only the initial seed value for `c` is provided
instead of supplying a value of `c` for each link in the ring. The hash
of the previous link is used as the next value of `c`.

The ring is successfully verified if the last value of `c` matches the
seed value.
"""


def ring_randkeys(n=4):
	skeys = [randsn() for _ in range(0, n)]
	pkeys = [sbmul(sk) for sk in skeys]
	i = randint(0, n-1)
	return pkeys, (pkeys[i], skeys[i])


def ring_sign(pkeys, mypair, tees=None, alpha=None):
	mypk, mysk = mypair
	myidx = pkeys.index(mypk)

	tees = tees or [randsn() for _ in range(0, len(pkeys))]
	cees = [0 for _ in range(0, len(pkeys))]
	alpha = alpha or randsn()

	i = myidx
	n = 0
	while n < len(pkeys):
		idx = i % len(pkeys)
		c = alpha if n == 0 else cees[idx-1]	
		cees[idx] = hashpn(add(sbmul(tees[idx]), multiply(pkeys[idx], c)))
		n += 1
		i += 1

	# Then close the ring, which proves we know the secret for one ring item
	alpha_gap = submodn(alpha, cees[myidx-1])
	tees[myidx] = addmodn(tees[myidx], mulmodn(mysk, alpha_gap))

	return pkeys, tees, cees[-1]


def ring_check(pkeys, tees, seed):
	c = seed
	for i, pkey in enumerate(pkeys):
		c = hashpn(add(sbmul(tees[i]), multiply(pkey, c or seed)))
	return c == seed


if __name__ == "__main__":
	print(ring_check(*ring_sign(*ring_randkeys(4))))
