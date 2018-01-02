from __future__ import print_function

from .secp256k1 import *


def schnorr_create(secret, message):
	xG = sbmul(secret)
	k = hashsn(message, secret)
	kG = sbmul(k)
	e = hashsn(hashpn(xG, kG), message)
	s = submodn(k, mulmodn(secret, e))
	return xG, s, e, message


def schnorr_calc(xG, s, e, message):
	kG = add(sbmul(s), multiply(xG, e))
	return hashsn(hashpn(xG, kG), message)


def schnorr_verify(xG, s, e, message):
	return e == schnorr_calc(xG, s, e, message)


if __name__ == "__main__":
	print(schnorr_verify(*schnorr_create(randsn(), randsn())))
