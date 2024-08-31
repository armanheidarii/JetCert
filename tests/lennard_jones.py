import numpy as np


def make_cluster(natoms, radius=20, seed=1981):
    np.random.seed(seed)
    cluster = np.random.normal(0, radius, size=(natoms, 3)) - 0.5
    return cluster


def input_generator():
    # for natoms in [100, 1000, 5000]:
    for natoms in [100, 500, 1000, 1500, 2000]:
        cluster = make_cluster(natoms)
        dtype = np.float64
        yield dict(
            category=(np.dtype(dtype).name,),
            x=natoms,
            input_args=(cluster,),
            input_kwargs={},
        )
