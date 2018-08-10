"""
https://www.cs.cornell.edu/courses/cs754/2001fa/129.PDF
"""

from .curve import *

def pedersen_com(m, r, h):
	H = hashtopoint(h)
	return add(sbmul(m), multiply(H, r)), r

def pedersen_unv(C, m, h):
	H = hashtopoint(h)
	return C[0] == add(sbmul(m), multiply(H, C[1]))
