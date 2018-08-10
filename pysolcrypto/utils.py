import sys
import binascii
import math
from functools import reduce
from os import urandom
from sha3 import keccak_256

quote = lambda x: '"' + str(x) + '"'
quotemany = lambda *x: ','.join(map(quote, x))
quotelist = lambda x: '[' + quotemany(*x) + ']'

safe_ord = ord if sys.version_info.major == 2 else lambda x: x if isinstance(x, int) else ord(x)

bytes_to_int = lambda x: reduce(lambda o, b: (o << 8) + safe_ord(b), [0] + list(x))

def packl(lnum):
    if lnum == 0:
        return b'\0'
    s = hex(lnum)[2:].rstrip('L')
    if len(s) & 1:
        s = '0' + s
    return binascii.unhexlify(s)

int_to_big_endian = packl

zpad = lambda x, l: b'\x00' * max(0, l - len(x)) + x

tobe256 = lambda v: zpad(int_to_big_endian(v), 32)

def hashs(*x):
    data = b''.join(map(tobe256, x))
    return bytes_to_int(keccak_256(data).digest())

randb256 = lambda: urandom(32)


bit_clear = lambda n, b: n ^ (1<<(b-1)) if n & 1<<(b-1) else n

bit_set = lambda n, b: n | (1<<(b-1))

bit_test = lambda n, b: 0 != (n & (1<<(b-1)))


def powmod(a,b,n):
    c = 0
    f = 1
    k = int(math.log(b, 2))
    while k >= 0:
        c *= 2
        f = (f*f)%n
        if b & (1 << k):
            c += 1
            f = (f*a) % n
        k -= 1
    return f


if __name__ == "__main__":
    assert bin(bit_clear(3, 1)) == '0b10'
    assert bin(bit_clear(3, 2)) == '0b1'
    assert bin(bit_set(0, 1)) == '0b1'
