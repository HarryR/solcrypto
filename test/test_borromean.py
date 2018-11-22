import unittest

from pysolcrypto.altbn128 import randsn, addmodp, asint
from pysolcrypto.borromean import *


class BorromeanRingTest(unittest.TestCase):

  def test_borromean(self):
    msg = randsn()
    rings, pairs = borromean_ring_gen(n=4, m=4)
    e, s_mat = borromean_ring_sign(rings, pairs, msg=msg)
    self.assertTrue(borromean_ring_verify(rings, e, s_mat, msg=msg))

  def test_borromean_with_bad_message(self):
    msg = randsn()
    rings, pairs = borromean_ring_gen(n=4, m=4)
    e, s_mat = borromean_ring_sign(rings, pairs, msg=msg)
    bad_msg = addmodp(msg,1)
    self.assertFalse(borromean_ring_verify(rings, e, s_mat, msg=bad_msg))

class RangeProofTest(unittest.TestCase):

  def test_range_proof(self):
    final, commitments, e, s_mat = self.range_proof_create(3, N=8)
    ret = self.range_proof_verify(final, commitments, e, s_mat)
    self.assertTrue(ret)

  def range_proof_create(self, value, blindings=None, N=16):
    base = 2
    bits = self.convert_base(value, base, N)
    rings = [[[0,0] for _ in range(base)] for _ in range(N)]
    pairs = []
    commitments = [[0,0] for _ in range(N)]
    final_commitment = None
    for i in range(N):
      subv = bits[i] * 2**i
      commitments[i], r = self.pedersen_c(subv, blindings[i] if blindings != None else None)
      C_1 = add(commitments[i], negp(multiply(self.H(), 2**i)))
      rings[i] = [commitments[i], C_1]
      pairs.append((rings[i][0 if subv == 0 else 1], r))
      final_commitment = add(final_commitment, commitments[i])
    e, s_mat = borromean_ring_sign(rings, pairs, msg=None)
    return final_commitment, commitments, e, s_mat

  def range_proof_verify(self, final, commitments, e, s_mat):
    base = 2
    N = len(commitments)
    rings = [[[0,0] for _ in range(base)] for _ in range(N)]
    expected_final = None
    for i in range(N):
      rings[i][0] = commitments[i]
      rings[i][1] = add(commitments[i], negp(multiply(self.H(), 2**i)))
      expected_final = add(expected_final, commitments[i])
    ret = borromean_ring_verify(rings, e, s_mat, msg=None)
    return ret and expected_final == final

  def H(self):
    from pysolcrypto.utils import hashs
    from pysolcrypto.altbn128 import hashtopoint, G1
    h = hashpn(G1)
    return hashtopoint(h)

  def pedersen_c(self, v, r=None):
    from pysolcrypto.altbn128 import add, multiply, G1, randsn
    if r is None:
      r = randsn()
    return add(multiply(G1,r), multiply(self.H(), v)), r

  def convert_base(self, value, base, n):
    digits = []
    i = 0
    while i < n:
      i += 1
      if value == 0:
        digits.append(0)
        continue
      digits.append(value % base)
      value = value // base
    return digits


# class SolidityTest(unittest.TestCase):
  
#   def test_solidity(self):
#     from web3 import Web3, HTTPProvider
#     pasint = lambda p: (asint(p[0]), asint(p[1].n))
#     mpasint = lambda *mp: [list(pasint(p)) for p in mp]
#     serring = lambda *x: [mpasint(*sublist) for sublist in x]
#     w3 = Web3(HTTPProvider(''))
#     abi = '[{"constant":true,"inputs":[{"name":"rings","type":"uint256[2][][]"},{"name":"tees","type":"uint256[][]"},{"name":"e0","type":"uint256"},{"name":"message","type":"uint256"}],"name":"VerifyProof","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'
#     adr = Web3.toChecksumAddress('')
#     c = w.eth.contract(abi=abi,address=adr)
#     msg = randsn()
#     rings, pairs = borromean_ring_gen(n=4, m=2)
#     e, s_mat = borromean_ring_sign(rings, pairs, msg=msg)
#     self.assertTrue(c.functions.VerifyProof(serring(*rings), s_mat, e, 0).call())


if __name__ == "__main__":
  unittest.main()