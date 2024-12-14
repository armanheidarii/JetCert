import numpy as np


def lj_numpy(r):
    sr6 = (1.0 / r) ** 6
    pot = 4.0 * (sr6 * sr6 - sr6)
    return pot


def distances_numpy(cluster):
    diff = cluster[:, np.newaxis, :] - cluster[np.newaxis, :, :]
    mat = np.sqrt((diff * diff).sum(-1))
    return mat


def potential_numpy(cluster):
    d = distances_numpy(cluster)
    dtri = np.triu(d)
    energy = lj_numpy(dtri[dtri > 1e-6]).sum()
    return energy


def go_fast(inputs):
    cluster = np.array(inputs.get("cluster"))

    energy = potential_numpy(cluster)

    return {"energy": energy}
