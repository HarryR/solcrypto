import unittest

from pysolcrypto.curve import randsn
from pysolcrypto.uaosring import uaosring_randkeys, uaosring_check, uaosring_sign


class UaosringTests(unittest.TestCase):
    def test_uaos(self):
        msg = randsn()
        keys = uaosring_randkeys(4)
        self.assertTrue(uaosring_check(*uaosring_sign(*keys, message=msg), message=msg))


if __name__ == "__main__":
    unittest.main()
