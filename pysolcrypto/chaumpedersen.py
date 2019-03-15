from __future__ import print_function

from .curve import *


# We want to prove that (G,H,A,B) is a DDH-tuple, i.e. A=xG AND B=xH without revealing secret x
# Reference: https://www.cs.jhu.edu/~susan/600.641/scribes/lecture10.pdf


_hash_points_and_message = lambda a, b, m: hashsn(hashpn(a, b), m)


def chaumpedersen_create(G,H,secret, message):
    assert isinstance(secret, long)
    assert isinstance(message, long)
    xG = multiply(G, secret)
    xH = multiply(H, secret)
    k = hashsn(message, secret)
    kG = multiply(G, k)
    kH = multiply(H, k)
    e = hashs(xG[0].n, xG[1].n, xH[0].n, xH[1].n, kG[0].n, kG[1].n, kH[0].n, kH[1].n, message)
    s = submodn(k, mulmodn(secret, e))
    return G, H, xG, xH, s, e, message


def chaumpedersen_calc(G, H, xG, xH, s, e, message):
    assert isinstance(s, long)
    assert isinstance(e, long)
    assert isinstance(message, long)
    sG = multiply(G, s)
    kG = add(sG, multiply(xG, e))
    sH = multiply(H, s)
    kH = add(sH, multiply(xH, e))
    return hashs(xG[0].n, xG[1].n, xH[0].n, xH[1].n, kG[0].n, kG[1].n, kH[0].n, kH[1].n, message)


def chaumpedersen_verify(G, H, xG, xH, s, e, message):
    return e == chaumpedersen_calc(G, H, xG, xH, s, e, message)


if __name__ == "__main__":
    G=sbmul(1)
    H=sbmul(2019)
    secret = 19977808579986318922850133509558564821349392755821541651519240729619349670944
    m = 19996069338995852671689530047675557654938145690856663988250996769054266469975
    proof = chaumpedersen_create(G,H,secret,m)
    print(chaumpedersen_verify(*proof))