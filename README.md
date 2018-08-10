# SolCrypto

[![Build Status](https://travis-ci.org/HarryR/solcrypto.svg?branch=master)](https://travis-ci.org/HarryR/solcrypto)

This repository contains Solidity and Python implementations of several cryptographic primitives, they are designed to work together and make it easier to build novel cryptosystems using composable primitives. These implementations can be easily switched to either the secp256k1 or alt_bn128 curves.

## Algorithms

 * Schnorr proof of knowledge: [Schnorr.sol](contracts/Schnorr.sol), [schnorr.py](pysolcrypto/schnorr.py)
 * AOS ring signatures: [AOSRing.sol](contracts/AOSRing.sol), [aosring.py](pysolcrypto/aosring.py)
 * Linkable AOS ring signatures: [UAOSRing.sol](contracts/UAOSRing.sol), [uaosring.py](pysolcrypto/uaosring.py)
 * Packed ECDSA signatures (2x 256bit words, no `v`): [ECDSA.sol](contracts/ECDSA.sol), [ecdsa.py](pysolcrypto/ecdsa.py)
 * Merkle tree: [MerkleProof.sol](contracts/MerkleProof.sol), [merkle.py](pysolcrypto/merkle.py)
 * Fast AOS ring signatures, using `ecrecover`: [HackyAOSRing.sol](contracts/HackyAOSRing.sol), [hackyaosring.py](pysolcrypto/hackyaosring.py), see [this post on ethresear.ch](https://ethresear.ch/t/you-can-kinda-abuse-ecrecover-to-do-ecmul-in-secp256k1-today/2384)

## TODO

 * Pedersen commitments
 * Security hardening
 * Documentation

## White Papers

 * [How to Leak a Secret](https://people.csail.mit.edu/rivest/pubs/RST01.pdf)
 * [Linkable Spontaneous Anonymous Group Signature for Ad Hoc Groups](https://eprint.iacr.org/2004/027.pdf)
 * [Borromean Ring Signatures: Gregory Maxwell, Andrew Poelstra](https://github.com/Blockstream/borromean_paper)
 * [One-Time, Zero-Sum Ring Signature: Conner Fromknech](https://scalingbitcoin.org/papers/one-time-zero-sum-ring-signature-conner-fromknecht-2015.pdf)
 * [1-out-of-n Signatures from a Variety of Keys: Masayuki Abe, Miyako Ohkubo and Koutarou Suzuki](https://www.iacr.org/cryptodb/archive/2002/ASIACRYPT/50/50.pdf)
 * [One-out-of-Many Proofs: Jens Groth and Markulf Kohlweiss](http://discovery.ucl.ac.uk/1502142/1/Groth_764.pdf)
 * [Non-interactive and Information-Theoretic Secure Verifiable Secret Sharing](https://www.cs.cornell.edu/courses/cs754/2001fa/129.PDF)