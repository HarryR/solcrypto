from py_ecc.bn128 import pairing, G2, G1

from .altbn128 import hashsn, mulmodp, invmodn, multiply


def accumulate(items_list):
    x0_mul_to_xn = 1
    for item in items_list:
        xi = hashsn(item)
        x0_mul_to_xn = mulmodp(x0_mul_to_xn, xi)

    FxK = x0_mul_to_xn
    AkX = multiply(G1, x0_mul_to_xn)
    return (FxK, AkX)


def witness(FxK, AkX, my_item, items_list):
    y = hashsn(my_item)
    return multiply(AkX, invmodn(y))


def ismember(FxK, AkX, my_item, W_x):
    x = hashsn(my_item)
    e1 = pairing(G2, AkX)
    e2 = pairing(multiply(G2, x), W_x)
    assert e1 == e2
    return e1 == e2


if __name__ == "__main__":
    items = list(range(1,10))
    my_item = items[3]
    FxK, AkX = accumulate(items)
    W_x = witness(FxK, AkX, my_item, items)
    ismember(FxK, AkX, my_item, W_x)
