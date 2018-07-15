#!/usr/bin/env python
"""
This merkle tree implementation uses a balanced binary tree, for example a 
tree containing 5 leafs has 3 nodes and 1 root.

        r
       / \ 
      n3  L5
      /\
     /  \
    /    \
   n1     n2
  / \    / \
 L1  L2 L3 L4

When hashing the leafs and nodes the highest bit is reserved for the proof
to store the left or right attribute. Example proof of L1:

  H(H(H(L1, L2), n2), L5) = r

The proof supplied for L1 is:

   L2, n2, L5

To prove L2 instead of L1 the proof supplied is:

   L1, n2, L5

The highest bit of each item in the proof determines if it's the 
left or right argument to the hash function.

Whereas to prove L5 the proof would be:

    n3

To verify the proof:

    r = H(n3, L5)

As you can see the `n3` entry takes the lhs param in order to preserve
the ordering property of the hash function by sacrificing a bit.

The 'balanced' terminology here may be different from the common understanding
of balanced, here it means that every node always has 2 children. 
"""
from __future__ import print_function
import random
from past.builtins import long

from sha3 import keccak_256

from .utils import zpad, int_to_big_endian, bit_clear, bit_test, bit_set, bytes_to_int

def serialize(v):
    if isinstance(v, str):
        return v
    if isinstance(v, (int, long)):
        return zpad(int_to_big_endian(v), 32)
    raise NotImplementedError(v)


hashs = lambda *x: bytes_to_int(keccak_256(b''.join(map(serialize, x))).digest())

merkle_hash = lambda *x: bit_clear(hashs(*x), 255)


def merkle_tree(items):
    tree = [[merkle_hash(_) for _ in items]]
    extra = merkle_hash(0)
    while True:
        level = tree[-1]
        if len(level) % 2 != 0:
            extra = merkle_hash(extra)
            level.append( extra )
        it = iter(level)
        level = [merkle_hash(item, next(it)) for item in it]
        tree.append(level)
        if len(level) == 1:
            break
    return tree, tree[-1][0]


def merkle_path(item, tree):
    """
    Create a merkle path for the item within the tree
    max length = (height*2) - 1
    min length = 1
    """
    item = merkle_hash(item)
    idx = tree[0].index(item)

    path = []
    for level in tree:
        if len(level) == 1:
            break
        even = (idx % 2) == 0
        if even:
            path.append(bit_set(level[idx+1], 255))
        else:
            path.append(level[idx-1])
        idx = idx // 2
    return path


def merkle_proof(leaf, path, root):
    """
    Verify merkle path for an item matches the root
    """
    node = merkle_hash(leaf)
    for item in path:
        if bit_test(item, 255):
            node = merkle_hash(node, bit_clear(item, 255))
        else:
            node = merkle_hash(item, node)
    return node == root


def main():
    for i in range(1, 100):
        items = range(0, i)
        tree, root = merkle_tree(items)
        random.shuffle(items)
        for item in items:
            proof = merkle_path(item, tree)
            assert merkle_proof(item, proof, root) is True


if __name__ == "__main__":
    main()
