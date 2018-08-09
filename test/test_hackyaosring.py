import unittest

from pysolcrypto.secp256k1 import randsn
from pysolcrypto.hackyaosring import haosring_randkeys, haosring_check, haosring_sign


class HaosringTests(unittest.TestCase):
    def test_aos(self):
        msg = randsn()
        keys = haosring_randkeys(4)
        self.assertTrue(haosring_check(*haosring_sign(*keys, message=msg), message=msg))


if __name__ == "__main__":
    unittest.main()
