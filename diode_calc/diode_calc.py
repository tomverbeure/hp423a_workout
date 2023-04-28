#! /usr/bin/env python3


import scipy
import scipy.constants
import math

from scipy.special import lambertw

def v_r(v_in, R, I0, n=1, T=300):

    q = scipy.constants.elementary_charge
    k = scipy.constants.Boltzmann
    
#    v_r = -lambertw(-

    print(k*T/q)

    I = I0 * (math.exp(q*v_in/(n*k*T))-1)

    print(I)

I0 = 1e-12
v_r(0.5, 200, I0)
