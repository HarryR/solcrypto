import unittest

import bitcoin as b

from pysolcrypto.utils import randb256
from pysolcrypto.ecdsa import pubkey_to_ethaddr, unpack_signature, sign, recover


class EcdsaTests(unittest.TestCase):
    def test_ecdsa(self):
        # Verifies that a random sample of freshly generated keys don't
        # end up setting the 'flag' bit which replaces 'v'
        # If this test ever fails, the entire premise of this thing is fucked!
        for _ in range(0, 100):
            messageHash = randb256()
            seckey = randb256()
            pubkey = pubkey_to_ethaddr(b.privtopub(seckey))

            sig_t = b.ecdsa_raw_sign(messageHash, seckey)
            sig = sign(messageHash, seckey)
            assert unpack_signature(*sig) == sig_t

            pubkey_v = recover(messageHash, *sig)
            assert pubkey == pubkey_v


if __name__ == "__main__":
    unittest.main()
