from libc.math cimport exp, log, sqrt, erf, M_PI, M_SQRT2
import numpy as np
cimport numpy as cnp

cdef double norm_cdf(double x):
    return 0.5 * (1.0 + erf(x/M_SQRT2))

cdef double norm_pdf(double x):
    return exp(-0.5 * x * x) / sqrt(2 * M_PI)

def call_price(double S, double K, double T, double r, double sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2)


def put_price(double S, double K, double T, double r, double sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return K * exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)