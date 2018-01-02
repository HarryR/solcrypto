# SolCrypto

This repository contains Solidity and Python implementations of several cryptographic primitives, they are designed to work together and make it easier to build novel cryptosystems using composable primitives. These implementations can be easily switched to either the secp256k1 or alt_bn128 curves.

## Algorithms

 * Schnorr proof of knowledge, [Schnorr.sol](contracts/Schnorr.sol), [schnorr.py](pysolcrypto/schnorr.py)
 * AOS ring signatures, [AOSRing.sol](contracts/AOSRing.sol), [ring.py](pysolcrypto/ring.py)

## TODO

 * Linkable AOS ring
 * Pedersen commitments
 * Security hardening
 * Documentation

## White Papers

 * [Borromean Ring Signatures: Gregory Maxwell, Andrew Poelstra](https://github.com/Blockstream/borromean_paper)
 * [One-Time, Zero-Sum Ring Signature: Conner Fromknech](https://scalingbitcoin.org/papers/one-time-zero-sum-ring-signature-conner-fromknecht-2015.pdf)
 * [1-out-of-n Signatures from a Variety of Keys: Masayuki Abe, Miyako Ohkubo and Koutarou Suzuki](https://www.iacr.org/cryptodb/archive/2002/ASIACRYPT/50/50.pdf)
 * [One-out-of-Many Proofs: Jens Groth and Markulf Kohlweiss](http://discovery.ucl.ac.uk/1502142/1/Groth_764.pdf)