from __future__ import print_function
import math
import os
from collections import defaultdict
from base64 import b64decode
from binascii import unhexlify, hexlify
from ethereum import utils
import bitcoin as b

from .utils import *


def pack_signature(v, r, s):
	v = (v - 27) << 255
	return tobe256(r), tobe256(s | v)


def unpack_signature(r, sv):
	r = bytes_to_int(r)
	sv = bytes_to_int(sv)
	v = (sv & (1 << 255))
	if v:
		v = 28
		sv = sv ^ (1 << 255)
	else:
		v = 27
	print("v", v)
	print("r", r)
	print("s", sv)
	return v, r, sv


def pubkey_to_ethaddr(pubkey):
	if isinstance(pubkey, tuple):
		assert len(pubkey) == 2
		pubkey = b.encode_pubkey(pubkey, 'bin')
	return utils.sha3(pubkey[1:])[12:].encode('hex')


def sign(messageHash, key):
	return pack_signature(*b.ecdsa_raw_sign(messageHash, seckey))


def recover(messageHash, r, sv):
	 return pubkey_to_ethaddr(b.ecdsa_raw_recover(messageHash, unpack_signature(r, sv)))


if __name__ == "__main__":
	messageHash = randb256()
	seckey = randb256()
	pubkey = pubkey_to_ethaddr(b.privtopub(seckey))

	sig_t = b.ecdsa_raw_sign(messageHash, seckey)
	sig = sign(messageHash, seckey)
	assert unpack_signature(*sig) == sig_t

	pubkey_v = recover(messageHash, *sig)
	assert pubkey == pubkey_v
	print("Pubkey:", pubkey_v)
	print("Message:", messageHash.encode('hex'))
	print("Sig:", sig[0].encode('hex'), sig[1].encode('hex'))
