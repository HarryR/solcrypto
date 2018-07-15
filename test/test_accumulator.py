import unittest

from pysolcrypto.accumulator import accumulate, witness, ismember


class AccumulatorTests(unittest.TestCase):
    def test_witness(self):
        items = list(range(1, 10))
        my_item = items[3]
        AkX = accumulate(items)
        W_x = witness(AkX, my_item)
        self.assertTrue(ismember(AkX, my_item, W_x))


if __name__ == "__main__":
    unittest.main()
