import unittest
import random

from pysolcrypto.merkle import merkle_tree, merkle_path, merkle_proof


class MerkleTests(unittest.TestCase):
    def test_merkle(self):
        for i in range(1, 100):
            items = list(range(0, i))
            tree, root = merkle_tree(items)
            random.shuffle(items)
            for item in items:
                proof = merkle_path(item, tree)
                assert merkle_proof(item, proof, root) is True


if __name__ == "__main__":
    unittest.main()
