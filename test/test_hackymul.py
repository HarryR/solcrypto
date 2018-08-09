import unittest

from pysolcrypto.secp256k1 import sbmul, G, hackymul_raw, hackymul, add, multiply, randsn, mulmodn, N
from pysolcrypto.ecdsa import pubkey_to_ethaddr
"""
def ecdsa_raw_recover(msghash, vrs):
    v, r, s = vrs
    y = # (get y coordinate for EC point with x=r, with same parity as v)
    Gz = jacobian_multiply((Gx, Gy, 1), (N - hash_to_int(msghash)) % N)
    XY = jacobian_multiply((r, y, 1), s)
    Qr = jacobian_add(Gz, XY)
    Q = jacobian_multiply(Qr, inv(r, N))
    return from_jacobian(Q)
Suppose that we feed in msghash=0, and s=r*k for some k. Then, we get:

Gz = 0
XY = (r,y) * r * k
Qr = (r,y) * r * k
Q = (r, y) * r * k * inv(r) = (r, y) * k


------------------

	Gz = sbmul(msghash)
	kG = add(Gz, multiply([r,y], s))


ECDSA(m,v,r,s) := (([Gx,Gy]*(-m)) + ([r,y]*s)) * -r

"""

class HackymulTests(unittest.TestCase):
	def test_hackymul(self):
		test1 = sbmul(1000)
		test2 = hackymul_raw(G[0], G[1], 1000)
		test3 = pubkey_to_ethaddr(test1)
		test4 = pubkey_to_ethaddr(test2)
		test5 = hackymul(G[0], G[1], 1000)
		self.assertEqual(test1, test2)
		self.assertEqual(test3, test4)
		self.assertEqual(test5, test4)

	def test_hacky_addmulmul(self):
		t = randsn()
		T = sbmul(t)
		c = randsn()
		y = randsn()
		Y = sbmul(y)

		m = (((N - t) % N) * Y[0]) % N
		X = hackymul_raw(Y[0], Y[1], c, m=m)
		self.assertEqual(X, add(T, multiply(Y, c)))



if __name__ == "__main__":
    unittest.main()
