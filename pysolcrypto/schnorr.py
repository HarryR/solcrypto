from __future__ import print_function

from .secp256k1 import *


def schnorr_create(secret, message):
	xG = sbmul(secret)
	k = hashsn(message, secret)
	kG = sbmul(k)
	e = hashsn(hashpn(xG, kG), message)
	s = submodn(k, mulmodn(secret, e))
	return xG, s, e, message


def schnorr_verify(xG, s, e, message):
	sG = sbmul(s)
	kG = add(sG, multiply(xG, e))
	check_e = hashsn(hashpn(xG, kG), message)
	return e == check_e


if __name__ == "__main__":
	print(schnorr_verify(*schnorr_create(randsn(), randsn())))
