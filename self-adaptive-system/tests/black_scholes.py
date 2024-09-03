import numpy as np

RISKFREE = 0.02
VOLATILITY = 0.30


def randfloat(rand_var, low, high):
    return (1.0 - rand_var) * low + rand_var * high


def input_generator():
    for dtype in [np.float64, np.float32]:
        for OPT_N in [1000, 100000, 1000000, 4000000]:
            category = (np.dtype(dtype).name,)

            stockPrice = randfloat(np.random.random(OPT_N), 5.0, 30.0).astype(dtype)
            optionStrike = randfloat(np.random.random(OPT_N), 1.0, 100.0).astype(dtype)
            optionYears = randfloat(np.random.random(OPT_N), 0.25, 10.0).astype(dtype)

            yield dict(
                category=category,
                x=OPT_N,
                input_args=(
                    stockPrice,
                    optionStrike,
                    optionYears,
                    RISKFREE,
                    VOLATILITY,
                ),
                input_kwargs={},
            )


def validator(input_args, input_kwargs, output):
    actual_call, actual_put = output
    # use numpy implementation above as reference
    expected_call, expected_put = black_scholes(*input_args, **input_kwargs)

    np.testing.assert_allclose(actual_call, expected_call, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(actual_put, expected_put, rtol=1e-5, atol=1e-5)
