import math
import numpy as np
from numba import jit


def randfloat(rand_var, low, high):
    return (1.0 - rand_var) * low + rand_var * high


@jit(nopython=True)
def cnd_numba(d):
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.330274429
    RSQRT2PI = 0.39894228040143267793994605993438
    K = 1.0 / (1.0 + 0.2316419 * math.fabs(d))
    ret_val = (
        RSQRT2PI
        * math.exp(-0.5 * d * d)
        * (K * (A1 + K * (A2 + K * (A3 + K * (A4 + K * A5)))))
    )
    if d > 0:
        ret_val = 1.0 - ret_val
    return ret_val


@jit(nopython=True)
def black_scholes_numba(stockPrice, optionStrike, optionYears, Riskfree, Volatility):
    callResult = np.empty_like(stockPrice)
    putResult = np.empty_like(stockPrice)

    S = stockPrice
    X = optionStrike
    T = optionYears
    R = Riskfree
    V = Volatility
    for i in range(len(S)):
        sqrtT = math.sqrt(T[i])
        d1 = (math.log(S[i] / X[i]) + (R + 0.5 * V * V) * T[i]) / (V * sqrtT)
        d2 = d1 - V * sqrtT
        cndd1 = cnd_numba(d1)
        cndd2 = cnd_numba(d2)

        expRT = math.exp((-1.0 * R) * T[i])
        callResult[i] = S[i] * cndd1 - X[i] * expRT * cndd2
        putResult[i] = X[i] * expRT * (1.0 - cndd2) - S[i] * (1.0 - cndd1)

    return callResult, putResult


def go_fast(inputs):
    stockPrice = np.array(inputs.get("stockPrice"))
    optionStrike = np.array(inputs.get("optionStrike"))
    optionYears = np.array(inputs.get("optionYears"))
    Riskfree = inputs.get("Riskfree")
    Volatility = inputs.get("Volatility")

    callResult, putResult = black_scholes_numba(
        stockPrice, optionStrike, optionYears, Riskfree, Volatility
    )

    return {"callResult": callResult.tolist(), "putResult": putResult.tolist()}


stockPrice = randfloat(np.random.random(1000), 5.0, 30.0).astype(np.float64)
optionStrike = randfloat(np.random.random(1000), 1.0, 100.0).astype(np.float64)
optionYears = randfloat(np.random.random(1000), 0.25, 10.0).astype(np.float64)
Riskfree = 0.02
Volatility = 0.30

black_scholes_numba(stockPrice, optionStrike, optionYears, Riskfree, Volatility)
