import unittest

from pysolcrypto.curve import randsn
from pysolcrypto.aosring import aosring_randkeys, aosring_check, aosring_sign


class AosringTests(unittest.TestCase):
    def test_aos(self):
        msg = randsn()
        keys = aosring_randkeys(4)
        self.assertTrue(aosring_check(*aosring_sign(*keys, message=msg), message=msg))


if __name__ == "__main__":
    unittest.main()
