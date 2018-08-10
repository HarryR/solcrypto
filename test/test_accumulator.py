import unittest

from pysolcrypto.accumulator import accumulate, witness, ismember
from pysolcrypto.altbn128 import randsn


class AccumulatorTests(unittest.TestCase):
    def test_witness(self):
        secret = randsn()
        items = list(range(1, 10))
        my_item = items[3]
        AkX = accumulate(items, secret)
        W_x = witness(AkX, my_item, secret)
        self.assertTrue(ismember(AkX, my_item, W_x, secret))


if __name__ == "__main__":
    unittest.main()
