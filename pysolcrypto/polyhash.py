from random import randint
from py_ecc.bn128 import FQ, field_modulus

from .utils import bytes_to_field_elements


def polyhash(key, nonce, message, round_consts=None):
    r"""
    This construction uses two `n`-bit keys, `k` and `k'`
    it operates on message of bitlength `L = t * n`.
    It starts by splitting the input message `x` into `t` blocks
    of bitlength `n` denoted `x_i`.
    The `x_i`, `k` and `k'` are represented as elements of `GF(p)`
    The authentication function `g_{k,k'}(x)` is then defined as:

        g_{k,k'}(x) = k' + \sum_{i=0}^t (x_i+c_i) * k^i

    Where:

     * `x` is the message
     * `x_i` is a segment of the message
     * `c_i` is an optional round constant
     * `k'` is the nonce
     * `k` is the key

    """
    if isinstance(message, (str, bytes)):
        if isinstance(message, str):
            message = message.encode('utf-8')
        message = bytes_to_field_elements(message)

    if round_consts and len(message) != round_consts:
        raise RuntimeError("Round consts must be the same length as message")

    k = None
    res = FQ(nonce)

    for i, x_i in enumerate(message):
        rhs = FQ(x_i)

        if round_consts:
            rhs += round_consts[i]

        if k is not None:
            rhs *= k
            k *= k
        else:
            k = FQ(key)

        res += rhs

    return res


if __name__ == "__main__":
    key = randint(2, field_modulus - 2)
    nonce = randint(2, field_modulus - 2)
    message = 'derp derp derp'
    print(polyhash(key, nonce, message))
