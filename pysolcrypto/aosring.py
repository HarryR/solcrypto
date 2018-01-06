from __future__ import print_function

from .curve import *
from .schnorr import *
from .utils import *

"""
This implements AOS 1-out-of-n ring signature which require only `n+1`
scalars to validate in addition to the `n` public keys.

''Intuitively, this scheme is a ring of Schnorr signatures where each
challenge is taken from the previous step. Indeed, it is the Schnorr
signature scheme where n=1''

For more information, see:

 - https://www.iacr.org/cryptodb/archive/2002/ASIACRYPT/50/50.pdf

When verifying the ring only the initial seed value for `c` is provided
instead of supplying a value of `c` for each link in the ring. The hash
of the previous link is used as the next value of `c`.

The ring is successfully verified if the last value of `c` matches the
seed value.

For more information on turning this scheme into a linkable ring:

 - https://bitcointalk.org/index.php?topic=972541.msg10619684#msg10619684
 - https://eprint.iacr.org/2004/027.pdf
"""


def aosring_randkeys(n=4):
	skeys = [randsn() for _ in range(0, n)]
	pkeys = [sbmul(sk) for sk in skeys]
	i = randint(0, n-1)
	return pkeys, (pkeys[i], skeys[i])


def aosring_sign(pkeys, mypair, tees=None, alpha=None, message=None):
	assert len(pkeys) > 0
	message = message or hashpn(*pkeys)
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
		cees[idx] = schnorr_calc(pkeys[idx], tees[idx], c, message)
		n += 1
		i += 1

	# Then close the ring, which proves we know the secret for one ring item
	# TODO: split into schnorr_alter
	alpha_gap = submodn(alpha, cees[myidx-1])
	tees[myidx] = addmodn(tees[myidx], mulmodn(mysk, alpha_gap))

	return pkeys, tees, cees[-1]


def aosring_check(pkeys, tees, seed, message=None):
	assert len(pkeys) > 0
	assert len(tees) == len(pkeys)
	message = message or hashpn(*pkeys)
	c = seed
	for i, pkey in enumerate(pkeys):
		c = schnorr_calc(pkey, tees[i], c, message)
	return c == seed


if __name__ == "__main__":
	msg = randsn()
	keys = aosring_randkeys(4)

	print(aosring_check(*aosring_sign(*keys, message=msg), message=msg))

	proof = aosring_sign(*keys, message=msg)
	print(quotelist([item.n for sublist in proof[0] for item in sublist]) + ',' + quotelist(proof[1]) + ',' + quote(proof[2]) + ',' + quote(msg))
