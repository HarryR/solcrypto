import unittest
import bls


class BlsTests(unittest.TestCase):
	def test_prove_key(self):
		sk, pk = bls.bls_keygen()
		sig = bls.bls_prove_key(sk)
		self.assertTrue(bls.bls_verify_key(pk, sig))

	def test_aggregate(self):
		"Aggregate signature where the two participants sign the same message"
		sk1, pk1 = bls.bls_keygen()
		sk2, pk2 = bls.bls_keygen()
		msg = bls.randn()
		sig1 = bls.bls_sign(sk1, msg)
		sig2 = bls.bls_sign(sk2, msg)
		self.assertTrue(bls.bls_agg_verify([pk1, pk2], msg, [sig1, sig2]))

	def test_aggregate_bad(self):
		"Bad aggregate signature, where the two participants sign different messages"
		sk1, pk1 = bls.bls_keygen()
		sk2, pk2 = bls.bls_keygen()
		msg1 = bls.randn()
		msg2 = bls.randn()
		sig1 = bls.bls_sign(sk1, msg1)
		sig2 = bls.bls_sign(sk2, msg2)
		self.assertFalse(bls.bls_agg_verify([pk1, pk2], msg1, [sig1, sig2]))


if __name__ == "__main__":
    unittest.main()
