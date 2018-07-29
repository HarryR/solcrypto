from py_ecc.bn128 import pairing, G2, G1

from .altbn128 import randsn, addmodn, hashsn, mulmodp, invmodn, multiply

"""
Bare-essentials implementation taken from the following papers:

- http://legacydirs.umiacs.umd.edu/~zhangyp/papers/accum.pdf
- https://pdfs.semanticscholar.org/3ffc/1bcb01802f85d764f1da2986389b2c4c818b.pdf
- https://eprint.iacr.org/2005/123.pdf
- https://eprint.iacr.org/2018/046.pdf
- https://eprint.iacr.org/2008/538.pdf

XXX: this doesn't fully and faithfully implement the papers
     there are a number of parameters missing which are crucial
     for security.
"""


def accumulate(items_list, secret):
    """
    Given a set of items, create an aggregate point on G1 which
    contains the hashes of all items.

    @param items_list: List of items

    @returns g^(x0)(x1)..(xn)
    """
    x0_mul_to_xn = 1
    for item in items_list:
        xi = addmodn(hashsn(item), secret)
        x0_mul_to_xn = mulmodp(x0_mul_to_xn, xi)

    AkX = multiply(G1, x0_mul_to_xn)
    return AkX


def witness(AkX, my_item, secret):
    """
    Create a witness as:

        W_x = (AkX / x)

    @param AkX: G1 point accumulator
    @param my_item: Your item
    """
    x = addmodn(hashsn(my_item), secret)
    return multiply(AkX, invmodn(x))


def ismember(AkX, my_item, W_x, secret):
    """
    Verify membership by pairing equality

        e(G2, AkX) = e(G2^x, W_x)

    @param AkX: G1 point accumulator
    @param my_item: Your item
    @param W_x: G1 point witness
    """
    x = addmodn(hashsn(my_item), secret)
    e1 = pairing(G2, AkX)
    e2 = pairing(multiply(G2, x), W_x)
    return e1 == e2


if __name__ == "__main__":
    secret = randsn()
    items = list(range(1, 10))
    my_item = items[3]
    AkX = accumulate(items, secret)
    W_x = witness(AkX, my_item, secret)
    assert True == ismember(AkX, my_item, W_x, secret)
