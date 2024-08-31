import numpy as np
import numba


def make_cluster(natoms, radius=20, seed=1981):
    np.random.seed(seed)
    cluster = np.random.normal(0, radius, size=(natoms, 3)) - 0.5
    return cluster


@numba.njit
def lj_numba_scalar_prange(r):
    sr6 = (1.0 / r) ** 6
    pot = 4.0 * (sr6 * sr6 - sr6)
    return pot


@numba.njit
def distance_numba_scalar_prange(atom1, atom2):
    dx = atom2[0] - atom1[0]
    dy = atom2[1] - atom1[1]
    dz = atom2[2] - atom1[2]

    r = (dx * dx + dy * dy + dz * dz) ** 0.5

    return r


@numba.njit(parallel=True)
def potential_numba_scalar_prange(cluster):
    energy = 0.0
    # numba.prange requires parallel=True flag to compile.
    # It causes the loop to run in parallel in multiple threads.
    for i in numba.prange(len(cluster) - 1):
        for j in range(i + 1, len(cluster)):
            r = distance_numba_scalar_prange(cluster[i], cluster[j])
            e = lj_numba_scalar_prange(r)
            energy += e

    return energy


def go_fast(inputs):
    cluster = np.array(inputs.get("cluster"))

    energy = potential_numba_scalar_prange(cluster)

    return {"energy": energy}


natoms = 100
cluster = make_cluster(natoms)
potential_numba_scalar_prange(cluster)
