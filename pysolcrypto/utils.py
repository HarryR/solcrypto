import sys
import binascii

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
